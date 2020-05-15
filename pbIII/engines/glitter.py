import itertools

from mutools import common_harmonics
from mutools import synthesis

from mu.sco import old
from mu.utils import infit
from mu.utils import tools

from pbIII.globals import globals

# STANDARD_MODULATOR = "pbIII/samples/speech/fisher/raw/"
# STANDARD_MODULATOR += "KodwoEshunFisherMemorialLectureMono.wav"


class GlitterEngine(synthesis.BasedCsoundEngine):
    def __init__(
        self,
        voice0: old.Melody,
        voice1: old.Melody,
        tempo_factor: float,
        anticipation_time: float = 0,
        overlaying_time: float = 0,
        n_voices: int = 5,
        max_harmonic: int = 32,
        attack_duration: infit.InfIt = infit.Value(0.5),
        release_duration: infit.InfIt = infit.Value(0.5),
        modulator: str = "randomi",
        # modulator: str = STANDARD_MODULATOR,
    ) -> None:
        self._modulator = modulator
        self.harmonic_melodies = self.make_melodies(
            voice0, voice1, n_voices, max_harmonic
        )

        if not isinstance(attack_duration, infit.InfIt):
            attack_duration = infit.Value(attack_duration)

        if not isinstance(release_duration, infit.InfIt):
            release_duration = infit.Value(release_duration)

        self.__anticipation_time = anticipation_time
        self.__overlaying_time = overlaying_time
        self.__tempo_factor = tempo_factor
        self.__attack_duration = attack_duration
        self.__release_duration = release_duration
        self.__duration = float(voice0.duration * tempo_factor)

    @staticmethod
    def make_melodies(
        voice0: old.Melody, voice1: old.Melody, n_voices: int, max_harmonic: int
    ) -> tuple:
        harmonic_melodies = common_harmonics.mk_harmonics_melodies(
            (voice0, voice1), n_voices=n_voices, max_harmonic=max_harmonic
        )[0]
        return harmonic_melodies

    @property
    def orc(self) -> str:
        envelope_line = r"aEnv linseg 0, "
        envelope_line += r"p6, 1, p3 - p6 - p7, 1, p7, 0"

        if self._modulator == "lfo":
            modulator_line = "kRandom randh 10, 30\n"
            modulator_line += r"aModulator lfo 1, kRandom + 3"

        elif self._modulator == "randomi":
            modulator_line = "kMetaModulator randomi 4, 20, 4\n"
            modulator_line += "aModulator randomi -1, 1, kMetaModulator"

        elif self._modulator == "randomh":
            modulator_line = "kMetaModulator randomi 4, 20, 4\n"
            modulator_line += "aModulator randomh -1, 1, kMetaModulator"

        elif self._modulator is None:
            modulator_line = "aModulator = 1"

        elif self._modulator[-4:] == r".wav":
            modulator_line = 'aModulator diskin2 "{}", 1, 0, 1, 6, 4'.format(
                self._modulator
            )

        else:
            msg = "Unknown modulator {}".format(self._modulator)
            raise NotImplementedError(msg)

        out_line_sine = "out asig * aEnv * 0.3 * p5"
        out_line = "out asig * aEnv * 0.15 * p5"
        endin_line = r"endin"

        lines = [
            r"0dbfs=1.25",
            r"giSine ftgen 0, 0, 2^10, 10, 1",
            r"giSaw ftgen 0, 0, 2^10, 10, 1, 1/2, 1/3, 1/4, 1/5, 1/6, 1/7, 1/8, 1/9",
            r"giSquare ftgen 0, 0, 2^10, 10, 1, 0, 1/3, 0, 1/5, 0, 1/7, 0, 1/9",
            r"giTri ftgen 0, 0, 2^10, 10, 1, 0, -1/9, 0, 1/25, 0, -1/49, 0, 1/81",
        ]

        for instr_idx, ftable_name in enumerate(
            ("giSine", "giSaw", "giSquare", "giTri")
        ):
            lines.append("instr {}".format(instr_idx + 1))
            lines.append(modulator_line)
            lines.append(
                r"asig poscil3 ((aModulator + 1) * 0.5), p4, {}".format(ftable_name)
            )
            lines.append(envelope_line)
            if instr_idx == 0:
                lines.append(out_line_sine)
            else:
                lines.append(out_line)
            lines.append(endin_line)

        return "\n".join(lines)

    @property
    def sco(self) -> str:
        lines = []

        instrument_number = itertools.cycle((1, 2, 1, 3, 1, 4, 1))
        for melody in self.harmonic_melodies:
            delay = tuple(float(dur) * self.__tempo_factor for dur in melody.delay)
            absolute_delay = tools.accumulate_from_zero(delay)
            for start_position, pitch, duration, volume in zip(
                absolute_delay, melody.pitch, delay, melody.volume
            ):

                if not pitch.is_empty:
                    attack_duration = next(self.__attack_duration)
                    release_duration = next(self.__release_duration)
                    envelope_duration = attack_duration + release_duration

                    duration += self.__anticipation_time + self.__overlaying_time
                    if duration <= envelope_duration:
                        duration = envelope_duration + 0.01

                    line = "i{} {} {} {} {} {} {}".format(
                        next(instrument_number),
                        start_position,
                        duration,
                        pitch.freq * globals.CONCERT_PITCH,
                        volume,
                        attack_duration,
                        release_duration,
                    )
                    lines.append(line)

        if not lines:
            lines.append("i1 0 {} 100 0".format(self.__duration))

        return "\n".join(lines)

    @property
    def cname(self) -> str:
        return ".glitter"


class SineDroneEngine(GlitterEngine):
    def __init__(
        self,
        freq: float,
        duration: float,
        anticipation_time: float = 0,
        overlaying_time: float = 0,
        attack_duration: float = 0.5,
        release_duration: float = 7,
        volume: float = 0.75,
        modulator: str = None,
        wave_form: str = "sine",
    ) -> None:
        self.__freq = freq
        self.__duration = duration + anticipation_time + overlaying_time
        self.__volume = volume
        self._modulator = modulator
        self.__anticipation_time = anticipation_time
        self.__overlaying_time = overlaying_time
        self.__attack_duration = attack_duration
        self.__release_duration = release_duration
        self.__envelope_duration = attack_duration + release_duration
        self.__instrument_number = {"sine": 1, "saw": 2, "square": 3, "tri": 4}[
            wave_form
        ]

    @property
    def cname(self) -> str:
        return ".glitter_drone"

    @property
    def sco(self) -> str:
        duration = self.__duration
        if duration <= self.__envelope_duration:
            duration = self.__envelope_duration + 0.01

        lines = (
            "i{} {} {} {} {} {} {}".format(
                self.__instrument_number,
                0,
                duration,
                self.__freq,
                self.__volume,
                self.__attack_duration,
                self.__release_duration,
            ),
        )
        return "\n".join(lines)
