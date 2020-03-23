import itertools

from mu.mel import ji
from mu.midiplug import midiplug
from mu.rhy import binr
from mu.rhy import indispensability
from mu.sco import old
from mu.utils import prime_factors

from mutools import MU
from mutools import polyrhythms
from mutools import pteqer

from pbIII.fragments import counterpoint
from pbIII.globals import globals

from pbIII.engines import diva
from pbIII.engines import glitter
from pbIII.engines import pteq


class Silence(MU.Segment):
    orchestration = globals.PBIII_ORCHESTRATION

    def __init__(self, name: str, duration: float):
        self.__duration = duration
        super().__init__(name, **{})

    @property
    def duration(self):
        return self.__duration


class ThreeVoiceCP(MU.Segment):
    orchestration = globals.PBIII_ORCHESTRATION

    # 7. natural radio hinzufügen
    # 8. stimmen hinzufügen
    # GUTES RHYTHMISCHES MODELL ÜBERLEGEN?
    # -> vielleicht dafür einfach mehrere verschiedene
    # subklassen machen, mit unterschiedlichen constraints
    # und unterschiedlichen techniken der rhythmus generierung
    # zB. EndChord, ...

    counterpoint_class = counterpoint.ThreeVoiceRhythmicCP

    def __init__(
        self,
        name: str,
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
        include_speech: bool = True,
    ) -> None:
        self.__n_bars = n_bars
        self.__gender_code = ("N", "P")[int(gender)]
        self.__bar_number = globals.MALE_SOIL.detect_group_index(group)
        self.__metrical_numbers = globals.MALE_SOIL.metre_per_vox_per_bar[
            self.__bar_number
        ]
        self.__anticipation_time = anticipation_time
        self.__overlaying_time = overlaying_time

        rhythms = polyrhythms.Polyrhythm(
            *tuple(
                binr.Compound.from_euclid(
                    metrical_prime * self.__n_bars, 7 * self.__n_bars
                )
                for metrical_prime in self.__metrical_numbers
            )
        ).transformed_rhythms

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
            rhythms, gender=gender, weight_per_beat=self.__weight_per_beat
        )
        self.__counterpoint_result = cp(
            *globals.MALE_SOIL.harmonic_primes_per_bar[self.__bar_number]
        )

        init_attributes = {}

        self.__duration_per_voice = duration_per_bar * self.__n_bars

        # make pianoteq voices
        if include_voices:
            init_attributes.update(self.make_voices())

        # make diva voices
        if include_diva:
            init_attributes.update(self.make_diva_voices())

        # make glitter voices
        if include_glitter:
            init_attributes.update(self.make_glitter_voices())

        # make natural radio voices
        if include_natural_radio:
            init_attributes.update(self.make_natural_radio())

        # make speech voices
        if include_speech:
            init_attributes.update(self.make_speech())

        super().__init__(name, **init_attributes)

    @property
    def duration(self) -> float:
        return super().duration - self.__overlaying_time

    def make_voices(self) -> dict:
        init_attributes = {}

        voices = tuple(
            old.Melody(old.Tone(p, r) for p, r in zip(vox[0], vox[1]))
            for vox in self.__counterpoint_result[0]
        )
        attribute_maker = pteqer.AttributeMaker(
            voices,
            metricity_per_beat=self.__weight_per_beat,
            max_spectrum_profile_change=10,
            dynamic_range=(0.35, 0.85),
        )
        for v_idx, voice, spectrum_profile_per_tone, volume_per_tone in zip(
            range(len(self.__counterpoint_result[0])),
            self.__counterpoint_result[0],
            attribute_maker.spectrum_profile_per_tone,
            attribute_maker.volume_per_tone_per_voice,
        ):
            sound_engine = pteq.PianoteqVoice(
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

    def make_glitter_voices(self) -> dict:
        init_attributes = {}
        voices = tuple(
            old.Melody(old.Tone(p, r) for p, r in zip(vox[0], vox[1]))
            for vox in self.__counterpoint_result[1]
        )
        glitter_duration = self.__duration_per_voice + self.__anticipation_time
        glitter_duration += self.__overlaying_time

        for combination in itertools.combinations(tuple(range(3)), 2):
            sound_engine = glitter.GlitterEngine(
                voices[combination[0]],
                voices[combination[1]],
                self.__tempo_factor,
                anticipation_time=self.__anticipation_time,
                overlaying_time=self.__overlaying_time,
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

    def make_natural_radio(self) -> dict:
        init_attributes = {}
        return init_attributes

    def make_speech(self) -> dict:
        init_attributes = {}
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

    def render(self, path: str) -> None:
        super().render(path)

        # make midi file render for DIVA
        for v_idx, voice in enumerate(self.__counterpoint_result[1]):
            diva_sequence = tuple(
                midiplug.DivaTone(
                    ji.JIPitch(pitch, multiply=globals.CONCERT_PITCH),
                    delay * self.__tempo_factor,
                    delay * self.__tempo_factor,
                )
                if pitch
                else old.Rest(delay * self.__tempo_factor)
                for pitch, delay in zip(*voice)
            )
            diva = midiplug.Diva(diva_sequence)
            diva.export("{}/diva{}{}.mid".format(path, self.__gender_code, v_idx))
