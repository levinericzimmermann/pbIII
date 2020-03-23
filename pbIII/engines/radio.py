from mutools import synthesis

from mu.sco import old
from mu.utils import interpolations


class RadioEngine(synthesis.BasedCsoundEngine):
    def __init__(
        self,
        voice: old.Melody,
        make_envelope: bool,
        min_volume: float,
        max_volume: float,
        duration: float,
        tempo_factor: float,
        shadow_time: float,
        crossfade_duration: float = 0.25,
        anticipation_time: float = 0,
        overlaying_time: float = 0,
        attack_duration: float = 0.5,
        release_duration: float = 0.5,
    ) -> None:

        assert max_volume > min_volume

        voice.delay = voice.delay.stretch(tempo_factor)
        voice.dur = voice.dur.stretch(tempo_factor)

        self.__duration = duration
        self.__envelope = self.mk_envelope(
            voice,
            shadow_time,
            duration,
            min_volume,
            max_volume,
            make_envelope,
            anticipation_time,
            overlaying_time,
        )
        self.__anticipation_time = anticipation_time
        self.__overlaying_time = overlaying_time
        self.__tempo_factor = tempo_factor
        self.__attack_duration = attack_duration
        self.__release_duration = release_duration
        self.__envelope_duration = attack_duration + release_duration
        self.__crossfade_duration = crossfade_duration

    @staticmethod
    def mk_envelope(
        voice: old.Melody,
        shadow_time: float,
        duration: float,
        min_volume: float,
        max_volume: float,
        make_envelope: bool,
        anticipation_time: float,
        overlaying_time: float,
    ) -> interpolations.InterpolationLine:
        volume_difference = max_volume - min_volume
        max_volume_of_melody = max(voice.volume)

        if make_envelope:
            events = tuple(
                (
                    float(tone.delay) + anticipation_time,
                    (tone.volume / max_volume_of_melody) * volume_difference,
                )
                for tone in voice.convert2absolute()
            )
            envelope = interpolations.ShadowInterpolationLine(
                min_volume, shadow_time, events, duration
            )

        else:
            envelope = interpolations.InterpolationLine(
                (
                    interpolations.FloatInterpolationEvent(duration, max_volume),
                    interpolations.FloatInterpolationEvent(0, max_volume),
                )
            )

        return envelope

    @property
    def cname(self) -> str:
        return ".radio"

    @property
    def orc(self) -> str:
        envelope_line = [r"gaEnv linseg"]
        for point in self.__envelope:
            envelope_line.append("{}".format(point.value))
            if point.delay != 0:
                envelope_line.append(", {},".format(point.delay))

        envelope_line = " ".join(envelope_line)

        endin_line = r"endin"

        lines = [
            r"0dbfs=1",
            r"instr 1",
            envelope_line,
            endin_line,
            r"instr 2",
            r"asig diskin2 p4, 1, 0, 0, 6, 4",
            r"aLocalEnv linseg 0, {0}, 1, p4 - {0} - {1}, 1, {1}, 0".format(
                self.__attack_duration, self.__release_duration
            ),
            r"out asig * aLocalEnv * gaEnv",
            endin_line,
        ]

        return "\n".join(lines)

    @property
    def sco(self) -> str:
        # TODO(make score, add instrument 2 calls with sample + crossover_time)

        lines = ["i1 0 {}".format(self.__duration)]

        return "\n".join(lines)
