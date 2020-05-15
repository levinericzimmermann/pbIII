from mutools import ambitus

from mu.mel import ji
from mu.utils import infit

# from mu.utils import interpolations

from pbIII.engines import percussion
from pbIII.engines import pteq

# from pbIII.engines import speech

from pbIII.fragments import harmony
from pbIII.segments import segments

from pbIII.globals import globals


def make(name: str = "TWO", gender=False, group=0, sub_group0=1):
    return (
        segments.FreeStyleCP(
            "{}_0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(
                ji.r(5, 1), ji.r(9, 4), ji.r(16, 11)
            ),
            decision_type="activity",
            energy_per_voice=(9, 7, 7),
            weight_range=(4, 10),
            metrical_numbers=(12, 9, 12),
            silence_decider_per_voice=(
                infit.ActivityLevel(2),
                infit.ActivityLevel(1),
                infit.ActivityLevel(2),
            ),
            group=(group, sub_group0, 0),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            gender=gender,
            n_bars=2,
            duration_per_bar=13,
            start=0,
            dynamic_range_of_voices=(0.2, 0.5),
            anticipation_time=0.01,
            overlaying_time=0.25,
            cp_add_dissonant_pitches_to_nth_voice=(True, True, True),
            glitter_include_dissonant_pitches=True,
            pteq_engine_per_voice=(
                pteq.mk_super_soft_trippy_pte(
                    empty_attack_dynamic_maker=infit.Value(0.2),
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    sustain_pedal=0,
                ),
                pteq.mk_dreamy_pte(
                    # modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    convert_dissonant_tones2glissandi=True,
                    empty_attack_dynamic_maker=infit.Value(0.2),
                ),
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0.2),
                    convert_dissonant_tones2glissandi=True,
                ),
            ),
            speech_init_attributes={},
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
                    likelihood_range=(0.5, 0.1),
                    volume_range=(0.1, 0.5),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(1,),
                    chord=infit.Cycle(
                        (
                            harmony.find_harmony(name="A", gender=gender),
                            harmony.find_harmony(name="C", gender=gender),
                        )
                    ),
                    sample_maker=infit.Cycle(
                        (
                            percussion.ResonanceSample(
                                path=infit.Cycle(globals.SAM_CYMBALS_BIG_CLOSE),
                                pitch_factor=infit.Gaussian(3, 5),
                                resonance_filter_bandwidth=infit.Gaussian(0.8, 0.5),
                                resonance_filter_octave=infit.Cycle((2,)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.3),
                                glissando_offset=0,
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                            percussion.ResonanceSample(
                                path=infit.Cycle(globals.SAM_CYMBALS_MIDDLE_CLOSE_LOUD),
                                pitch_factor=infit.Gaussian(3, 4),
                                resonance_filter_bandwidth=infit.Uniform(0.5, 1),
                                resonance_filter_octave=infit.Cycle((2,)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=0,
                                glissando_size=infit.Gaussian(1, 0.1),
                            ),
                        )
                    ),
                    likelihood_range=(0.6, 0.1),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(0, 1, 2),
                    chord=infit.Cycle((harmony.find_harmony(name="B", gender=gender),)),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_HIGH_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_HIGH_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((2, 4, 8, 4)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=infit.Uniform(0, 0.1),
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((16, 8, 4, 8, 2)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=infit.Uniform(0, 0.1),
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_HIGH_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_HIGH_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((8, 4, 2, 4)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=infit.Uniform(0, 0.1),
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((8, 16, 8, 4, 8, 2)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=infit.Uniform(0, 0.1),
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                        )
                    ),
                    likelihood_range=(0.1, 0.5),
                    volume_range=(0.1, 0.5),
                    ignore_beats_occupied_by_voice=False,
                ),
            ),
            include_glitter=True,
            include_diva=False,
            include_natural_radio=True,
            include_percussion=True,
            voices_overlaying_time=5,
            radio_samples=(
                globals.SAM_RADIO_ITALY[-1],
                globals.SAM_RADIO_BIELEFELD[-1],
            ),
            radio_n_changes=8,
            radio_average_volume=0.1,
            radio_shadow_time=0.01,
            radio_min_volume=0.825,
        ),
        segments.Chord(
            "{}_Bell2".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(
                ji.r(12, 1), ji.r(2, 1), ji.r(15, 8)
            ),
            group=(group, sub_group0, 1),
            chord=harmony.find_harmony(name="A", idx=0, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=8,
            start=4,
            dynamic_range_of_voices=(0.7, 0.9),
            anticipation_time=0.2,
            overlaying_time=1.25,
            glitter_modulater_per_voice=("randomh", "randomh", "randomh"),
            pteq_engine_per_voice=(
                pteq.mk_bright_bell(
                    fxp='"pbIII/fxp/Bells_no_stretching.fxp"',
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
            # speech_init_attributes={
            #     # "speech0": {
            #     #     "start": 0.3,
            #     #     "duration": 12.5,
            #     #     "sound_engine": speech.Sampler(
            #     #         globals.SAM_RADIO_CAROLINA[1], volume=0.6
            #     #     ),
            #     # },
            #     # "speech2": {
            #     #     "start": -0.3,
            #     #     "duration": 12.5,
            #     #     "sound_engine": speech.Sampler(
            #     #         globals.SAM_RADIO_ROEHRENRADIO_CLOSE_MITTELWELLE[-1], volume=0.6
            #     #     ),
            #     # },
            # },
            include_glitter=False,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
        ),
        segments.FreeStyleCP(
            "{}_1".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(
                ji.r(5, 1), ji.r(9, 4), ji.r(16, 11)
            ),
            decision_type="activity",
            energy_per_voice=(9, 6, 7),
            weight_range=(4, 10),
            metrical_numbers=(13, 9, 13),
            silence_decider_per_voice=(
                infit.ActivityLevel(2),
                infit.ActivityLevel(1),
                infit.ActivityLevel(2),
            ),
            group=(group, sub_group0, 1),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            gender=gender,
            n_bars=2,
            duration_per_bar=15,
            start=-3.8,
            dynamic_range_of_voices=(0.2, 0.4),
            anticipation_time=0.01,
            overlaying_time=0.25,
            cp_add_dissonant_pitches_to_nth_voice=(True, True, True),
            glitter_include_dissonant_pitches=True,
            pteq_engine_per_voice=(
                pteq.mk_super_soft_trippy_pte(
                    empty_attack_dynamic_maker=infit.Value(0.2),
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    sustain_pedal=0,
                ),
                pteq.mk_dreamy_pte(
                    # modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    convert_dissonant_tones2glissandi=True,
                    empty_attack_dynamic_maker=infit.Value(0.2),
                ),
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0.2),
                    convert_dissonant_tones2glissandi=True,
                ),
            ),
            speech_init_attributes={},
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
                    likelihood_range=(0.5, 0.1),
                    volume_range=(0.1, 0.5),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(1,),
                    chord=infit.Cycle(
                        (
                            harmony.find_harmony(name="A", gender=gender),
                            harmony.find_harmony(name="C", gender=gender),
                        )
                    ),
                    sample_maker=infit.Cycle(
                        (
                            percussion.ResonanceSample(
                                path=infit.Cycle(globals.SAM_CYMBALS_BIG_CLOSE),
                                pitch_factor=infit.Gaussian(3, 5),
                                resonance_filter_bandwidth=infit.Gaussian(0.8, 0.5),
                                resonance_filter_octave=infit.Cycle((2,)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.3),
                                glissando_offset=0,
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                            percussion.ResonanceSample(
                                path=infit.Cycle(globals.SAM_CYMBALS_MIDDLE_CLOSE_LOUD),
                                pitch_factor=infit.Gaussian(3, 4),
                                resonance_filter_bandwidth=infit.Uniform(0.5, 1),
                                resonance_filter_octave=infit.Cycle((2,)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=0,
                                glissando_size=infit.Gaussian(1, 0.1),
                            ),
                        )
                    ),
                    likelihood_range=(0.6, 0.1),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(0, 1, 2),
                    chord=infit.Cycle((harmony.find_harmony(name="B", gender=gender),)),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_HIGH_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_HIGH_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((2, 4, 8, 4)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=infit.Uniform(0, 0.1),
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((16, 8, 4, 8, 2)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=infit.Uniform(0, 0.1),
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_HIGH_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_HIGH_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((8, 4, 2, 4)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=infit.Uniform(0, 0.1),
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_CLOSE_HAND
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_CLOSE_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((8, 16, 8, 4, 8, 2)),
                                glissando_direction=True,
                                glissando_duration=infit.Uniform(0.001, 0.2),
                                glissando_offset=infit.Uniform(0, 0.1),
                                glissando_size=infit.Gaussian(1, 0.2),
                            ),
                        )
                    ),
                    likelihood_range=(0.1, 0.5),
                    volume_range=(0.1, 0.5),
                    ignore_beats_occupied_by_voice=False,
                ),
            ),
            include_glitter=True,
            include_diva=False,
            include_natural_radio=True,
            include_percussion=True,
            voices_overlaying_time=5,
            radio_samples=(
                globals.SAM_RADIO_ITALY[-1],
                globals.SAM_RADIO_BIELEFELD[-1],
            ),
            radio_n_changes=8,
            radio_average_volume=0.1,
            radio_shadow_time=0.01,
            radio_min_volume=0.825,
        ),
    )
