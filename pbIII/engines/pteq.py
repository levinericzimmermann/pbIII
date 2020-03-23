from mutools import pteqer
from mutools import synthesis

from mu.mel import ji
from mu.midiplug import midiplug
from mu.rhy import binr

from pbIII.globals import globals


class PianoteqVoice(synthesis.SoundEngine):
    def __init__(
        self,
        tempo_factor: float,
        pitches: tuple,
        rhythm: binr.Compound,
        is_not_dissonant_pitch_per_tone: tuple,
        dynamics: tuple,
        spectrum_profile_per_tone: tuple,
        preset: str = '"Concert Harp Daily"',
        fxp: str = None,
    ):
        self.__tempo_factor = tempo_factor
        self.__pitches = pitches
        self.__rhythm = rhythm
        self.__is_not_dissonant_pitch_per_tone = is_not_dissonant_pitch_per_tone
        self.__dynamics = dynamics
        self.__spectrum_profile_per_tone = spectrum_profile_per_tone
        self.__preset = preset
        self.__fxp = fxp

    def render(self, path: str) -> None:
        sequence = []
        for pitch, rhythm, is_not_dissonant_pitch, spectrum_profile, volume in zip(
            self.__pitches,
            self.__rhythm,
            self.__is_not_dissonant_pitch_per_tone,
            self.__spectrum_profile_per_tone,
            self.__dynamics,
        ):

            rhythm *= self.__tempo_factor

            if pitch.is_empty:
                tone = pteqer.mk_empty_attack(rhythm, 1)

            else:
                if True:
                    impedance = 2.15
                    cutoff = 2.5
                    q_factor = 0.2
                    string_length = 6
                    hammer_noise = 1
                    sustain_pedal = 0
                    hammer_hard_mezzo = 0.75
                    hammer_hard_forte = 1.5
                    hammer_hard_mezzo = 0.5
                    hammer_hard_forte = 1

                else:
                    impedance = 0.4
                    cutoff = 1
                    q_factor = 3.5
                    string_length = 1
                    hammer_noise = 3
                    sustain_pedal = 1
                    hammer_hard_mezzo = 1.2
                    hammer_hard_forte = 2
                    hammer_hard_mezzo = 1
                    hammer_hard_forte = 1.4

                tone = midiplug.PyteqTone(
                    ji.JIPitch(pitch, multiply=globals.CONCERT_PITCH),
                    rhythm,
                    rhythm,
                    volume=volume,
                    sustain_pedal=sustain_pedal,
                    hammer_noise=hammer_noise,
                    impedance=impedance,
                    cutoff=cutoff,
                    q_factor=q_factor,
                    string_length=string_length,
                    strike_point=1 / 8,
                    spectrum_profile_3=spectrum_profile[0],
                    spectrum_profile_5=spectrum_profile[1],
                    spectrum_profile_6=spectrum_profile[0],
                    spectrum_profile_7=spectrum_profile[2],
                    hammer_hard_mezzo=hammer_hard_mezzo,
                    hammer_hard_forte=hammer_hard_forte,
                )

            sequence.append(tone)

        pteq = midiplug.Pianoteq(tuple(sequence))
        pteq.export2wav(path, preset=self.__preset, fxp=self.__fxp)
