import functools
import itertools
import operator

from mu.mel import ji
from mu.mel import mel
from mu.rhy import binr
from mu.rhy import indispensability
from mu.sco import old
from mu.utils import infit
from mu.utils import prime_factors
from mu.utils import tools

from mutools import ambitus
from mutools import MU
from mutools import polyrhythms
from mutools import pteqer
from mutools import schillinger


from pbIII.fragments import counterpoint
from pbIII.fragments import harmony
from pbIII.globals import globals

from pbIII.engines import diva
from pbIII.engines import glitter
from pbIII.engines import pteq
from pbIII.engines import radio


class PBIII_Segment(MU.Segment):
    orchestration = globals.PBIII_ORCHESTRATION


class Silence(PBIII_Segment):
    """Segment class that generates only silence, for rests etc."""

    def __init__(self, name: str, duration: float, start: float = 0):
        self.__duration = duration
        super().__init__(name, start=start, **{})

    @property
    def duration(self):
        return self.__duration


class CyclicPermutation(object):
    """Helper class for distributing natural radio sounds on different speaker."""

    def __init__(self, pattern: tuple) -> None:
        self.__cycle = itertools.cycle(tuple(set(schillinger.permute_cyclic(pattern))))
        self.__pattern = pattern

    def __repr__(self) -> str:
        return "CyclicPermutation({})".format(self.pattern)

    def __next__(self) -> tuple:
        return next(self.__cycle)

    @property
    def pattern(self) -> tuple:
        return self.__pattern


class ThreeVoiceCP(PBIII_Segment):
    """General Segment class for Segments with counterpoint for 3 voices.

    More specific Segments could be generated through inheritance.
    """

    counterpoint_class = counterpoint.ThreeVoiceRhythmicCP

    def __init__(
        self,
        name: str,
        tracks2ignore=tuple([]),
        rhythm_maker=None,
        start: float = 0,
        group: tuple = (0, 0, 0),
        gender: bool = True,
        n_bars: int = 1,
        anticipation_time: float = 0.5,
        overlaying_time: float = 0.5,
        duration_per_bar: float = 5,
        include_voices: bool = True,
        include_diva: bool = True,
        include_glitter: bool = True,
        include_natural_radio: bool = True,
        dynamic_range_of_voices: tuple = (0.2, 0.95),
        max_spectrum_profile_change: int = 10,
        glitter_include_dissonant_pitches: bool = True,
        glitter_modulater_per_voice: tuple = ("randomi", "randomi", "randomi"),
        radio_samples: tuple = (
            "pbIII/samples/radio/bielefeld/2.wav",
            "pbIII/samples/radio/UK/4.wav",
            "pbIII/samples/radio/Italy/2.wav",
        ),
        radio_make_envelope: bool = True,
        radio_average_volume: float = 0.3,
        radio_min_volume: float = 0.65,
        radio_max_volume: float = 1,
        radio_n_changes: int = 5,
        radio_crossfade_duration: float = 0.5,
        radio_shadow_time: float = 0.175,
        radio_silent_channels: tuple = tuple([]),
        cp_constraints_harmonic: tuple = tuple([]),
        cp_constraints_interpolation: tuple = tuple([]),
        speech_init_attributes: dict = {},
        ambitus_maker: ambitus.AmbitusMaker = ambitus.SymmetricalRanges(
            ji.r(1, 1), ji.r(3, 1), ji.r(5, 4)
        ),
        start_harmony: tuple = None,
        pteq_engine_per_voice: tuple = (
            pteq.mk_contrasting_pte(),
            pteq.mk_contrasting_pte(),
            pteq.mk_contrasting_pte(),
        ),
        diva_engine_per_voice: tuple = (
            diva.FloatingDivaMidiEngine,
            diva.FloatingDivaMidiEngine,
            diva.FloatingDivaMidiEngine,
        ),
        # in case the user want to use her or his own metrical numbers
        metrical_numbers: tuple = None,
    ) -> None:

        self.__n_bars = n_bars
        self.__gender_code = ("N", "P")[int(gender)]
        self.__bar_number = globals.MALE_SOIL.detect_group_index(group)
        if metrical_numbers is None:
            metrical_numbers = globals.MALE_SOIL.metre_per_vox_per_bar[
                self.__bar_number
            ]
        self.__metrical_numbers = metrical_numbers
        self.__anticipation_time = anticipation_time
        self.__overlaying_time = overlaying_time
        self.__pteq_engine_per_voice = pteq_engine_per_voice
        self.__diva_engine_per_voice = diva_engine_per_voice

        if rhythm_maker is None:

            def rhythm_maker(self) -> tuple:
                return tuple(
                    binr.Compound.from_euclid(
                        metrical_prime * self.__n_bars, 7 * self.__n_bars
                    )
                    for metrical_prime in self.__metrical_numbers
                )

        rhythms = polyrhythms.Polyrhythm(*rhythm_maker(self)).transformed_rhythms

        self.__bar_size = int(sum(rhythms[0])) // n_bars
        self.__weight_per_beat_for_one_bar = self.make_weight_per_beat_for_one_bar(
            self.__metrical_numbers, self.__bar_size
        )
        self.__tempo_factor = self.convert_duration2factor(
            duration_per_bar, self.__bar_size
        )

        self.__weight_per_beat = tuple(
            self.__weight_per_beat_for_one_bar * self.__n_bars
        )

        cp = self.counterpoint_class(
            rhythms,
            gender=gender,
            weight_per_beat=self.__weight_per_beat,
            constraints_harmonic_resolution=cp_constraints_harmonic,
            constraints_added_pitches=cp_constraints_interpolation,
            ambitus_maker=ambitus_maker,
            start_harmony=start_harmony,
        )
        self.__counterpoint_result = cp(
            *globals.MALE_SOIL.harmonic_primes_per_bar[self.__bar_number]
        )

        init_attributes = {}

        self.__duration_per_voice = duration_per_bar * self.__n_bars

        self.__voices_inner = tuple(
            old.Melody(old.Tone(p, r) for p, r in zip(vox[0], vox[1]))
            for vox in self.__counterpoint_result[0]
        )
        self.__attribute_maker_inner = pteqer.AttributeMaker(
            self.__voices_inner,
            metricity_per_beat=self.__weight_per_beat,
            max_spectrum_profile_change=max_spectrum_profile_change,
            dynamic_range=dynamic_range_of_voices,
        )

        self.__voices_outer = tuple(
            old.Melody(old.Tone(p, r) for p, r in zip(vox[0], vox[1]))
            for vox in self.__counterpoint_result[1]
        )
        self.__attribute_maker_outer = pteqer.AttributeMaker(
            self.__voices_outer,
            metricity_per_beat=self.__weight_per_beat,
            max_spectrum_profile_change=max_spectrum_profile_change,
            dynamic_range=dynamic_range_of_voices,
        )

        # make pianoteq voices
        if include_voices:
            init_attributes.update(self.make_voices())

        # make diva voices
        if include_diva:
            init_attributes.update(self.make_diva_voices())

        # make glitter voices
        if include_glitter:
            init_attributes.update(
                self.make_glitter_voices(
                    glitter_include_dissonant_pitches, glitter_modulater_per_voice
                )
            )

        # make natural radio voices
        if include_natural_radio:
            voices_inner_and_outer = []
            for voices, volume_per_voice in (
                (
                    self.__voices_inner,
                    self.__attribute_maker_inner.volume_per_tone_per_voice,
                ),
                (
                    self.__voices_outer,
                    self.__attribute_maker_outer.volume_per_tone_per_voice,
                ),
            ):
                voices = tuple(
                    old.Melody(
                        old.Tone(tone.pitch, tone.delay, tone.delay, volume=volume)
                        for tone, volume in zip(voice, volume_per_tone)
                    )
                    for voice, volume_per_tone in zip(voices, volume_per_voice)
                )
                voices_inner_and_outer.append(voices)

            init_attributes.update(
                self.make_natural_radio(
                    voices_inner_and_outer[0],
                    voices_inner_and_outer[1],
                    self.__tempo_factor,
                    gender,
                    make_envelope=radio_make_envelope,
                    samples=radio_samples,
                    n_changes=radio_n_changes,
                    crossfade_duration=radio_crossfade_duration,
                    anticipation_time=self.__anticipation_time,
                    overlaying_time=self.__overlaying_time,
                    average_volume=radio_average_volume,
                    min_volume=radio_min_volume,
                    max_volume=radio_max_volume,
                    shadow_time=radio_shadow_time,
                    silent_channels=radio_silent_channels,
                )
            )

        # make speech voices
        init_attributes.update(speech_init_attributes)

        super().__init__(
            name=name, start=start, tracks2ignore=tracks2ignore, **init_attributes
        )

    @property
    def duration(self) -> float:
        return super().duration - self.__overlaying_time

    def make_voices(self) -> dict:
        init_attributes = {}

        for (
            v_idx,
            voice,
            spectrum_profile_per_tone,
            volume_per_tone,
            pteq_engine,
        ) in zip(
            range(len(self.__counterpoint_result[0])),
            self.__counterpoint_result[0],
            self.__attribute_maker_inner.spectrum_profile_per_tone,
            self.__attribute_maker_inner.volume_per_tone_per_voice,
            self.__pteq_engine_per_voice,
        ):
            sound_engine = pteq_engine(
                self.__tempo_factor,
                voice[0],
                voice[1],
                voice[2],
                volume_per_tone,
                spectrum_profile_per_tone,
            )

            voice_name = "voice{}{}".format(self.__gender_code, v_idx)

            init_attributes.update(
                {
                    voice_name: {
                        "start": 0,
                        "duration": self.__duration_per_voice,
                        "sound_engine": sound_engine,
                    }
                }
            )

        return init_attributes

    def make_diva_voices(self) -> dict:
        init_attributes = {}
        for v_idx, voice in enumerate(self.__counterpoint_result[1]):
            voice_name = "diva{}{}".format(self.__gender_code, v_idx)
            sound_engine = diva.DivaSimulation(self.__tempo_factor, voice[0], voice[1])
            init_attributes.update(
                {
                    voice_name: {
                        "start": 0,
                        "duration": self.__duration_per_voice,
                        "sound_engine": sound_engine,
                    }
                }
            )

        return init_attributes

    def make_glitter_voices(
        self, include_dissonant_pitches: bool, glitter_modulater_per_voice: tuple
    ) -> dict:
        init_attributes = {}
        if include_dissonant_pitches:
            voice_base = self.__counterpoint_result[0]
        else:
            voice_base = self.__counterpoint_result[1]

        voices = tuple(
            old.Melody(old.Tone(p, r) for p, r in zip(vox[0], vox[1]))
            for vox in voice_base
        )
        glitter_duration = self.__duration_per_voice + self.__anticipation_time
        glitter_duration += self.__overlaying_time

        for combination, modulator in zip(
            tuple(itertools.combinations(tuple(range(3)), 2)),
            glitter_modulater_per_voice,
        ):
            sound_engine = glitter.GlitterEngine(
                voices[combination[0]],
                voices[combination[1]],
                self.__tempo_factor,
                anticipation_time=self.__anticipation_time,
                overlaying_time=self.__overlaying_time,
                modulator=modulator,
            )

            voice_name = "glitter{}{}{}".format(
                self.__gender_code, *sorted(combination)
            )

            init_attributes.update(
                {
                    voice_name: {
                        "start": -self.__anticipation_time,
                        "duration": glitter_duration,
                        "sound_engine": sound_engine,
                    }
                }
            )

        return init_attributes

    @staticmethod
    def make_natural_radio(
        voices_main: tuple,
        voices_side: tuple,
        tempo_factor: float,
        gender: bool,
        make_envelope: bool,
        samples: tuple,
        n_changes: int,
        crossfade_duration: float,
        anticipation_time: float,
        overlaying_time: float,
        average_volume: float,
        min_volume: float,
        max_volume: float,
        shadow_time: float,
        silent_channels: tuple,
    ) -> dict:
        n_samples = len(samples)

        # make sure there are at least one sample but not more than three
        assert n_samples in (1, 2, 3)

        # are those asserts here really necessary?
        assert shadow_time <= anticipation_time
        assert shadow_time <= overlaying_time

        inner_voices = globals.POSITIVE_VOICES_POSITION
        outer_voices = globals.NEGATIVE_VOICES_POSITIONS

        duration = float(voices_main[0].duration * tempo_factor)
        duration += anticipation_time + overlaying_time

        if not gender:
            inner_voices, outer_voices = outer_voices, inner_voices

        delay_volume_pairs_per_voice = tuple(
            tuple(
                (delay, tone.volume)
                for delay, tone in zip(
                    melody.delay.stretch(tempo_factor).convert2absolute(), melody
                )
            )
            for melody in voices_main
        )

        delay_volume_pairs = functools.reduce(
            operator.add, delay_volume_pairs_per_voice
        )
        sorted_delay_volume_pairs = sorted(
            delay_volume_pairs, key=operator.itemgetter(1), reverse=True
        )

        change_positions = [0]
        for delay_volume_pair in sorted_delay_volume_pairs:
            if len(change_positions) - 1 == n_changes:
                break
            position = delay_volume_pair[0]
            if position not in change_positions:
                change_positions.append(position)

        change_positions = sorted(change_positions)

        sample_distributer_cycle = itertools.cycle(
            (
                # for one sample
                (CyclicPermutation((0,) * 6),),
                # for two samples
                (CyclicPermutation((0, 1) * 3), CyclicPermutation((0, 0, 1, 0, 1, 1))),
                # for three samples
                (
                    CyclicPermutation((0, 1, 2, 2, 1, 0)),
                    CyclicPermutation((0, 1, 2, 0, 1, 2)),
                ),
            )[n_samples - 1]
        )

        sample_distribution_per_change = tuple(
            next(next(sample_distributer_cycle)) for n in range(n_changes + 1)
        )
        sample_per_change_per_voice = tuple(
            tuple(samples[sample_idx] for sample_idx in voice)
            for voice in zip(*sample_distribution_per_change)
        )

        init_attributes = {}

        for voice_type, voices in enumerate((voices_main, voices_side)):
            for voice_idx, voice in enumerate(voices):

                absolute_voice_idx = (inner_voices, outer_voices)[voice_type][voice_idx]

                if absolute_voice_idx not in silent_channels:

                    sound_engine = radio.RadioEngine(
                        voice,
                        change_positions,
                        sample_per_change_per_voice[absolute_voice_idx],
                        make_envelope,
                        average_volume,
                        min_volume,
                        max_volume,
                        duration,
                        tempo_factor,
                        shadow_time,
                        crossfade_duration,
                        anticipation_time=anticipation_time,
                        overlaying_time=overlaying_time,
                        attack_duration=0.35,
                        release_duration=0.35,
                    )

                    voice_name = "natural_radio_{}".format(absolute_voice_idx)

                    init_attributes.update(
                        {
                            voice_name: {
                                "start": -anticipation_time,
                                "duration": duration,
                                "sound_engine": sound_engine,
                            }
                        }
                    )

        return init_attributes

    @staticmethod
    def make_weight_per_beat_for_one_bar(metrical_primes: tuple, size: int) -> tuple:
        def find_weight_per_beat(prime: int) -> tuple:
            weights = indispensability.indispensability_for_bar(
                tuple(prime_factors.factorise(prime))
            )
            maxima = max(weights)
            return tuple(w / maxima for w in weights)

        weight_per_beat = [0 for i in range(size)]
        for prime in metrical_primes:
            weights = find_weight_per_beat(prime)
            step_size = size // prime
            for step_position, weight in zip(range(0, size, step_size), weights):
                if weight_per_beat[step_position] < weight:
                    weight_per_beat[step_position] = weight

        return tuple(weight_per_beat)

    @staticmethod
    def convert_duration2factor(duration: float, bar_size: int) -> float:
        return duration / bar_size

    def _render_midi_diva(self, path: str) -> None:
        for v_idx, voice, volume_per_tone, diva_engine in zip(
            range(3),
            self.__counterpoint_result[1],
            self.__attribute_maker_outer.volume_per_tone_per_voice,
            self.__diva_engine_per_voice,
        ):
            voice = tuple(
                old.Tone(p, r, volume=v)
                for p, r, v in zip(*(tuple(voice) + (volume_per_tone,)))
            )
            diva_path = "{}/diva{}{}.mid".format(path, self.__gender_code, v_idx)
            diva_engine(voice, self.__tempo_factor).render(diva_path)

    def render(self, path: str) -> None:
        # make midi file render for DIVA
        self._render_midi_diva(path)

        # make usual sound file render
        super().render(path)


class Chord(ThreeVoiceCP):
    def __init__(self, name: str, chord: harmony.find_harmony(), **kwargs):
        def rhythm_maker(self) -> tuple:
            return tuple(
                binr.Compound.from_euclid(
                    metrical_prime * self._ThreeVoiceCP__n_bars, 1
                )
                for metrical_prime in self._ThreeVoiceCP__metrical_numbers
            )

        if "rhythm_maker" not in kwargs:
            kwargs.update({"rhythm_maker": rhythm_maker})

        super().__init__(name=name, start_harmony=chord, **kwargs)


class DensityBasedThreeVoiceCP(ThreeVoiceCP):
    def __init__(
        self,
        name: str,
        density_per_voice: tuple = (1.0, 1.0, 1.0),
        rhythmic_function: str = "barlow",
        curve_per_voice: tuple = ((0, 0.5, 0.5, 0), (0, 0.5, 0.5, 0), (0, 0.5, 0.5, 0)),
        distribution_function_for_first_attack_per_bar: infit.InfIt = infit.Cycle(
            ((0, 1), (0, 2), (1, 2))
        ),
        *args,
        **kwargs
    ):
        def rhythm_maker(self) -> tuple:
            n_bars = self._ThreeVoiceCP__n_bars
            # for first attack every voice should have a theoretical attack
            # (rests are explicitly controlled through the start_harmony argument)
            distribution_for_first_attack_per_bar = ((0, 1, 2),)
            distribution_for_first_attack_per_bar += tuple(
                next(distribution_function_for_first_attack_per_bar)
                for i in range(n_bars - 1)
            )
            rhythm_per_voice = []
            max_attacks_per_bar = min(self._ThreeVoiceCP__metrical_numbers)
            for voice_idx, metrical_prime, density, curve in zip(
                range(3),
                self._ThreeVoiceCP__metrical_numbers,
                density_per_voice,
                curve_per_voice,
            ):

                rhythm = []

                # if density between 0 and 1 understand as percentage
                # for density 1 only understand it as percentage if type is
                # float
                if (density >= 0 and density < 1) or (
                    density == 1 and type(density) is float
                ):
                    n_attacks_per_bar = int(density * max_attacks_per_bar)

                # else use it as an absolute number
                else:
                    assert density <= max_attacks_per_bar
                    n_attacks_per_bar = int(density)

                for (
                    distribution_for_first_attack
                ) in distribution_for_first_attack_per_bar:
                    has_first_attack = voice_idx in distribution_for_first_attack
                    n_attacks = n_attacks_per_bar + has_first_attack

                    if rhythmic_function is "euclid":
                        current_rhythm = tools.euclid(metrical_prime, n_attacks)

                    elif rhythmic_function is "barlow":
                        if metrical_prime == 10:
                            divided = (2, 5)
                        else:
                            divided = tuple(prime_factors.factorise(metrical_prime))

                        ranking = indispensability.bar_indispensability2indices(
                            indispensability.indispensability_for_bar(divided)
                        )
                        choosen_attacks = sorted(ranking[:n_attacks])
                        current_rhythm = tuple(
                            b - a
                            for a, b in zip(
                                choosen_attacks, choosen_attacks[1:] + [metrical_prime]
                            )
                        )

                    else:
                        msg = "Unknown rhythmic function {}.".format(rhythmic_function)
                        raise NotImplementedError(msg)

                    if not has_first_attack:
                        rhythm[-1] += current_rhythm[0]
                        current_rhythm = current_rhythm[1:]

                    rhythm.extend(current_rhythm)

                rhythm_per_voice.append(binr.Compound(rhythm))

            return tuple(rhythm_per_voice)

        def constraint_AP_remove_non_relevant_pitches(
            voice_idx: int, data: tuple
        ) -> tuple:
            pitches, rhythm, is_not_dissonant_pitch = data
            n_tones = len(pitches)

            curve = curve_per_voice[voice_idx]
            curve_summed = sum(curve)
            curve_percentage = tuple(item / curve_summed for item in curve)
            n_attacks_per_curve_part = tools.round_percentage(curve_percentage, n_tones)
            is_attack_allowed = list(
                functools.reduce(
                    operator.add,
                    tuple(
                        tools.not_fibonacci_transition(s0, s1, s2, s3)
                        for s0, s1, s2, s3 in (
                            n_attacks_per_curve_part[:2] + (0, 1),
                            n_attacks_per_curve_part[2:] + (1, 0),
                        )
                    ),
                )
            )

            is_attack_allowed[0] = 1

            pitches = tuple(
                p if is_allowed else mel.TheEmptyPitch
                for is_allowed, p in zip(is_attack_allowed, pitches)
            )

            return (pitches, rhythm, is_not_dissonant_pitch)

        if "rhythm_maker" not in kwargs:
            kwargs.update({"rhythm_maker": rhythm_maker})

        kwarg_name = "cp_constraints_interpolation"
        if kwarg_name in kwargs:
            new_constraints_AP = tuple(kwargs[kwarg_name]) + (
                constraint_AP_remove_non_relevant_pitches,
            )
            kwargs.update({kwarg_name: new_constraints_AP})
        else:
            kwargs.update({kwarg_name: (constraint_AP_remove_non_relevant_pitches,)})

        super().__init__(name=name, *args, **kwargs)
