import itertools

from mutools import common_harmonics
from mutools import synthesis

from mu.sco import old
from mu.utils import tools

from pbIII.globals import globals


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
        attack_duration: float = 0.5,
        release_duration: float = 0.5,
    ) -> None:
        self.harmonic_melodies = self.make_melodies(
            voice0, voice1, n_voices, max_harmonic
        )

        self.__anticipation_time = anticipation_time
        self.__overlaying_time = overlaying_time
        self.__tempo_factor = tempo_factor
        self.__attack_duration = attack_duration
        self.__release_duration = release_duration
        self.__envelope_duration = attack_duration + release_duration
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
        envelope_line += r"{0}, 1, p3 - {0} - {1}, 1, {1}, 0".format(
            self.__attack_duration, self.__release_duration
        )
        out_line_sine = "out asig * aEnv * 0.3"
        out_line = "out asig * aEnv * 0.15"
        endin_line = r"endin"

        lines = [
            r"0dbfs=1",
            r"giSine ftgen 0, 0, 2^10, 10, 1",
            r"giSaw ftgen 0, 0, 2^10, 10, 1, 1/2, 1/3, 1/4, 1/5, 1/6, 1/7, 1/8, 1/9",
            r"giSquare ftgen 0, 0, 2^10, 10, 1, 0, 1/3, 0, 1/5, 0, 1/7, 0, 1/9",
            r"giTri ftgen 0, 0, 2^10, 10, 1, 0, -1/9, 0, 1/25, 0, -1/49, 0, 1/81",
        ]

        for instr_idx, ftable_name in enumerate(
            ("giSine", "giSaw", "giSquare", "giTri")
        ):
            lines.append("instr {}".format(instr_idx + 1))
            lines.append(r"asig poscil3 p5, p4, {}".format(ftable_name))
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
                    duration += self.__anticipation_time + self.__overlaying_time
                    if duration <= self.__envelope_duration:
                        duration = self.__envelope_duration + 0.01

                    line = "i{} {} {} {} {}".format(
                        next(instrument_number),
                        start_position,
                        duration,
                        pitch.freq * globals.CONCERT_PITCH,
                        volume,
                    )
                    lines.append(line)

        if not lines:
            lines.append("i1 0 {} 100 0".format(self.__duration))

        return "\n".join(lines)

    @property
    def cname(self) -> str:
        return ".glitter"
