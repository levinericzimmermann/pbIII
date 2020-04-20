import abc
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
                            msg = "Type of argument '{}' is '{}', ".format(
                                arg_name, type(arg_value)
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
        "frequency": (float, type(None)),
        # multipy pitch
        "pitch_factor": (float, type(None)),
        # tuple to tell which channels to use and None if all channels shall be used (and
        # mixed down to mono source)
        "channels": (tuple, type(None)),
        # float to skip n seconds of the sample or None for starting at the beginning
        "skip_time": (float, type(None)),
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

    def instrument(self, instrument_idx: int, **kwargs) -> tuple:
        n_channels = synthesis.pyo.sndinfo(kwargs["path"])[3]

        if kwargs["channels"] is None:
            channel2use = tuple(range(n_channels))
        else:
            channel2use = kwargs["channels"]

        name_of_signals = tuple("aSignal{}".format(idx) for idx in range(n_channels))
        diskin2 = "{} diskin2 p4, p5, p6, 0, 6, 4".format(", ".join(name_of_signals))
        summarized = " + ".join(
            tuple(
                signal
                for sig_idx, signal in enumerate(name_of_signals)
                if sig_idx in channel2use
            )
        )
        summarized = "aSummarized = ({}) / {}".format(summarized, len(channel2use))
        out = "out aSummarized * p7"

        top_definition = super().instrument(instrument_idx)

        lines = (top_definition[0], diskin2, summarized, out, top_definition[-1])
        return lines

    def make_score_lines(
        self, instrument_idx: int, start: float, duration: float, **kwargs
    ) -> tuple:
        # set duration to sample duration
        duration = synthesis.pyo.sndinfo(kwargs["path"])[1]

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

        if kwargs["skip_time"] is None:
            skip_time = 0
        else:
            skip_time = kwargs["skip_time"]

        line = 'i{} {} {} "{}" {} {} {}'.format(
            instrument_idx,
            start,
            duration,
            kwargs["path"],
            pitch_factor,
            skip_time,
            kwargs["volume"],
        )
        return (line,)


class Rhythmizer(synthesis.BasedCsoundEngine):

    #########################################################################
    #       ATTRIBUTES THAT HAS TO GET INITALISED BY SEGMENT CLASS          #
    #########################################################################

    # tuple
    weight_per_beat = None
    # old.Melody
    voice = None
    # int
    n_bars = None
    # tuple filled with integer
    allowed_metrical_numbers = None
    # float
    tempo_factor = None
    # int
    bar_number = None

    #########################################################################
    # values that get set after manual initalization before rendering       #
    #########################################################################

    _orc = None
    _sco = None

    def __init__(
        self,
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
        chord: tuple = harmony.find_harmony(),
        ignore_beats_occupied_by_voice: bool = True,
        octaves: tuple = tuple(range(-3, 4)),
    ):
        self._sample_maker = sample_maker
        self._likelihood_range = likelihood_range
        self._volume_range = volume_range
        self._chord = chord
        self._ignore_beats_occupied_by_voice = ignore_beats_occupied_by_voice
        self._octaves = octaves

        import random

        random.seed(seed)

        self._random_module = random

    def find_possible_attack_indices(self) -> tuple:
        duration = int(self.voice.duration)
        bar_size = duration // self.n_bars
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
            occupied_by_voice = tuple(
                int(item) for item in self.voice.convert2absolute().delay
            )
            attack_indices = tuple(
                idx for idx in attack_indices if idx not in occupied_by_voice
            )

        return attack_indices

    def find_attack_indices(self) -> tuple:
        possible_attack_indices = self.find_possible_attack_indices()
        scaled_weights = tools.scale(self.weight_per_beat, *self._likelihood_range)

        attack_positions = []
        original_weight = []
        for possible_attack_position in possible_attack_indices:
            if self._random_module.random() < scaled_weights[possible_attack_position]:
                attack_positions.append(possible_attack_position)
                original_weight.append(self.weight_per_beat[possible_attack_position])

        return tuple(attack_positions), tuple(original_weight)

    def find_start_and_duration_and_volume(self) -> tuple:
        """1. start values, 2. duration per attack, 3. volume per attack"""

        attack_indices, weight_per_attack = self.find_attack_indices()

        has_first_attack = True
        if 0 not in attack_indices:
            attack_indices = (0,) + attack_indices
            has_first_attack = False

        duration_values = tuple(
            (b - a) * self.tempo_factor
            for a, b in zip(
                attack_indices, attack_indices[1:] + (int(self.voice.duration),)
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

        valid_pitches = functools.reduce(
            operator.add,
            tuple(
                tuple(
                    ji.JIPitch(p, multiply=globals.CONCERT_PITCH).register(octave).freq
                    for octave in self._octaves
                )
                for p in self._chord[0](
                    *globals.MALE_SOIL.harmonic_primes_per_bar[self.bar_number]
                )
            ),
        )

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
