import abc
import collections
import functools
import operator

from mu.utils import infit
from mu.utils import tools

from mu.rhy import binr

from mu.mel import ji

from mutools import synthesis

from pbIII.fragments import harmony
from pbIII.globals import globals


class _MetaSample(type):
    def __new__(cls, name, bases, attrs):
        def auto_init(self, **kwargs):
            available_args = self._basic_args + tuple(self._infit_args.keys())

            for arg_name in available_args:

                try:
                    arg_value = kwargs[arg_name]
                except KeyError:
                    arg_value = None

                if arg_name in self._infit_args:

                    if not isinstance(arg_value, infit.InfIt):
                        tests = tuple(
                            isinstance(arg_value, allowed_class)
                            for allowed_class in self._infit_args[arg_name]
                        )

                        if any(tests):
                            arg_value = infit.Value(arg_value)

                        else:
                            msg = "Type of argument '{}' (value '{}') is '{}', ".format(
                                arg_name, arg_value, type(arg_value)
                            )
                            msg += "while only '{}' are allowed types.".format(
                                self._infit_args[arg_name]
                            )
                            raise TypeError(msg)

                setattr(self, arg_name, arg_value)

        attrs["__init__"] = auto_init
        return type.__new__(cls, name, bases, attrs)


class _AbstractInstrument(metaclass=_MetaSample):
    """Abstract Csound Instrument.

    Unlike the usual approach when one static instrument get defined and a score get
    automatically generated from the musical data, this approach also allows the dynamic
    generation of an instrument according to the particular needs of the current data.
    """

    @abc.abstractproperty
    def _basic_args(self) -> tuple:
        raise NotImplementedError

    @abc.abstractproperty
    def _infit_args(self) -> dict:
        raise NotImplementedError

    @property
    def _upper_args(self) -> dict:
        return {}

    def instrument(self, instrument_idx: int, **kwargs) -> tuple:
        """Csound instrument definition."""
        instr = "instr {}".format(instrument_idx)
        endin = "endin"
        return (instr, endin)

    @abc.abstractmethod
    def make_score_lines(
        self, instrument_idx: int, start: float, duration: float, **kwargs
    ) -> tuple:
        raise NotImplementedError

    def __call__(
        self, instrument_idx: int, start: float, duration: float, **kwargs
    ) -> tuple:
        """Return instrument definition & score lines."""

        for arg in self._infit_args:
            kwargs.update({arg: next(getattr(self, arg))})

        for arg in self._upper_args:
            if arg not in kwargs:
                kwargs.update({arg: self._upper_args[arg]})

        instrument = self.instrument(instrument_idx, **kwargs)
        score_lines = self.make_score_lines(instrument_idx, start, duration, **kwargs)
        return instrument, score_lines


class Sample(_AbstractInstrument):
    _basic_args = tuple([])
    _infit_args = {
        # path of the sample
        "path": (str,),
        # either float (Hz) or if there isn't any certain detectable frequency set to None
        "frequency": (float, int, type(None)),
        # multipy pitch
        "pitch_factor": (float, int, type(None)),
        # tuple to tell which channels to use and None if all channels shall be used (and
        # mixed down to mono source)
        "channels": (tuple, type(None)),
        # float to skip n seconds of the sample or None for starting at the beginning
        "skip_time": (float, int, type(None)),
        # size of glissando
        "glissando_size": (float, int, type(None)),
        # duration of glissando
        "glissando_duration": (float, int, type(None)),
        # time until glissando starts
        "glissando_offset": (float, int, type(None)),
        # True -> from glissando position to original pitch
        # False -> from original pitch position to glissando pitch position
        "glissando_direction": (bool, type(None)),
        # ############################################################################
        # ############# EFFECTS ######################################################
        # ############################################################################
        # float for having a resonance filter at the particular frequency or None if no
        # resonance filter shall be used
        "resonance_filter_frequency": (float, type(None)),
        # float for having a resonance filter with the particular bandwidth or None if no
        # resonance filter shall be used
        "resonance_filter_bandwidth": (float, type(None)),
        # float for having a notch filter at the particular frequency or None if no
        # resonance filter shall be used
        "notch_filter_frequency": (float, type(None)),
        # float for having a notch filter with the particular bandwidth or None if no
        # resonance filter shall be used
        "notch_filter_bandwidth": (float, type(None)),
        "lowpass_filter_frequency": (float, type(None)),
        "lowpass_filter_q": (float, type(None)),
        "distortion": (float, type(None)),
    }

    _effects = {
        "reson": ("resonance_filter_frequency", "resonance_filter_bandwidth", 1),
        "areson": ("notch_filter_frequency", "notch_filter_bandwidth"),
        "lowpass2": ("lowpass_filter_frequency", "lowpass_filter_q"),
        "distort": ("distortion",),
    }

    # possible arguments send from outside the class.
    # value equals the default value and not the expected type (like in _infit_args)
    _upper_args = {
        # pitch in Hertz. could also be a list or tuple filled with possible values in
        # Hertz. Then the class will automatically choose the closest frequency to the
        # frequency of the current sample.
        "pitch": None,
        # volume factor (usual value would range between 0 and 1)
        "volume": 1,
    }

    @staticmethod
    def _make_pitch_interpolation(kwargs: dict) -> str:
        if kwargs["pitch_factor"] is None:
            pitch_factor = 1
        else:
            pitch_factor = kwargs["pitch_factor"]

        if kwargs["frequency"] is not None and kwargs["pitch"] is not None:

            if isinstance(kwargs["pitch"], float):
                pitch_factor *= kwargs["pitch"] / kwargs["frequency"]

            elif hasattr(kwargs["pitch"], "__getitem__"):
                pitch_factor_ = tools.find_closest_item(
                    kwargs["frequency"], kwargs["pitch"]
                )
                pitch_factor_ /= kwargs["frequency"]
                pitch_factor *= pitch_factor_

            else:
                msg = "Unknown type '{}' for 'pitch' with value '{}'".format(
                    type(kwargs["pitch"]), kwargs["pitch"]
                )
                raise TypeError(msg)

        if all(
            tuple(
                kwargs[arg] is not None
                for arg in (
                    "glissando_size",
                    "glissando_duration",
                    "glissando_offset",
                    "glissando_direction",
                )
            )
        ):
            glissando_pitch_factor = pitch_factor * kwargs["glissando_size"]

            if kwargs["glissando_direction"]:
                start_factor, end_factor = glissando_pitch_factor, pitch_factor
            else:
                end_factor, start_factor = glissando_pitch_factor, pitch_factor

            pitch_interpolation = "kPitch linseg "

            glissando_offset = kwargs["glissando_offset"]
            if glissando_offset > 0:
                pitch_interpolation += "{0}, {1}, ".format(
                    start_factor, glissando_offset
                )

            pitch_interpolation += "{0}, {1}, {2}".format(
                start_factor, kwargs["glissando_duration"], end_factor
            )

        else:
            pitch_interpolation = "kPitch linseg {0}, p3, {0}".format(pitch_factor)

        return pitch_interpolation

    def instrument(self, instrument_idx: int, **kwargs) -> tuple:
        n_channels = synthesis.pyo.sndinfo(kwargs["path"])[3]

        if kwargs["channels"] is None:
            channel2use = tuple(range(n_channels))
        else:
            channel2use = kwargs["channels"]

        name_of_signals = tuple("aSignal{}".format(idx) for idx in range(n_channels))

        pitch_interpolation = self._make_pitch_interpolation(kwargs)

        diskin2 = "{} diskin2 p4, kPitch, p5, 0, 6, 4".format(
            ", ".join(name_of_signals)
        )
        summarized = " + ".join(
            tuple(
                signal
                for sig_idx, signal in enumerate(name_of_signals)
                if sig_idx in channel2use
            )
        )
        summarized = "aSummarized = ({}) / {}".format(summarized, len(channel2use))

        last_signal = "aSummarized"
        effect_lines = []
        for effect in self._effects:
            arguments = self._effects[effect]
            argument_values = {
                arg: kwargs[arg] for arg in arguments if type(arg) is str
            }
            if all(tuple(argument_values[arg] is not None for arg in argument_values)):

                if effect == "distort":
                    dist_table_name = "iDistTable"
                    dist_func_table = "{} ftgenonce 0,0, 257, 9, .5,1,270,".format(
                        dist_table_name
                    )
                    dist_func_table += "1.5,.33,90,2.5,.2,270,3.5,.143,90,4.5,.111,270"
                    effect_lines.append(dist_func_table)
                    arguments += (dist_table_name,)

                signal_name = "aEffect{}".format(len(effect_lines))
                fx = "{} {} {}, ".format(signal_name, effect, last_signal)

                fx_data = []
                for val in arguments:
                    try:
                        fx_data.append(str(argument_values[val]))
                    except KeyError:
                        fx_data.append(str(val))

                fx += ", ".join(fx_data)
                effect_lines.append(fx)
                last_signal = signal_name

        if effect_lines:
            balance = "{0} balance {0}, aSummarized".format(last_signal)
        else:
            balance = ""

        out = "out {} * p6".format(last_signal)

        top_definition = super().instrument(instrument_idx)

        lines = (top_definition[0], pitch_interpolation, diskin2, summarized)
        lines += tuple(effect_lines)
        lines += (balance, out, top_definition[-1])
        return lines

    def make_score_lines(
        self, instrument_idx: int, start: float, duration: float, **kwargs
    ) -> tuple:
        # set duration to sample duration
        duration = synthesis.pyo.sndinfo(kwargs["path"])[1]

        if kwargs["skip_time"] is None:
            skip_time = 0
        else:
            skip_time = kwargs["skip_time"]

        line = 'i{} {} {} "{}" {} {}'.format(
            instrument_idx, start, duration, kwargs["path"], skip_time, kwargs["volume"]
        )
        return (line,)


class ResonanceSample(Sample):
    _infit_args = dict(Sample._infit_args)
    _infit_args.update({"resonance_filter_octave": (int,)})

    _oct_border = (globals.CONCERT_PITCH, globals.CONCERT_PITCH * 2)

    def __call__(
        self, instrument_idx: int, start: float, duration: float, **kwargs
    ) -> tuple:
        try:
            self._pitch_counter
        except AttributeError:
            self._pitch_counter = collections.Counter([])

        pitch_data = kwargs["pitch"]

        # making sure there is any data
        assert pitch_data

        relevant_pitch_data = tuple(
            p
            for p in pitch_data
            if p >= self._oct_border[0] and p <= self._oct_border[1]
        )
        pitch_counter_pairs = tuple(
            (self._pitch_counter[p], p) for p in relevant_pitch_data
        )
        choosen_pitch = sorted(pitch_counter_pairs, key=operator.itemgetter(0))[0][1]

        self._pitch_counter.update({choosen_pitch: 1})
        kwargs["resonance_filter_frequency"] = choosen_pitch * (
            2 ** next(self.resonance_filter_octave)
        )
        kwargs["pitch"] = None

        for arg in self._infit_args:
            if arg != "resonance_filter_frequency":
                kwargs.update({arg: next(getattr(self, arg))})

        for arg in self._upper_args:
            if arg not in kwargs:
                kwargs.update({arg: self._upper_args[arg]})

        instrument = self.instrument(instrument_idx, **kwargs)
        score_lines = self.make_score_lines(instrument_idx, start, duration, **kwargs)
        return instrument, score_lines


class Rhythmizer(synthesis.BasedCsoundEngine):
    print_output = False
    remove_files = True

    #########################################################################
    #       ATTRIBUTES THAT HAVE TO GET INITALISED BY SEGMENT CLASS         #
    #########################################################################

    # segment class
    segment = None

    #########################################################################
    # values that get set after manual initalization before rendering       #
    #########################################################################

    _orc = None
    _sco = None

    def __init__(
        self,
        voice_meters2occupy: tuple = (0,),
        sample_maker: infit.InfIt = infit.Cycle(
            (
                Sample(
                    path=infit.Cycle(globals.SAM_KENDANG_HIGH_LOW_CLOSE_HAND),
                    frequency=globals.SAM_KENDANG_HIGH_LOW_CLOSE_HAND.information[
                        "frequency"
                    ],
                    pitch_factor=infit.Cycle((0.5, 2, 4, 1)),
                ),
                Sample(
                    path=infit.Cycle(globals.SAM_KENDANG_LOW_HIGH_CLOSE_HAND),
                    frequency=globals.SAM_KENDANG_LOW_HIGH_CLOSE_HAND.information[
                        "frequency"
                    ],
                    pitch_factor=infit.Cycle((0.5, 2, 4, 1)),
                ),
                Sample(
                    path=infit.Cycle(globals.SAM_CYMBALS_BIG_AGGRESSIVE),
                    frequency=globals.SAM_CYMBALS_BIG_AGGRESSIVE.information[
                        "frequency"
                    ],
                    pitch_factor=infit.Uniform(0.4, 1.3),
                ),
                Sample(
                    path=infit.Cycle(globals.SAM_KENDANG_LOW_LOW_CLOSE_HAND),
                    frequency=globals.SAM_KENDANG_LOW_LOW_CLOSE_HAND.information[
                        "frequency"
                    ],
                    pitch_factor=infit.Cycle((0.5, 2, 4, 1)),
                ),
            )
        ),
        likelihood_range: tuple = (0.79, 1),
        volume_range: tuple = (0.5, 1),
        seed: int = 100,
        chord: infit.InfIt = harmony.find_harmony(),
        ignore_beats_occupied_by_voice: bool = True,
        voices2ignore: tuple = None,
        octaves: tuple = tuple(range(-3, 4)),
    ):
        if voices2ignore is None:
            voices2ignore = voice_meters2occupy

        if type(chord) is tuple:
            chord = infit.Value(chord)

        elif isinstance(chord, infit.InfIt):
            pass

        else:
            msg = "Wrong type '{}' for chord '{}'.".format(type(chord), chord)
            raise TypeError(msg)

        self._voices2ignore = voices2ignore
        self._voice_meters2occupy = voice_meters2occupy
        self._sample_maker = sample_maker
        self._likelihood_range = likelihood_range
        self._volume_range = volume_range
        self._chord = chord
        self._ignore_beats_occupied_by_voice = ignore_beats_occupied_by_voice
        self._octaves = octaves

        import random

        random.seed(seed)

        self._random_module = random

    @property
    def allowed_metrical_numbers(self) -> tuple:
        return tuple(
            self.segment._metrical_numbers[idx] for idx in self._voice_meters2occupy
        )

    def find_possible_attack_indices(self) -> tuple:
        duration = int(self.segment._duration)
        bar_size = duration // self.segment._n_bars
        generator_size_per_metrical_number = (
            bar_size // number for number in self.allowed_metrical_numbers
        )
        metrical_rhythms = tuple(
            binr.Compound.from_generator(generator_size, duration)
            for generator_size in generator_size_per_metrical_number
        )
        attack_indices = tuple(
            int(item)
            for item in functools.reduce(
                lambda a, b: a.union(b), metrical_rhythms
            ).convert2absolute()
        )

        if self._ignore_beats_occupied_by_voice:
            occupied_by_voice = []
            for v_idx in self._voices2ignore:
                occupied_by_voice += [
                    int(item)
                    for item in self.segment._voices_inner[v_idx]
                    .convert2absolute()
                    .delay
                ]

            attack_indices = tuple(
                idx for idx in attack_indices if idx not in occupied_by_voice
            )

        return attack_indices

    def find_attack_indices(self) -> tuple:
        possible_attack_indices = self.find_possible_attack_indices()
        scaled_weights = tools.scale(
            self.segment._weight_per_beat, *self._likelihood_range
        )

        attack_positions = []
        original_weight = []
        for possible_attack_position in possible_attack_indices:
            if self._random_module.random() < scaled_weights[possible_attack_position]:
                attack_positions.append(possible_attack_position)
                original_weight.append(
                    self.segment._weight_per_beat[possible_attack_position]
                )

        return tuple(attack_positions), tuple(original_weight)

    def find_start_and_duration_and_volume(self) -> tuple:
        """1. start values, 2. duration per attack, 3. volume per attack"""

        attack_indices, weight_per_attack = self.find_attack_indices()

        has_first_attack = True
        if 0 not in attack_indices:
            attack_indices = (0,) + attack_indices
            has_first_attack = False

        duration_values = tuple(
            (b - a) * self.segment._tempo_factor
            for a, b in zip(
                attack_indices, attack_indices[1:] + (int(self.segment._duration),)
            )
        )
        start_values = tools.accumulate_from_zero(duration_values)

        if not has_first_attack:
            start_values = start_values[1:]
            duration_values = duration_values[1:]

        volume_per_attack = tools.scale(weight_per_attack, *self._volume_range)

        return start_values, duration_values, volume_per_attack

    def make_data(self) -> tuple:
        """set orc and sco attributes."""

        start_per_attack, duration_per_attack, volume_per_attack = (
            self.find_start_and_duration_and_volume()
        )

        orc_lines = []
        sco_lines = []

        for instr_idx, start, duration, volume in zip(
            range(len(start_per_attack)),
            start_per_attack,
            duration_per_attack,
            volume_per_attack,
        ):

            valid_pitches = functools.reduce(
                operator.add,
                tuple(
                    tuple(
                        ji.JIPitch(p, multiply=globals.CONCERT_PITCH)
                        .register(octave)
                        .freq
                        for octave in self._octaves
                    )
                    for p in next(self._chord)[0](
                        *globals.MALE_SOIL.harmonic_primes_per_bar[
                            self.segment._bar_number
                        ]
                    )
                ),
            )
            orc_data, sco_data = next(self._sample_maker)(
                instrument_idx=instr_idx + 1,
                start=start,
                duration=duration,
                volume=volume,
                pitch=valid_pitches,
            )

            orc_lines.extend(orc_data + ("",))
            sco_lines.extend(sco_data)

        self._orc = "\n".join(orc_lines)
        self._sco = "\n".join(sco_lines)

    @property
    def cname(self) -> str:
        return ".rhythmizer"

    @property
    def orc(self) -> str:
        return self._orc

    @property
    def sco(self) -> str:
        return self._sco

    def render(self, path: str):
        # define orc and sco
        if self._orc is None:
            self.make_data()

        # usual render process
        return super().render(path)
