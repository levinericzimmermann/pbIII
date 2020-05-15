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


def make(name: str = "TWO", gender=False, group=0, sub_group0=1):
    return (
        segments.Chord(
            "{}_Bell0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(2, 1), ji.r(2, 1), ji.r(5, 4)),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="A", idx=0, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=5,
            start=-3,
            # start=0,
            dynamic_range_of_voices=(0.6, 0.7),
            voices_entry_delay_per_voice=(0.03, 0.07, 0.01),
            anticipation_time=6,
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
                        interpolations.FloatInterpolationEvent(4, 0),
                        interpolations.FloatInterpolationEvent(2, 0.5),
                        interpolations.FloatInterpolationEvent(4, 1.1),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                ),
                "glitterN02": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(4, 0),
                        interpolations.FloatInterpolationEvent(2, 0.5),
                        interpolations.FloatInterpolationEvent(4, 1),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                ),
                "glitterN12": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(4, 0),
                        interpolations.FloatInterpolationEvent(2, 0.5),
                        interpolations.FloatInterpolationEvent(4, 1),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                ),
            },
            glitter_type="drone",
            glitter_wave_form_per_voice=("square", "saw", "square"),
            glitter_register_per_voice=(2, 3, 3),
            glitter_volume_per_voice=(3.85, 4.5, 4.5),
            glitter_modulater_per_voice=(None, None, None),
            glitter_release_duration=6,
            glitter_attack_duration=5,
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
            volume_envelope_per_track={
                "voiceN0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(4, 0.2),
                        interpolations.FloatInterpolationEvent(6, 1),
                        interpolations.FloatInterpolationEvent(2, 1),
                        interpolations.FloatInterpolationEvent(0, 0),
                    ]
                ),
                "voiceN1": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(2, 0.2),
                        interpolations.FloatInterpolationEvent(0, 1),
                    ]
                ),
                "voiceN2": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(3, 0.2),
                        interpolations.FloatInterpolationEvent(0, 1),
                    ]
                ),
                "glitterN01": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(2, 0),
                        interpolations.FloatInterpolationEvent(2, 0.5),
                        interpolations.FloatInterpolationEvent(5, 1),
                        interpolations.FloatInterpolationEvent(0, 0.2),
                    ]
                ),
                "glitterN02": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(2, 0),
                        interpolations.FloatInterpolationEvent(2, 0.5),
                        interpolations.FloatInterpolationEvent(5, 1),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                ),
                "glitterN12": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(2, 0),
                        interpolations.FloatInterpolationEvent(2, 0.5),
                        interpolations.FloatInterpolationEvent(5, 1),
                        interpolations.FloatInterpolationEvent(0, 0.2),
                    ]
                ),
            },
            diva_engine_per_voice=(
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
            ),
            group=(group, sub_group0, 0),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            energy_per_voice=(5, 10, 10),
            silence_decider_per_voice=(
                infit.ActivityLevel(6),
                infit.ActivityLevel(3),
                infit.ActivityLevel(3),
            ),
            weight_range=(6, 10),
            decision_type="activity",
            gender=gender,
            n_bars=2,
            duration_per_bar=14.5,
            start=-5,
            dynamic_range_of_voices=(0.1, 0.24),
            anticipation_time=5.5,
            overlaying_time=1.25,
            cp_add_dissonant_pitches_to_nth_voice=(False, True, True),
            cp_constraints_interpolation=(
                counterpoint.constraints.AP_tremolo(
                    0,
                    add_tremolo_decider=infit.ActivityLevel(10),
                    only_on_non_dissonant_pitches=False,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, (4, 11, 5, 6, 7, 4, 3, 4, 19))
                    ),
                ),
                counterpoint.constraints.AP_tremolo(
                    1,
                    add_tremolo_decider=infit.ActivityLevel(7),
                    only_on_non_dissonant_pitches=True,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, ((4, 3, 10, 5, 3, 7, 4, 11, 3, 9, 14),))
                    ),
                ),
                counterpoint.constraints.AP_tremolo(
                    2,
                    add_tremolo_decider=infit.ActivityLevel(6),
                    only_on_non_dissonant_pitches=True,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, ((7, 5, 8, 5, 6, 12, 8, 9, 10, 4),))
                    ),
                ),
            ),
            glitter_include_dissonant_pitches=False,
            voices_overlaying_time=1,
            pteq_engine_per_voice=(
                pteq.mk_super_soft_leading_pte(
                    modulator=(
                        ornamentations.SoftLineGlissandoMaker(
                            activity_lv=7,
                            minima_glissando_duration=0.05,
                            maxima_glissando_duration=0.1,
                            minima_glissando_size=20,
                            maxima_glissando_size=70,
                        ),
                    ),
                    empty_attack_dynamic_maker=infit.Value(0.2),
                    fxp='"pbIII/fxp/GlockenspielHumanizednostretching.fxp"',
                    preset=None,
                    sustain_pedal=0,
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
                    chord=infit.Cycle(
                        (
                            harmony.find_harmony(name="A", gender=gender),
                            harmony.find_harmony(name="C", gender=gender),
                        )
                    ),
                    sample_maker=infit.Cycle(
                        (
                            percussion.ResonanceSample(
                                path=infit.Cycle(globals.SAM_CYMBALS_BIG_AGGRESSIVE),
                                pitch_factor=infit.Uniform(2, 6),
                                resonance_filter_bandwidth=infit.Uniform(0.4, 2),
                                resonance_filter_octave=infit.Cycle((2, 4, 3, 4, 1, 2)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=infit.Uniform(0, 0.1),
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                            percussion.ResonanceSample(
                                path=infit.Cycle(globals.SAM_CYMBALS_MIDDLE_AGGRESSIVE),
                                pitch_factor=infit.Uniform(2, 5),
                                resonance_filter_bandwidth=infit.Uniform(0.5, 2),
                                resonance_filter_octave=infit.Cycle((2, 3, 4, 1, 2)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=infit.Uniform(0, 0.1),
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                        )
                    ),
                    likelihood_range=(0.3, 0.1),
                    volume_range=(0.1, 0.5),
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
                                distortion=infit.Uniform(0.7, 1.4),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((1, 0.25, 1)),
                                distortion=infit.Uniform(0.7, 1.3),
                            ),
                        )
                    ),
                    likelihood_range=(0.1, 0.325),
                    volume_range=(0.45, 0.64),
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
                    likelihood_range=(0.08, 0.54),
                    volume_range=(0.54, 0.8),
                    ignore_beats_occupied_by_voice=False,
                    seed=39,
                ),
            ),
            speech_init_attributes={},
            glitter_modulater_per_voice=("randomi", "randomh", "randomh"),
            glitter_attack_duration=infit.Gaussian(1.2, 0.3),
            glitter_release_duration=infit.Gaussian(1, 0.2),
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
            radio_average_volume=0.425,
            radio_shadow_time=0.04,
            radio_min_volume=0.725,
            radio_attack_duration=infit.Gaussian(1, 0.1),
            radio_release_duration=infit.Gaussian(5.2, 0.2),
        ),
        segments.Chord(
            "{}_CF_BELL_0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(7, 1), ji.r(2, 1), ji.r(4, 3)),
            group=(group, sub_group0, 1),
            chord=harmony.find_harmony(name="C", gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=8,
            start=-1.35,
            dynamic_range_of_voices=(0.4, 0.5),
            anticipation_time=2.25,
            overlaying_time=3.25,
            pteq_engine_per_voice=(
                pteq.mk_pianoteq_engine(
                    fxp='"pbIII/fxp/Bells_no_stretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
                pteq.mk_pianoteq_engine(
                    fxp='"pbIII/fxp/Bells_no_stretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
                pteq.mk_dreamy_pte(
                    fxp='"pbIII/fxp/Bells_no_stretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
            ),
            radio_samples=(
                globals.SAM_RADIO_ITALY[-1],
                globals.SAM_RADIO_BIELEFELD[-1],
            ),
            speech_init_attributes={},
            include_glitter=False,
            include_diva=False,
            include_natural_radio=True,
            include_percussion=False,
        ),
        segments.Chord(
            "{}_Bell1".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(2, 1), ji.r(2, 1), ji.r(5, 4)),
            group=(group, sub_group0, 1),
            chord=harmony.find_harmony(name="A", idx=0, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=5,
            start=-5,
            dynamic_range_of_voices=(0.44, 0.54),
            voices_entry_delay_per_voice=(0.03, 0.07, 0.01),
            anticipation_time=5,
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
                        interpolations.FloatInterpolationEvent(3, 0),
                        interpolations.FloatInterpolationEvent(2, 0.3),
                        interpolations.FloatInterpolationEvent(4, 1.1),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                ),
                "glitterN02": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(3, 0),
                        interpolations.FloatInterpolationEvent(2, 0.3),
                        interpolations.FloatInterpolationEvent(4, 1),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                ),
                "glitterN12": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(3, 0),
                        interpolations.FloatInterpolationEvent(2, 0.3),
                        interpolations.FloatInterpolationEvent(4, 1),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                ),
            },
            glitter_type="drone",
            glitter_wave_form_per_voice=("square", "saw", "square"),
            glitter_register_per_voice=(3, 3, 4),
            glitter_volume_per_voice=(3.65, 4.4, 4.4),
            glitter_modulater_per_voice=(None, None, None),
            glitter_release_duration=6,
            glitter_attack_duration=5,
            include_glitter=True,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
        ),
        segments.MelodicCP(
            "{}_1".format(name),
            volume_envelope_per_track={
                "voiceN0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(10, 2.1),
                        interpolations.FloatInterpolationEvent(0, 2.7),
                    ]
                ),
            },
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(2, 1), ji.r(3, 1), ji.r(5, 4)),
            random_seed=100,
            group=(group, sub_group0, 1),
            action_per_voice=(0.7, 0.73),
            sound_per_voice=(0.82, 0.87),
            phrases=(0,),
            melody_register=1,
            melodic_weight=0,
            weight_range=(0.3, 1),
            harmonicity_range=(0.25, 1),
            gender=gender,
            duration_per_bar=9.25,
            start=-5,
            dynamic_range_of_voices=(0.2, 0.35),
            anticipation_time=3,
            overlaying_time=2.2,
            voices_overlaying_time=3.5,
            glitter_attack_duration=infit.Gaussian(2.1, 0.15),
            glitter_release_duration=infit.Gaussian(1, 0.15),
            tremolo_maker_per_voice=(
                None,
                None,
                tremolo.TremoloMaker(
                    add_tremolo_decider=infit.ActivityLevel(6),
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Gaussian, (0.2675, 0.11))
                    ),
                    tremolo_volume_factor=0.48,
                ),
            ),
            pteq_engine_per_voice=(
                pteq.mk_super_soft_leading_pte(
                    empty_attack_dynamic_maker=infit.Value(0.3),
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    sustain_pedal=1,
                ),
                pteq.mk_dreamy_pte(
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    empty_attack_dynamic_maker=infit.Value(0.4),
                ),
                pteq.mk_super_soft_pte(
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    empty_attack_dynamic_maker=infit.Value(0.3),
                    fxp='"pbIII/fxp/GlockenspielHumanizednostretching.fxp"',
                    preset=None,
                    sustain_pedal=0,
                ),
            ),
            diva_engine_per_voice=(
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
            ),
            percussion_engine_per_voice=(),
            speech_init_attributes={},
            include_glitter=True,
            include_diva=False,
            include_natural_radio=True,
            include_percussion=False,
            radio_silent_channels=(0, 2, 4),
            radio_samples=(globals.SAM_RADIO_PROCESSED_DEGRADE[0],),
            radio_n_changes=2,
            radio_average_volume=0.08,
            radio_shadow_time=0.08,
            radio_min_volume=0.755,
        ),
        segments.MelodicCP(
            "{}_2".format(name),
            volume_envelope_per_track={
                "voiceN0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(13, 2.2),
                        interpolations.FloatInterpolationEvent(5, 2.75),
                        interpolations.FloatInterpolationEvent(0, 1),
                    ]
                ),
                "voiceN1": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(16.5, 1),
                        interpolations.FloatInterpolationEvent(5, 0.9),
                        interpolations.FloatInterpolationEvent(0, 0.335),
                    ]
                ),
                "voiceN2": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(17, 1),
                        interpolations.FloatInterpolationEvent(4, 0.9),
                        interpolations.FloatInterpolationEvent(0, 0.4),
                    ]
                ),
            },
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(3, 1), ji.r(3, 1), ji.r(5, 4)),
            random_seed=1,
            group=(group, sub_group0, 2),
            action_per_voice=(0.6, 0.63),
            sound_per_voice=(0.82, 0.87),
            phrases=(0,),
            melody_register=1,
            melodic_weight=0,
            weight_range=(0.3, 1),
            harmonicity_range=(0.25, 1),
            gender=gender,
            duration_per_bar=8.9,
            start=0.75,
            dynamic_range_of_voices=(0.24, 0.55),
            anticipation_time=2,
            overlaying_time=2.2,
            voices_overlaying_time=3.5,
            glitter_attack_duration=infit.Gaussian(1.9, 0.15),
            glitter_release_duration=infit.Gaussian(1, 0.15),
            tremolo_maker_per_voice=(
                None,
                tremolo.TremoloMaker(
                    add_tremolo_decider=infit.ActivityLevel(6),
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Gaussian, (0.2675, 0.11))
                    ),
                    tremolo_volume_factor=0.48,
                ),
                tremolo.TremoloMaker(
                    add_tremolo_decider=infit.ActivityLevel(6),
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Gaussian, (0.2675, 0.11))
                    ),
                    tremolo_volume_factor=0.48,
                ),
            ),
            pteq_engine_per_voice=(
                pteq.mk_super_soft_leading_pte(
                    empty_attack_dynamic_maker=infit.Value(0.3),
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    sustain_pedal=1,
                ),
                pteq.mk_dreamy_pte(
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    empty_attack_dynamic_maker=infit.Value(0.4),
                ),
                pteq.mk_super_soft_pte(
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    empty_attack_dynamic_maker=infit.Value(0.3),
                    fxp='"pbIII/fxp/GlockenspielHumanizednostretching.fxp"',
                    preset=None,
                    sustain_pedal=0,
                ),
            ),
            diva_engine_per_voice=(
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
            ),
            percussion_engine_per_voice=(),
            speech_init_attributes={},
            include_glitter=True,
            include_diva=False,
            include_natural_radio=True,
            include_percussion=False,
            radio_silent_channels=(0, 2, 4),
            radio_samples=(globals.SAM_RADIO_PROCESSED_DEGRADE[0],),
            radio_n_changes=2,
            radio_average_volume=0.1,
            radio_shadow_time=0.08,
            radio_min_volume=0.955,
        ),
        segments.Chord(
            "{}_Bell2".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(5, 1), ji.r(2, 1), ji.r(5, 4)),
            group=(group, sub_group0, 2),
            chord=harmony.find_harmony(name="A", idx=0, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=8,
            start=1,
            dynamic_range_of_voices=(0.34, 0.42),
            voices_entry_delay_per_voice=(0, 0.09, 0.05),
            anticipation_time=0,
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
            include_glitter=False,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
        ),
    )
