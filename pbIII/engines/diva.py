from mutools import synthesis

from mu.mel import ji
from mu.rhy import binr
from mu.sco import old
from mu.utils import infit
from mu.utils import interpolations

from mu.midiplug import midiplug

import pyo64 as pyo

import numbers

from pbIII.globals import globals


class DivaSimulation(synthesis.SineMelodyEngine):
    def __init__(
        self,
        tempo_factor: float,
        pitches: tuple,
        rhythm: binr.Compound,
        discard_rests: bool = True,
    ):
        self.__tempo_factor = tempo_factor
        self.__pitches = pitches
        self.__rhythm = rhythm

        melody = old.Melody(
            old.Tone(ji.JIPitch(p, multiply=globals.CONCERT_PITCH), r * tempo_factor)
            if not p.is_empty
            else old.Rest(r * tempo_factor)
            for p, r in zip(pitches, rhythm)
        )
        if discard_rests:
            melody = melody.discard_rests()
        super().__init__(melody, attack=0.08, decay=0.05, release=0.25)

    def copy(self) -> "DivaSimulation":
        return type(self)(self.__tempo_factor, self.__pitches, self.__rhythm)

    @property
    def instrument(self) -> pyo.EventInstrument:
        class PhasorPlayer(pyo.EventInstrument):
            def __init__(self, **args) -> None:
                pyo.EventInstrument.__init__(self, **args)
                self.osc = pyo.Phasor(freq=self.freq, mul=self.env).play(dur=self.dur)
                self.filter = pyo.Reson(self.osc, self.freq, q=5).out(dur=self.dur)
                self.reverb = pyo.Freeverb(
                    0.5 * self.filter, size=[0.79, 0.8], damp=0.9, bal=0.3
                ).out(dur=self.dur + 4)

        return PhasorPlayer


class DivaMidiEngine(synthesis.SoundEngine):
    def __init__(self, voice: tuple, tempo_factor: float, **kwargs):
        self.__init_arguments = self.make_init_arguments()
        self.__diva_sequence = self.make_diva_sequence(voice, tempo_factor)

    @property
    def _init_arguments(self) -> dict:
        """define class specfic data here when inherting"""
        return {}

    @property
    def init_arguments(self) -> dict:
        return self.__init_arguments

    def make_init_arguments(self) -> dict:
        init_args = self._init_arguments
        for arg in midiplug.DivaTone._init_args:
            if arg not in init_args:
                init_args[arg] = infit.Value(None)
            else:
                value = init_args[arg]

                if not isinstance(value, infit.InfIt):
                    if isinstance(value, numbers.Real) or isinstance(
                        value, interpolations.InterpolationLine
                    ):
                        init_args[arg] = infit.Value(value)
                    else:
                        msg = "Unknown type '{}' for argument '{}'".format(
                            type(value), arg
                        )
                        msg += " with value '{}'.".format(value)
                        raise NotImplementedError(msg)

        return init_args

    def make_diva_sequence(self, voice: tuple, tempo_factor: float) -> tuple:
        diva_sequence = []

        for tone in voice:
            delay = tone.delay * tempo_factor

            if tone.pitch.is_empty:
                dt = old.Rest(delay)

            else:
                div_synth_args = {
                    arg: next(self.init_arguments[arg]) for arg in self.init_arguments
                }
                dt = midiplug.DivaTone(
                    ji.JIPitch(tone.pitch, multiply=globals.CONCERT_PITCH),
                    delay,
                    delay,
                    volume=tone.volume,
                    **div_synth_args
                )

            diva_sequence.append(dt)

        return tuple(diva_sequence)

    def render(self, path: str) -> None:
        """Only generate midi file and not wav file!"""

        diva = midiplug.Diva(self.__diva_sequence)
        diva.export(path)


class FloatingDivaMidiEngine(DivaMidiEngine):
    @property
    def _init_arguments(self) -> dict:
        """define class specfic data here when inherting"""
        return {
            "volume_curve": infit.Cycle(
                (
                    interpolations.Rising(),
                    interpolations.FallingRising(),
                    interpolations.Falling(),
                    interpolations.RisingFalling(),
                )
            ),
            "osc_noise_volume": infit.Uniform(0, 25),
            "osc_mix": infit.Value(infit.Gaussian(50, 25)),
            "osc_tune_mod_depth2": infit.Cycle(
                (
                    interpolations.Rising(0, 2),
                    interpolations.Falling(-2, 2),
                    infit.Gaussian(0, 1.5),
                    interpolations.RisingFalling(-2, 2),
                    interpolations.Falling(0, 2),
                    0,
                    interpolations.Rising(0, 1),
                    infit.Uniform(-1, 1),
                    interpolations.RisingFalling(-1, 1.5),
                    interpolations.Falling(-2, -1),
                    interpolations.Rising(-1, 0),
                    0,
                    infit.Gaussian(0, 2),
                )
            ),
            "vcf1_freq_mod_depth": infit.Uniform(0, 30),
            "vcf1_filter_fm": infit.Cycle(
                (
                    0,
                    interpolations.Rising(0, 10),
                    interpolations.FallingRising(-10, 10),
                    interpolations.Falling(0, 10),
                    0,
                    interpolations.RisingFalling(0, 10),
                    interpolations.Falling(-10, 0),
                    interpolations.Rising(-10, 0),
                )
            ),
        }
