from mutools import pteqer
from mutools import synthesis

from mu.mel import ji
from mu.midiplug import midiplug
from mu.rhy import binr
from mu.utils import infit

from pbIII.globals import globals


class __PianoteqVoice(synthesis.SoundEngine):
    def __init__(
        self,
        tempo_factor: float,
        pitches: tuple,
        rhythm: binr.Compound,
        is_not_dissonant_pitch_per_tone: tuple,
        dynamics: tuple,
        spectrum_profile_per_tone: tuple,
    ):

        self.__tempo_factor = tempo_factor
        self.__pitches = pitches
        self.__rhythm = rhythm
        self.__is_not_dissonant_pitch_per_tone = is_not_dissonant_pitch_per_tone
        self.__dynamics = dynamics
        self.__spectrum_profile_per_tone = spectrum_profile_per_tone

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
                tone = pteqer.mk_empty_attack(rhythm, 0.4)

            else:
                if is_not_dissonant_pitch:
                    parameters = self.parameter_non_dissonant_pitches

                else:
                    parameters = self.parameter_dissonant_pitches

                for par in parameters:
                    value = parameters[par]
                    if isinstance(value, infit.InfIt):
                        parameters[par] = next(value)
                    elif isinstance(value, float) or isinstance(value, int):
                        parameters[par] = value
                    else:
                        msg = "Unknown value type: {}.".format(type(value))
                        raise TypeError(msg)

                tone = midiplug.PyteqTone(
                    ji.JIPitch(pitch, multiply=globals.CONCERT_PITCH),
                    rhythm,
                    rhythm,
                    volume=volume,
                    spectrum_profile_3=spectrum_profile[0],
                    spectrum_profile_5=spectrum_profile[1],
                    spectrum_profile_6=spectrum_profile[0],
                    spectrum_profile_7=spectrum_profile[2],
                    **parameters,
                )

            sequence.append(tone)

        pteq = midiplug.Pianoteq(tuple(sequence))
        pteq.export2wav(path, preset=self.preset, fxp=self.fxp)


__USED_PIANOTEQ_PARAMETER = {
    "impedance": 2,
    "cutoff": 1.5,
    "q_factor": 1,
    "string_length": 3,
    "hammer_noise": 1,
    "sustain_pedal": 1,
    "hammer_hard_piano": 0.5,
    "hammer_hard_mezzo": 0.75,
    "hammer_hard_forte": 1.5,
    "strike_point": 1 / 8,
}


# Functions for generating pianoteq voice classes
__STANDARD_PRESET = '"Concert Harp Daily"'
__STANDARD_FXP = None


def mk_pianoteq_engine(
    preset: str = __STANDARD_PRESET,
    fxp: str = __STANDARD_FXP,
    parameter_non_dissonant_pitches: dict = {},
    parameter_dissonant_pitches: dict = {},
) -> type:

    assert fxp is None or preset is None

    for parameter in __USED_PIANOTEQ_PARAMETER:
        if parameter not in parameter_non_dissonant_pitches:
            parameter_non_dissonant_pitches.update(
                {parameter: __USED_PIANOTEQ_PARAMETER[parameter]}
            )

        if parameter not in parameter_dissonant_pitches:
            parameter_dissonant_pitches.update(
                {parameter: __USED_PIANOTEQ_PARAMETER[parameter]}
            )

    attributes = {
        "preset": preset,
        "fxp": fxp,
        "parameter_dissonant_pitches": parameter_dissonant_pitches,
        "parameter_non_dissonant_pitches": parameter_non_dissonant_pitches,
    }
    return type("PianoteqVoice", (__PianoteqVoice,), attributes)


def mk_contrasting_pte(
    preset: str = __STANDARD_PRESET, fxp: str = __STANDARD_FXP, *args, **kwargs
) -> type:
    return mk_pianoteq_engine(
        preset=preset,
        fxp=fxp,
        parameter_non_dissonant_pitches={
            "impedance": 2.15,
            "cutoff": 2.5,
            "q_factor": 0.2,
            "string_length": 6,
            "hammer_noise": 1,
            "sustain_pedal": 1,
            "hammer_hard_piano": 0.5,
            "hammer_hard_mezzo": 0.75,
            "hammer_hard_forte": 1.5,
            "strike_point": 1 / 8,
        },
        parameter_dissonant_pitches={
            "impedance": 0.4,
            "cutoff": 0.8,
            "q_factor": 3.5,
            "string_length": 1,
            "hammer_noise": 3,
            "sustain_pedal": 1,
            "hammer_hard_piano": 0.8,
            "hammer_hard_mezzo": 1.3,
            "hammer_hard_forte": 2,
            "strike_point": 1 / 8,
        },
        *args,
        **kwargs,
    )


def mk_dreamy_pte(
    preset: str = __STANDARD_PRESET, fxp: str = __STANDARD_FXP, *args, **kwargs
) -> type:
    return mk_pianoteq_engine(
        preset=preset,
        fxp=fxp,
        parameter_non_dissonant_pitches={
            "impedance": 3,
            "cutoff": 2.7,
            "q_factor": 0.2,
            "string_length": 9,
            "hammer_noise": 1,
            "sustain_pedal": 1,
            "hammer_hard_piano": 0.4,
            "hammer_hard_mezzo": 0.7,
            "hammer_hard_forte": 1,
            "strike_point": 1 / 8,
        },
        parameter_dissonant_pitches={
            "hammer_hard_piano": 0.3,
            "hammer_hard_mezzo": 0.5,
            "hammer_hard_forte": 0.7,
        },
        *args,
        **kwargs,
    )
