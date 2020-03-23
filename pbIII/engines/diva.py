from mutools import synthesis

from mu.mel import ji
from mu.rhy import binr
from mu.sco import old

import pyo64 as pyo

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
