from mutools import ambitus

from mu.mel import ji
from mu.utils import infit
from mu.utils import interpolations

from mutools import counterpoint
from mutools import ornamentations

from pbIII.engines import percussion
from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.segments import segments

from pbIII.globals import globals


def make(name: str = "ONE", gender=False, group=0, sub_group0=1):
    return (
        segments.FreeStyleCP(
            "{}_0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(
                ji.r(2, 1), ji.r(12, 5), ji.r(9, 4)
            ),
            volume_envelope=interpolations.InterpolationLine(
                [
                    interpolations.FloatInterpolationEvent(1, 0),
                    interpolations.FloatInterpolationEvent(11, 1),
                    interpolations.FloatInterpolationEvent(4, 1),
                    interpolations.FloatInterpolationEvent(0, 0.4),
                ]
            ),
            volume_envelope_per_track={
                "voiceP0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(4, 0),
                        interpolations.FloatInterpolationEvent(6, 1),
                        interpolations.FloatInterpolationEvent(2, 1),
                        interpolations.FloatInterpolationEvent(0, 0),
                    ]
                ),
                "voiceP1": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(2, 0),
                        interpolations.FloatInterpolationEvent(0, 1),
                    ]
                ),
                "voiceP2": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(3, 0),
                        interpolations.FloatInterpolationEvent(0, 1),
                    ]
                ),
            },
            group=(group, sub_group0, 0),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            energy_per_voice=(4, 10, 10),
            silence_decider_per_voice=(
                infit.ActivityLevel(8),
                infit.ActivityLevel(3),
                infit.ActivityLevel(3),
            ),
            weight_range=(6, 10),
            decision_type="activity",
            gender=gender,
            n_bars=2,
            duration_per_bar=11,
            start=4,
            dynamic_range_of_voices=(0.6, 1),
            anticipation_time=1.75,
            overlaying_time=2.25,
            cp_add_dissonant_pitches_to_nth_voice=(False, True, True),
            cp_constraints_interpolation=(
                counterpoint.constraints.AP_tremolo(
                    0,
                    add_tremolo_decider=infit.ActivityLevel(10),
                    only_on_non_dissonant_pitches=False,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Value, (4,))
                    ),
                ),
                counterpoint.constraints.AP_tremolo(
                    1,
                    add_tremolo_decider=infit.ActivityLevel(4),
                    only_on_non_dissonant_pitches=True,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, ((1, 2, 3, 4),))
                    ),
                ),
                counterpoint.constraints.AP_tremolo(
                    2,
                    add_tremolo_decider=infit.ActivityLevel(3),
                    only_on_non_dissonant_pitches=True,
                    define_tremolo_tones_as_dissonant=False,
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Cycle, ((4, 3, 4, 5, 6, 7, 8, 9, 10),))
                    ),
                ),
            ),
            glitter_include_dissonant_pitches=False,
            voices_overlaying_time=1,
            pteq_engine_per_voice=(
                pteq.mk_super_soft_pte(
                    empty_attack_dynamic_maker=infit.Uniform(0.15, 0.3),
                    # modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    convert_dissonant_tones2glissandi=False,
                    # preset='"Pleyel Player"',
                    preset=None,
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    sustain_pedal=0,
                ),
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Uniform(0.15, 0.3),
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    convert_dissonant_tones2glissandi=True,
                    preset='"Pleyel Player"',
                    sustain_pedal=0,
                ),
                pteq.mk_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Uniform(0.15, 0.3),
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    convert_dissonant_tones2glissandi=True,
                    preset='"Pleyel Player"',
                    sustain_pedal=0,
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
                    likelihood_range=(0.3, 0.1),
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
                    likelihood_range=(0.1, 0.3),
                    volume_range=(0.1, 0.5),
                    ignore_beats_occupied_by_voice=False,
                ),
            ),
            speech_init_attributes={},
            glitter_modulater_per_voice=("randomi", "randomh", "randomh"),
            include_glitter=True,
            include_diva=True,
            include_natural_radio=True,
            include_percussion=True,
            # radio_silent_channels=(1, 3, 5),
            radio_samples=(
                "pbIII/samples/radio/carolina/3.wav",
                "pbIII/samples/radio/carolina/1.wav",
            ),
            radio_n_changes=1,
            radio_average_volume=0.08,
            radio_shadow_time=0.085,
            radio_min_volume=0.925,
        ),
    )
