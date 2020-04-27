import subprocess

from mutools import pteqer
from mutools import synthesis

from mu.mel import mel
from mu.mel import ji
from mu.midiplug import midiplug
from mu.rhy import binr
from mu.sco import old
from mu.utils import infit
from mu.utils import interpolations
from mu.utils import tools

from pbIII.globals import globals


class __PianoteqVoice(synthesis.SoundEngine):
    glissando_duration = 0.5  # seconds

    def __init__(
        self,
        tempo_factor: float,
        pitches: tuple,
        rhythm: binr.Compound,
        is_not_dissonant_pitch_per_tone: tuple,
        dynamics: tuple,
        spectrum_profile_per_tone: tuple,
        overlaying_time: float = 0,
    ):

        self.__tempo_factor = tempo_factor
        self.__pitches = pitches
        self.__overlaying_time = overlaying_time
        self.__rhythm = rhythm
        self.__is_not_dissonant_pitch_per_tone = is_not_dissonant_pitch_per_tone
        self.__dynamics = dynamics
        self.__spectrum_profile_per_tone = spectrum_profile_per_tone

    def render(self, path: str) -> subprocess.Popen:
        adapted_rhythms = [rhythm * self.__tempo_factor for rhythm in self.__rhythm]
        adapted_rhythms[-1] += self.__overlaying_time

        melody = old.Melody(
            tuple(
                old.Tone(p, r, r, volume=v)
                for p, r, v in zip(self.__pitches, adapted_rhythms, self.__dynamics)
            )
        )

        if self.convert_dissonant_tones2glissandi:
            melody = self._convert_dissonant_tones2glissandi(melody)

        for modulator in self.modulator:
            melody = modulator(melody)

        sequence = []
        for tone, is_not_dissonant_pitch, spectrum_profile in zip(
            melody,
            self.__is_not_dissonant_pitch_per_tone,
            self.__spectrum_profile_per_tone,
        ):

            pitch, rhythm, volume, glissando = (
                tone.pitch,
                tone.delay,
                tone.volume,
                tone.glissando,
            )

            if pitch.is_empty:
                tone = pteqer.mk_empty_attack(
                    rhythm, next(self.empty_attack_dynamic_maker)
                )

            else:
                if is_not_dissonant_pitch:
                    parameters = self.parameter_non_dissonant_pitches

                else:
                    parameters = self.parameter_dissonant_pitches

                for par in parameters:
                    value = parameters[par]
                    if isinstance(value, infit.InfIt):
                        parameters[par] = next(value)
                    elif (
                        isinstance(value, float)
                        or isinstance(value, int)
                        or value is None
                    ):
                        parameters[par] = value
                    else:
                        msg = "Unknown value type: {}.".format(type(value))
                        raise TypeError(msg)

                if parameters["pinch_harmonic_pedal"] == 1:
                    if parameters["pinch_harmonic_pedal"]:
                        pitch -= ji.r(2, 1)

                tone = midiplug.PyteqTone(
                    ji.JIPitch(pitch, multiply=globals.CONCERT_PITCH),
                    rhythm,
                    rhythm,
                    volume=volume,
                    glissando=glissando,
                    spectrum_profile_3=spectrum_profile[0],
                    spectrum_profile_5=spectrum_profile[1],
                    spectrum_profile_6=spectrum_profile[0],
                    spectrum_profile_7=spectrum_profile[2],
                    **parameters,
                )

            sequence.append(tone)

        pteq = midiplug.Pianoteq(tuple(sequence))
        return pteq.export2wav(path, preset=self.preset, fxp=self.fxp)

    def _convert_dissonant_tones2glissandi(self, melody: old.Melody):
        consonant_tones_positions = tools.find_all_indices_of_n(
            True, self.__is_not_dissonant_pitch_per_tone
        )
        new_melody = melody[: consonant_tones_positions[0]].copy()

        consonant_and_its_dissonant_tones = tuple(
            (melody[idx0], melody[idx0 + 1 : idx1])
            for idx0, idx1 in zip(
                consonant_tones_positions,
                consonant_tones_positions[1:] + (len(melody),),
            )
        )

        for main_and_its_side_tones in consonant_and_its_dissonant_tones:
            main_tone, additional_tones = main_and_its_side_tones
            if not main_tone.pitch.is_empty:
                duration_per_pitch = (main_tone.duration,) + tuple(
                    t.duration for t in additional_tones
                )
                summed_duration = sum(duration_per_pitch)

                glissando = []
                for t0, t1 in zip(
                    (main_tone,) + tuple(additional_tones), additional_tones
                ):

                    pitch_difference = t0.pitch - main_tone.pitch
                    duration = t0.duration

                    if duration > self.glissando_duration:
                        staying = duration - self.glissando_duration
                        changing = self.glissando_duration
                    else:
                        staying = duration * 0.5
                        changing = float(staying)

                    glissando.append(old.PitchInterpolation(staying, pitch_difference))
                    glissando.append(old.PitchInterpolation(changing, pitch_difference))

                last_pitch = mel.TheEmptyPitch
                last_pitch_idx = -1
                while last_pitch.is_empty:
                    try:
                        last_pitch = additional_tones[last_pitch_idx].pitch
                    except IndexError:
                        last_pitch = None
                        break
                    last_pitch_idx -= 1

                if last_pitch is not None:
                    pitch_difference = last_pitch - main_tone.pitch
                    glissando.append(old.PitchInterpolation(0, pitch_difference))
                    glissando = old.GlissandoLine(
                        interpolations.InterpolationLine(glissando)
                    )
                else:
                    glissando = None

                print(glissando)

                new_tone = old.Tone(
                    main_tone.pitch,
                    delay=summed_duration,
                    duration=summed_duration,
                    glissando=glissando,
                )

                new_melody.append(new_tone)

            else:
                new_melody.extend((main_tone,) + tuple(additional_tones))

        return new_melody


# Functions for generating pianoteq voice classes
__STANDARD_PRESET = '"Concert Harp Daily"'
__STANDARD_FXP = None


def mk_pianoteq_engine(
    preset: str = __STANDARD_PRESET,
    fxp: str = __STANDARD_FXP,
    parameter_non_dissonant_pitches: dict = {},
    parameter_dissonant_pitches: dict = {},
    empty_attack_dynamic_maker: infit.InfIt = infit.Uniform(0.2, 0.4),
    modulator: tuple = tuple([]),
    convert_dissonant_tones2glissandi: bool = False,
) -> type:

    assert fxp is None or preset is None

    for parameter in midiplug.PyteqTone._init_args:

        if parameter not in (
            "spectrum_profile_3",
            "spectrum_profile_5",
            "spectrum_profile_6",
            "spectrum_profile_7",
        ):
            if parameter not in parameter_non_dissonant_pitches:
                parameter_non_dissonant_pitches.update({parameter: None})

            if parameter not in parameter_dissonant_pitches:
                parameter_dissonant_pitches.update({parameter: None})

    attributes = {
        "preset": preset,
        "fxp": fxp,
        "parameter_dissonant_pitches": parameter_dissonant_pitches,
        "parameter_non_dissonant_pitches": parameter_non_dissonant_pitches,
        "empty_attack_dynamic_maker": empty_attack_dynamic_maker,
        "modulator": modulator,
        "convert_dissonant_tones2glissandi": convert_dissonant_tones2glissandi,
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
            "impedance": infit.Uniform(2.5, 3),
            "cutoff": infit.Uniform(2.5, 3, seed=2),
            "q_factor": infit.Uniform(0.2, 0.4, seed=2),
            "direct_sound_duration": infit.Uniform(4, 5, seed=3),
            "string_length": infit.Uniform(8, 10),
            "sympathetic_resonance": infit.Uniform(2, 5),
            "hammer_noise": infit.Uniform(0.2, 1.0, seed=10),
            "sustain_pedal": 1,
            # "hammer_hard_piano": 0.4,
            "hammer_hard_piano": 0.5,
            # "hammer_hard_mezzo": 0.65,
            "hammer_hard_mezzo": 0.85,
            # "hammer_hard_forte": 0.885,
            "hammer_hard_forte": 1.15,
            "strike_point": infit.Uniform(1 / 64, 1 / 8),
            "pinch_harmonic_pedal": 0,
            "buff_stop_pedal": 0,
            "sound_speed": infit.Uniform(200, 500),
            "blooming_energy": infit.Uniform(1.55, 2),
            "blooming_inertia": infit.Uniform(1.55, 2.8),
        },
        parameter_dissonant_pitches={
            "impedance": infit.Uniform(2.2, 2.75),
            "cutoff": infit.Uniform(2, 2.5, seed=2),
            "q_factor": infit.Uniform(0.2, 1),
            "string_length": infit.Uniform(4, 7),
            "direct_sound_duration": infit.Uniform(2, 4, seed=3),
            # "hammer_hard_piano": 0.25,
            "hammer_hard_piano": 0.35,
            # "hammer_hard_mezzo": 0.525,
            "hammer_hard_mezzo": 0.625,
            # "hammer_hard_forte": 0.75,
            "hammer_hard_forte": 0.895,
            "sustain_pedal": 1,
            "sound_speed": infit.Uniform(200, 500),
            "sympathetic_resonance": infit.Uniform(1, 2),
            "pinch_harmonic_pedal": infit.Cycle((1, 0, 1)),
            "buff_stop_pedal": infit.Cycle((0, 1, 0, 1, 0)),
            "strike_point": infit.Uniform(1 / 64, 1 / 32),
            "hammer_noise": infit.Uniform(0.65, 1.25, seed=1000),
            "blooming_energy": 0,
        },
        *args,
        **kwargs,
    )


def mk_super_dreamy_pte(
    preset: str = __STANDARD_PRESET, fxp: str = __STANDARD_FXP, *args, **kwargs
) -> type:
    return mk_pianoteq_engine(
        preset=preset,
        fxp=fxp,
        parameter_non_dissonant_pitches={
            "impedance": infit.Uniform(2.5, 3),
            "cutoff": infit.Uniform(2.5, 3, seed=2),
            "q_factor": infit.Uniform(0.2, 0.4, seed=2),
            "direct_sound_duration": infit.Uniform(4, 5, seed=3),
            "string_length": infit.Uniform(8, 10),
            "sympathetic_resonance": infit.Uniform(2, 5),
            "hammer_noise": infit.Uniform(0.2, 1.0, seed=10),
            "sustain_pedal": 1,
            "hammer_hard_piano": 0.3,
            "hammer_hard_mezzo": 0.55,
            "hammer_hard_forte": 0.785,
            "strike_point": infit.Uniform(1 / 64, 1 / 8),
            "pinch_harmonic_pedal": 0,
            "buff_stop_pedal": 0,
            "sound_speed": infit.Uniform(200, 500),
            "blooming_energy": infit.Uniform(1.55, 2),
            "blooming_inertia": infit.Uniform(1.55, 2.8),
        },
        parameter_dissonant_pitches={
            "impedance": infit.Uniform(2.2, 2.75),
            "cutoff": infit.Uniform(2, 2.5, seed=2),
            "q_factor": infit.Uniform(0.2, 1),
            "string_length": infit.Uniform(4, 7),
            "direct_sound_duration": infit.Uniform(2, 4, seed=3),
            "hammer_hard_piano": 0.3,
            "hammer_hard_mezzo": 0.4,
            "hammer_hard_forte": 0.6,
            "sustain_pedal": 1,
            "sound_speed": infit.Uniform(200, 500),
            "sympathetic_resonance": infit.Uniform(1, 2),
            "pinch_harmonic_pedal": infit.Cycle((1, 0, 1)),
            "buff_stop_pedal": infit.Cycle((0, 1, 0, 1, 0)),
            "strike_point": infit.Uniform(1 / 64, 1 / 32),
            "hammer_noise": infit.Uniform(0.65, 1.25, seed=1000),
            "blooming_energy": 0,
        },
        *args,
        **kwargs,
    )
