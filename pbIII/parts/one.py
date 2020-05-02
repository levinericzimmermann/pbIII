from mutools import ambitus

from mu.mel import ji
from mu.utils import infit

from mutools import counterpoint
from mutools import ornamentations

from pbIII.engines import percussion
from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.segments import segments

from pbIII.globals import globals


def make(name: str = "ONE", gender=True, group=0, sub_group0=0):
    return (
        segments.FreeStyleCP(
            "{}_0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(
                ji.r(4, 1), ji.r(12, 5), ji.r(9, 4)
            ),
            group=(group, sub_group0, 0),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            energy_per_voice=(5.7, 9, 9),
            weight_range=(0.35, 1),
            decision_type="random",
            gender=gender,
            n_bars=2,
            duration_per_bar=11,
            start=0,
            dynamic_range_of_voices=(0.2, 0.6),
            anticipation_time=2.75,
            overlaying_time=3.25,
            cp_add_dissonant_pitches_to_nth_voice=(False, False, False),
            cp_constraints_interpolation=[],
            glitter_include_dissonant_pitches=False,
            pteq_engine_per_voice=(
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0),
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    # convert_dissonant_tones2glissandi=True,
                ),
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0),
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    # convert_dissonant_tones2glissandi=True,
                ),
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0),
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    # convert_dissonant_tones2glissandi=True,
                ),
            ),
            speech_init_attributes={},
            include_glitter=True,
            include_diva=False,
            include_natural_radio=True,
            include_percussion=False,
            radio_silent_channels=(1, 3, 5),
            radio_samples=(
                "pbIII/samples/radio/carolina/3.wav",
                "pbIII/samples/radio/carolina/1.wav",
            ),
            radio_n_changes=1,
            radio_average_volume=0.385,
            radio_shadow_time=0.2,
            radio_min_volume=0.925,
        ),
        segments.DensityBasedThreeVoiceCP(
            "{}_1".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(
                ji.r(16, 5), ji.r(5, 2), ji.r(8, 5)
            ),
            group=(group, sub_group0, 1),
            start_harmony=harmony.find_harmony("A", True, 0, (0,), gender=gender),
            density_per_voice=(0, 0.6, 0.6),
            gender=gender,
            n_bars=1,
            duration_per_bar=10,
            start=1.25,
            dynamic_range_of_voices=(0.15, 0.45),
            anticipation_time=1.5,
            overlaying_time=1.5,
            cp_constraints_harmonic=(
                counterpoint.constraints.HR_forbid_too_empty_harmonies(1, [0]),
            ),
            cp_constraints_interpolation=[],
            # cp_add_dissonant_pitches_to_nth_voice=(False, False, False),
            cp_add_dissonant_pitches_to_nth_voice=(True, True, True),
            pteq_engine_per_voice=(
                pteq.mk_super_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0),
                    modulator=(
                        ornamentations.SoftLineGlissandoMaker(
                            maxima_glissando_duration=0.35, maxima_glissando_size=180
                        ),
                    ),
                    convert_dissonant_tones2glissandi=True,
                ),
                pteq.mk_super_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0),
                    modulator=(
                        ornamentations.SoftLineGlissandoMaker(
                            maxima_glissando_duration=0.35, maxima_glissando_size=180
                        ),
                    ),
                    convert_dissonant_tones2glissandi=True,
                ),
                pteq.mk_super_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0),
                    modulator=(
                        ornamentations.SoftLineGlissandoMaker(
                            maxima_glissando_duration=0.35, maxima_glissando_size=180
                        ),
                    ),
                    convert_dissonant_tones2glissandi=True,
                ),
            ),
            speech_init_attributes={},
            include_glitter=True,
            include_diva=False,
            include_natural_radio=True,
            include_percussion=False,
            radio_silent_channels=(1, 3, 5),
            radio_samples=(
                "pbIII/samples/radio/carolina/3.wav",
                "pbIII/samples/radio/carolina/1.wav",
            ),
            radio_n_changes=0,
            radio_average_volume=0.2,
            radio_shadow_time=0.175,
            radio_min_volume=0.875,
            glitter_include_dissonant_pitches=False,
        ),
        segments.DensityBasedThreeVoiceCP(
            "{}_2".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(6, 1), ji.r(5, 2), ji.r(9, 4)),
            group=(group, sub_group0, 2),
            start_harmony=harmony.find_harmony("A", True, 0, (0,), gender=gender),
            density_per_voice=(0.775, 1, 1),
            gender=gender,
            n_bars=3,
            duration_per_bar=7,
            start=4.5,
            dynamic_range_of_voices=(0.1, 0.2),
            anticipation_time=1.25,
            overlaying_time=1.25,
            cp_add_dissonant_pitches_to_nth_voice=(False, False, True),
            cp_constraints_harmonic=(
                counterpoint.constraints.HR_forbid_too_empty_harmonies(1, [0]),
            ),
            cp_constraints_interpolation=[],
            glitter_include_dissonant_pitches=False,
            pteq_engine_per_voice=(
                pteq.mk_dreamy_pte(
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0),
                    modulator=(
                        ornamentations.SoftLineGlissandoMaker(
                            maxima_glissando_duration=0.35, maxima_glissando_size=180
                        ),
                    ),
                ),
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0),
                    modulator=(
                        ornamentations.SoftLineGlissandoMaker(
                            maxima_glissando_duration=0.35, maxima_glissando_size=180
                        ),
                    ),
                ),
            ),
            speech_init_attributes={},
            include_glitter=True,
            include_diva=False,
            include_natural_radio=True,
            include_percussion=True,
            percussion_engine_per_voice=(
                percussion.Rhythmizer(
                    voice_meters2occupy=(0, 1, 2),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_CYMBALS_BIG_CLOSE),
                                pitch_factor=infit.Uniform(0.5, 2),
                                distortion=infit.Uniform(0.05, 0.3),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_CYMBALS_MIDDLE_CLOSE_LOUD),
                                pitch_factor=infit.Uniform(0.5, 2),
                                distortion=infit.Uniform(0.04, 0.5),
                            ),
                        )
                    ),
                    likelihood_range=(0.1, 0.7),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(1,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_CYMBALS_BIG_CLOSE),
                                pitch_factor=infit.Uniform(0.5, 2),
                                resonance_filter_frequency=infit.Uniform(5000, 9000),
                                resonance_filter_bandwidth=infit.Uniform(200, 700),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_CYMBALS_MIDDLE_CLOSE_LOUD),
                                pitch_factor=infit.Uniform(0.5, 2),
                            ),
                        )
                    ),
                    likelihood_range=(0.1, 0.7),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(2,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_CYMBALS_BIG_CLOSE),
                                pitch_factor=infit.Uniform(0.5, 2),
                                resonance_filter_frequency=infit.Uniform(1000, 3000),
                                resonance_filter_bandwidth=infit.Uniform(90, 200),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_CYMBALS_MIDDLE_CLOSE_LOUD),
                                pitch_factor=infit.Uniform(0.5, 2),
                                resonance_filter_frequency=infit.Uniform(1000, 3000),
                                resonance_filter_bandwidth=infit.Uniform(90, 200),
                            ),
                        )
                    ),
                    likelihood_range=(0.1, 0.7),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=False,
                ),
            ),
            radio_silent_channels=(1, 3, 5),
            radio_samples=(
                "pbIII/samples/radio/carolina/3.wav",
                "pbIII/samples/radio/carolina/1.wav",
            ),
            radio_n_changes=1,
            radio_average_volume=0.285,
            radio_shadow_time=0.2,
            radio_min_volume=0.925,
        ),
    )
