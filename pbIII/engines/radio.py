import pyo

from mutools import synthesis

from mu.sco import old
from mu.utils import infit
from mu.utils import interpolations

from mu.rhy import rhy


class RadioEngine(synthesis.BasedCsoundEngine):
    def __init__(
        self,
        voice: old.Melody,
        new_sample_positions: tuple,
        sample_per_change: tuple,
        make_envelope: bool,
        average_volume: float,
        min_volume: float,
        max_volume: float,
        duration: float,
        tempo_factor: float,
        shadow_time: float,
        crossfade_duration: float = 0.25,
        anticipation_time: float = 0,
        overlaying_time: float = 0,
        attack_duration: infit.InfIt = infit.Value(0.5),
        release_duration: infit.InfIt = infit.Value(0.5),
        random_seed: int = 100,
    ) -> None:

        assert max_volume > min_volume
        assert min_volume > average_volume

        if not isinstance(attack_duration, infit.InfIt):
            attack_duration = infit.Value(attack_duration)

        if not isinstance(release_duration, infit.InfIt):
            release_duration = infit.Value(release_duration)

        import random as random_module

        random_module.seed(random_seed)

        self.__random_module = random_module

        voice.delay = rhy.Compound(voice.delay).stretch(tempo_factor)
        voice.dur = rhy.Compound(voice.dur).stretch(tempo_factor)

        self.__sndinfo_per_sample = {
            sample: pyo.sndinfo(sample) for sample in set(sample_per_change)
        }
        self.__n_channels_per_sample = {
            sample: self.__sndinfo_per_sample[sample][3]
            for sample in self.__sndinfo_per_sample
        }
        self.__duration_per_sample = {
            sample: self.__sndinfo_per_sample[sample][1]
            for sample in self.__sndinfo_per_sample
        }
        self.__new_sample_positions = new_sample_positions
        self.__sample_per_change = sample_per_change
        self.__duration = duration
        self.__envelope = self.mk_envelope(
            voice,
            shadow_time,
            duration,
            average_volume,
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
        self.__crossfade_duration = crossfade_duration
        self.__halved_crossfade_duration = crossfade_duration * 0.5

    @staticmethod
    def mk_envelope(
        voice: old.Melody,
        shadow_time: float,
        duration: float,
        average_volume: float,
        min_volume: float,
        max_volume: float,
        make_envelope: bool,
        anticipation_time: float,
        overlaying_time: float,
    ) -> interpolations.InterpolationLine:

        volume_difference = max_volume - min_volume
        max_volume_of_melody = max(voice.volume)

        def detect_volume(tone_volume: float) -> float:
            percentage = tone_volume / max_volume_of_melody
            return (percentage * volume_difference) + min_volume

        if make_envelope:
            events = tuple(
                (float(tone.delay) + anticipation_time, detect_volume(tone.volume))
                for tone in voice.convert2absolute()
            )
            envelope = interpolations.ShadowInterpolationLine(
                average_volume, shadow_time, events, duration
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
        def mk_instr(number: int, n_channels: int) -> list:
            signal_names = tuple("aSig{}".format(idx) for idx in range(n_channels))
            input_line = ", ".join(signal_names)
            input_line = "{} diskin2 p4, 1, p5, p6, 6, 4".format(input_line)
            summarize_line = " + ".join(signal_names)
            summarize_line = "asig = ({}) / {}".format(summarize_line, n_channels)
            return [
                r"instr {}".format(number),
                input_line,
                summarize_line,
                r"aLocalEnv linseg 0, p7, 1, p3 - p7 - p8, 1, p8, 0",
                r"out asig * aLocalEnv * gaEnv",
                endin_line,
            ]

        envelope_line = [r"gaEnv linseg"]
        for point in self.__envelope:
            envelope_line.append("{}".format(point.value))
            if point.delay != 0:
                envelope_line.append(", {},".format(point.delay))

        envelope_line = " ".join(envelope_line)
        endin_line = r"endin"

        lines = [r"0dbfs=1", r"instr 1", envelope_line, endin_line]

        for n_channels in range(2):
            lines.extend(mk_instr(n_channels + 2, n_channels + 1))

        return "\n".join(lines)

    @property
    def sco(self) -> str:
        lines = ["i1 0 {}".format(self.__duration)]

        duration_per_sample = [
            (b - a)
            for a, b in zip(
                self.__new_sample_positions,
                self.__new_sample_positions[1:] + [self.__duration],
            )
        ]

        duration_per_sample[-1] -= self.__halved_crossfade_duration

        for sample, duration, start_position in zip(
            self.__sample_per_change, duration_per_sample, self.__new_sample_positions
        ):
            duration += self.__crossfade_duration
            duration += self.__anticipation_time
            duration += self.__overlaying_time

            diff = start_position - self.__halved_crossfade_duration
            if diff <= 0:
                start_position = 0
                duration += diff
            else:
                start_position = diff

            attack_duration = next(self.__attack_duration)
            release_duration = next(self.__release_duration)
            envelope_duration = attack_duration + release_duration

            if duration < envelope_duration:
                duration = envelope_duration + 0.005

            sample_duration = self.__duration_per_sample[sample]

            if sample_duration < duration:
                skip_time = self.__random_module.uniform(0, duration - sample_duration)
                wrap = 0

            else:
                # TODO(does this potentially create clicks? when looping
                # through the file and there isn't any particular envelope for
                # this case?)
                skip_time = 0
                wrap = 1

            if self.__n_channels_per_sample[sample] == 1:
                instr_number = 2
            elif self.__n_channels_per_sample[sample] == 2:
                instr_number = 3
            else:
                raise NotImplementedError()

            lines.append(
                'i{} {} {} "{}" {} {} {} {}'.format(
                    instr_number,
                    start_position,
                    duration,
                    sample,
                    skip_time,
                    wrap,
                    attack_duration,
                    release_duration,
                )
            )

        return "\n".join(lines)
