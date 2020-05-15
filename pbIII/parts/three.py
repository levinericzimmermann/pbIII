from mutools import ambitus

from mu.mel import ji
from mu.utils import infit
from mu.utils import interpolations

from mutools import counterpoint
from mutools import ornamentations

from pbIII.engines import diva
from pbIII.engines import percussion
from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.fragments import tremolo

from pbIII.segments import segments

from pbIII.globals import globals


def make(name: str = "THREE", gender=False, group=0, sub_group0=2):
    return (
        segments.Chord(
            "{}_Bell0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(4, 1), ji.r(2, 1), ji.r(5, 4)),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="A", idx=0, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=5,
            start=-2,
            # start=0,
            dynamic_range_of_voices=(0.3, 0.4),
            voices_entry_delay_per_voice=(0.03, 0.07, 0.01),
            anticipation_time=4,
            overlaying_time=0,
            pteq_engine_per_voice=(
                pteq.mk_bright_bell(
                    fxp='"pbIII/fxp/GlockenspielHumanizednostretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
                pteq.mk_bright_bell(
                    fxp='"pbIII/fxp/GlockenspielHumanizednostretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
                pteq.mk_bright_bell(
                    fxp='"pbIII/fxp/GlockenspielHumanizednostretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
            ),
            speech_init_attributes={},
            volume_envelope_per_track={
                "glitterN01": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(2, 0),
                        interpolations.FloatInterpolationEvent(1, 0.5),
                        interpolations.FloatInterpolationEvent(4, 1.1),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                ),
                "glitterN02": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(2, 0),
                        interpolations.FloatInterpolationEvent(1, 0.5),
                        interpolations.FloatInterpolationEvent(4, 1),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                ),
                "glitterN12": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(2, 0),
                        interpolations.FloatInterpolationEvent(1, 0.5),
                        interpolations.FloatInterpolationEvent(4, 1),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                ),
            },
            glitter_type="drone",
            glitter_wave_form_per_voice=("square", "sine", "sine"),
            glitter_register_per_voice=(3, 4, 4),
            glitter_volume_per_voice=(3.85, 4.5, 4.5),
            glitter_modulater_per_voice=(None, None, None),
            glitter_release_duration=4,
            glitter_attack_duration=4,
            include_glitter=True,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
        ),
        segments.FreeStyleCP(
            "{}_0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(
                ji.r(2, 1), ji.r(12, 5), ji.r(9, 5)
            ),
            diva_engine_per_voice=(
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
            ),
            group=(group, sub_group0, 0),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            energy_per_voice=(9, 10, 9),
            silence_decider_per_voice=(
                infit.ActivityLevel(2),
                infit.ActivityLevel(3),
                infit.ActivityLevel(3),
            ),
            weight_range=(5, 10),
            decision_type="activity",
            gender=gender,
            n_bars=3,
            duration_per_bar=12.75,
            start=-5,
            dynamic_range_of_voices=(0.175, 0.55),
            anticipation_time=2,
            overlaying_time=1.25,
            cp_add_dissonant_pitches_to_nth_voice=(False, True, True),
            cp_constraints_interpolation=(
                counterpoint.constraints.AP_tremolo(
                    0,
                    add_tremolo_decider=infit.ActivityLevel(10),
                    only_on_non_dissonant_pitches=False,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, ((7, 12, 8, 15, 10, 8, 10),))
                    ),
                ),
                counterpoint.constraints.AP_tremolo(
                    1,
                    add_tremolo_decider=infit.ActivityLevel(8),
                    only_on_non_dissonant_pitches=True,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, ((7, 12, 8, 15, 10, 8, 10),))
                    ),
                ),
                counterpoint.constraints.AP_tremolo(
                    2,
                    add_tremolo_decider=infit.ActivityLevel(8),
                    only_on_non_dissonant_pitches=True,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, ((6, 9, 8, 12, 10, 8, 10, 13, 6, 4),))
                    ),
                ),
            ),
            volume_envelope_per_track={
                "voiceN0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(20, 1),
                        interpolations.FloatInterpolationEvent(0, 1),
                    ]
                )
            },
            glitter_include_dissonant_pitches=False,
            voices_overlaying_time=2,
            pteq_engine_per_voice=(
                pteq.mk_soft_leading_overdrive_harp_pte(
                    fxp='"pbIII/fxp/Harp_with_overdrive.fxp"',
                    preset=None,
                    sustain_pedal=1,
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                ),
                pteq.mk_super_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Uniform(0.15, 0.3),
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    convert_dissonant_tones2glissandi=True,
                ),
                pteq.mk_super_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Uniform(0.15, 0.3),
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    convert_dissonant_tones2glissandi=True,
                ),
            ),
            percussion_engine_per_voice=(
                percussion.Rhythmizer(
                    voice_meters2occupy=(0,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((1, 2, 0.25, 1)),
                                glissando_size=infit.Gaussian(0.8, 0.2),
                                glissando_offset=0,
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.1, 0.5),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1, 0.5)),
                                glissando_size=infit.Gaussian(0.9, 0.1),
                                glissando_offset=0,
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.2, 0.5),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_FAR_HAND
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_FAR_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((1, 0.25, 1, 0.5)),
                                glissando_size=infit.Gaussian(1.15, 0.2),
                                glissando_offset=0,
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.3, 0.5),
                            ),
                        )
                    ),
                    likelihood_range=(0.1, 0.7),
                    volume_range=(0.3, 0.45),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(1,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1, 0.5)),
                                distortion=infit.Uniform(0, 1),
                                glissando_size=infit.Gaussian(1.15, 0.1),
                                glissando_offset=0,
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.25, 0.5),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((1, 2, 0.25, 1)),
                                distortion=infit.Uniform(0, 0.5),
                                glissando_size=infit.Gaussian(0.9, 0.1),
                                glissando_offset=0,
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.25, 0.48),
                            ),
                        )
                    ),
                    likelihood_range=(0.1, 0.655),
                    volume_range=(0.45, 0.6),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(2,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_RADIO_ROEHRENRADIO_KEYS),
                                pitch_factor=infit.Uniform(1.4, 2.75),
                                distortion=infit.Uniform(0.3, 1),
                            ),
                        )
                    ),
                    likelihood_range=(0.08, 0.26),
                    volume_range=(0.54, 0.8),
                    ignore_beats_occupied_by_voice=False,
                    seed=39,
                ),
            ),
            speech_init_attributes={},
            glitter_modulater_per_voice=(None, None, None),
            glitter_attack_duration=infit.Gaussian(1.9, 0.3),
            glitter_release_duration=infit.Gaussian(2, 0.2),
            include_glitter=True,
            include_diva=True,
            include_natural_radio=True,
            include_percussion=True,
            # radio_silent_channels=(0, 2, 4),
            radio_samples=(
                globals.SAM_RADIO_ROEHRENRADIO_FAR_KURZWELLE[0],
                globals.SAM_RADIO_ROEHRENRADIO_CLOSE_KURZWELLE[0],
            ),
            radio_n_changes=3,
            radio_average_volume=0.34,
            radio_shadow_time=0.02,
            radio_min_volume=0.7,
            radio_attack_duration=infit.Gaussian(2, 0.1),
            radio_release_duration=infit.Gaussian(5.2, 0.2),
        ),
        segments.FreeStyleCP(
            "{}_1".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(
                ji.r(7, 4), ji.r(8, 3), ji.r(9, 7)
            ),
            diva_engine_per_voice=(
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
            ),
            group=(group, sub_group0, 1),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            energy_per_voice=(8.5, 5, 6),
            silence_decider_per_voice=(
                infit.ActivityLevel(1),
                infit.ActivityLevel(1),
                infit.ActivityLevel(1),
            ),
            weight_range=(0.5, 1),
            decision_type="random",
            random_seed=1000,
            gender=gender,
            n_bars=2,
            duration_per_bar=12.5,
            start=0.33,
            dynamic_range_of_voices=(0.185, 0.88),
            anticipation_time=1.5,
            overlaying_time=1.25,
            cp_add_dissonant_pitches_to_nth_voice=(False, True, True),
            cp_constraints_interpolation=(
                counterpoint.constraints.AP_tremolo(
                    0,
                    add_tremolo_decider=infit.ActivityLevel(10),
                    only_on_non_dissonant_pitches=False,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, ((7, 12, 8, 15, 10, 8, 10),))
                    ),
                ),
                counterpoint.constraints.AP_tremolo(
                    1,
                    add_tremolo_decider=infit.ActivityLevel(9),
                    only_on_non_dissonant_pitches=True,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, ((7, 12, 8, 15, 10, 8, 10),))
                    ),
                ),
                counterpoint.constraints.AP_tremolo(
                    2,
                    add_tremolo_decider=infit.ActivityLevel(9),
                    only_on_non_dissonant_pitches=True,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, ((6, 9, 8, 12, 10, 8, 10, 13, 6, 4),))
                    ),
                ),
            ),
            volume_envelope_per_track={
                "voiceN0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(20, 1),
                        interpolations.FloatInterpolationEvent(0, 1),
                    ]
                )
            },
            glitter_include_dissonant_pitches=False,
            voices_overlaying_time=2,
            pteq_engine_per_voice=(
                pteq.mk_soft_leading_overdrive_harp_pte(
                    fxp='"pbIII/fxp/Harp_with_overdrive.fxp"',
                    preset=None,
                    sustain_pedal=1,
                ),
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Uniform(0.15, 0.3),
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    convert_dissonant_tones2glissandi=True,
                ),
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Uniform(0.15, 0.3),
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    convert_dissonant_tones2glissandi=True,
                ),
            ),
            percussion_engine_per_voice=(
                percussion.Rhythmizer(
                    voice_meters2occupy=(0,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((1, 2, 0.25, 1)),
                                glissando_size=infit.Gaussian(0.8, 0.2),
                                glissando_offset=0,
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.1, 0.5),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1, 0.5)),
                                glissando_size=infit.Gaussian(0.9, 0.1),
                                glissando_offset=0,
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.2, 0.5),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_FAR_HAND
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_FAR_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((1, 0.25, 1, 0.5)),
                                glissando_size=infit.Gaussian(1.15, 0.2),
                                glissando_offset=0,
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.3, 0.5),
                            ),
                        )
                    ),
                    likelihood_range=(0.15, 0.9),
                    volume_range=(0.3, 0.45),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(1,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1, 0.5)),
                                distortion=infit.Uniform(0, 1),
                                glissando_size=infit.Gaussian(1.15, 0.1),
                                glissando_offset=0,
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.25, 0.5),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((1, 2, 0.25, 1)),
                                distortion=infit.Uniform(0, 0.5),
                                glissando_size=infit.Gaussian(0.9, 0.1),
                                glissando_offset=0,
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.25, 0.48),
                            ),
                        )
                    ),
                    likelihood_range=(0.15, 0.855),
                    volume_range=(0.45, 0.6),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(2,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_RADIO_ROEHRENRADIO_KEYS),
                                pitch_factor=infit.Uniform(1.4, 2.75),
                                distortion=infit.Uniform(0.3, 1),
                            ),
                        )
                    ),
                    likelihood_range=(0.08, 0.26),
                    volume_range=(0.54, 0.8),
                    ignore_beats_occupied_by_voice=False,
                    seed=39,
                ),
            ),
            speech_init_attributes={},
            glitter_modulater_per_voice=(None, None, None),
            glitter_attack_duration=infit.Gaussian(1.9, 0.3),
            glitter_release_duration=infit.Gaussian(2, 0.2),
            include_glitter=True,
            include_diva=True,
            include_natural_radio=True,
            include_percussion=True,
            # radio_silent_channels=(0, 2, 4),
            radio_samples=(
                globals.SAM_RADIO_ROEHRENRADIO_FAR_KURZWELLE[0],
                globals.SAM_RADIO_ROEHRENRADIO_CLOSE_KURZWELLE[0],
            ),
            radio_n_changes=5,
            radio_average_volume=0.4,
            radio_shadow_time=0.02,
            radio_min_volume=0.8,
            radio_attack_duration=infit.Gaussian(2, 0.1),
            radio_release_duration=infit.Gaussian(5.2, 0.2),
        ),
    )
