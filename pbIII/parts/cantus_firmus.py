from mutools import ambitus

from mu.mel import ji
from mu.utils import infit
from mu.utils import interpolations

from mutools import ornamentations

from pbIII.engines import diva
from pbIII.engines import percussion
from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.fragments import tremolo

from pbIII.segments import segments

from pbIII.globals import globals


def make(name: str = "ONE", gender=True, group=0, sub_group0=0):
    return (
        segments.MelodicCP(
            "{}_0".format(name),
            volume_envelope=interpolations.InterpolationLine(
                [
                    interpolations.FloatInterpolationEvent(11, 1),
                    interpolations.FloatInterpolationEvent(4, 1),
                    interpolations.FloatInterpolationEvent(0, 0.4),
                ]
            ),
            volume_envelope_per_track={
                "voiceP0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(4, 0.7),
                        interpolations.FloatInterpolationEvent(6, 1.1),
                        interpolations.FloatInterpolationEvent(2, 1.1),
                        interpolations.FloatInterpolationEvent(0, 0.4),
                    ]
                ),
                "divaP0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(4, 0.4),
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
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(2, 1), ji.r(3, 1), ji.r(5, 4)),
            random_seed=1000,
            group=(group, sub_group0, 0),
            action_per_voice=(0.94, 0.93),
            sound_per_voice=(0.89, 0.87),
            phrases=(0,),
            melody_register=1,
            melodic_weight=0,
            weight_range=(0.3, 1),
            harmonicity_range=(0.25, 1),
            gender=gender,
            duration_per_bar=13,
            start=0,
            dynamic_range_of_voices=(0.4, 0.75),
            anticipation_time=3,
            overlaying_time=2.2,
            voices_overlaying_time=3.5,
            glitter_attack_duration=infit.Gaussian(1.9, 0.15),
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
                    likelihood_range=(0.85, 0.285),
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
            speech_init_attributes={},
            include_glitter=True,
            include_diva=True,
            include_natural_radio=True,
            include_percussion=True,
            radio_silent_channels=(1, 3, 5),
            tracks2ignore=("speech0", "speech1", "speech2"),
            radio_samples=(
                globals.SAM_RADIO_PROCESSED_DEGRADE[0],
                globals.SAM_RADIO_ITALY[-1],
                globals.SAM_RADIO_BIELEFELD[-1],
            ),
            radio_n_changes=8,
            radio_average_volume=0.45,
            radio_shadow_time=0.08,
            radio_min_volume=0.955,
        ),
        segments.MelodicCP(
            "{}_1".format(name),
            volume_envelope=interpolations.InterpolationLine(
                [
                    interpolations.FloatInterpolationEvent(0.1, 0),
                    interpolations.FloatInterpolationEvent(0, 1),
                ]
            ),
            volume_envelope_per_track={
                "voiceP0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(3, 0.5),
                        interpolations.FloatInterpolationEvent(18, 1),
                        interpolations.FloatInterpolationEvent(5, 1),
                        interpolations.FloatInterpolationEvent(0, 0),
                    ]
                ),
                "voiceP1": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(21, 1),
                        interpolations.FloatInterpolationEvent(6, 1),
                        interpolations.FloatInterpolationEvent(3, 0.7),
                        interpolations.FloatInterpolationEvent(0, 0.135),
                    ]
                )
            },
            diva_engine_per_voice=(
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
                diva.FlageoletDivaMidiEngine,
            ),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(3, 2), ji.r(3, 1), ji.r(5, 4)),
            random_seed=1000,
            group=(group, sub_group0, 1),
            action_per_voice=(0.94, 0.97),
            sound_per_voice=(0.96, 0.96),
            phrases=(1, 2),
            melody_register=1,
            melodic_weight=0,
            weight_range=(0.5, 1),
            harmonicity_range=(0.25, 1),
            gender=gender,
            duration_per_bar=13,
            start=0.72,
            glitter_attack_duration=infit.Gaussian(1, 0.15),
            glitter_release_duration=infit.Gaussian(1, 0.15),
            dynamic_range_of_voices=(0.55, 0.9),
            anticipation_time=1,
            overlaying_time=1.5,
            voices_overlaying_time=4,
            tremolo_maker_per_voice=(
                None,
                tremolo.TremoloMaker(
                    add_tremolo_decider=infit.ActivityLevel(6),
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Gaussian, (0.23, 0.12))
                    ),
                    tremolo_volume_factor=0.39,
                ),
                tremolo.TremoloMaker(
                    add_tremolo_decider=infit.ActivityLevel(6),
                    tremolo_size_generator_per_tone=infit.MetaCycle(
                        (infit.Gaussian, (0.09, 0.03))
                    ),
                    tremolo_volume_factor=0.42,
                ),
            ),
            pteq_engine_per_voice=(
                pteq.mk_super_soft_leading_pte(
                    empty_attack_dynamic_maker=infit.Value(0.2),
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    sustain_pedal=1,
                ),
                pteq.mk_dreamy_pte(
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    empty_attack_dynamic_maker=infit.Value(0.2),
                ),
                pteq.mk_super_soft_pte(
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    empty_attack_dynamic_maker=infit.Value(0.2),
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
                    likelihood_range=(0.89, 0.5),
                    volume_range=(0.1, 0.5),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(1,),
                    chord=infit.Cycle(
                        (
                            harmony.find_harmony(name="B", gender=gender),
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
                    likelihood_range=(0.8, 0.1),
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
                                path=infit.Cycle(globals.SAM_RADIO_ROEHRENRADIO_KEYS),
                                pitch_factor=infit.Uniform(0.8, 2),
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
                    likelihood_range=(0.1, 0.7),
                    volume_range=(0.1, 0.5),
                    ignore_beats_occupied_by_voice=False,
                ),
            ),
            speech_init_attributes={},
            include_glitter=True,
            include_diva=True,
            include_natural_radio=True,
            include_percussion=True,
            radio_silent_channels=(1, 3),
            tracks2ignore=("speech0", "speech1", "speech2"),
            radio_samples=(
                globals.SAM_RADIO_ITALY[-1],
                globals.SAM_RADIO_BIELEFELD[-1],
            ),
            radio_n_changes=8,
            radio_average_volume=0.4,
            radio_shadow_time=0.08,
            radio_min_volume=0.955,
        ),
        segments.Chord(
            "{}_CF_BELL_0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(7, 1), ji.r(2, 1), ji.r(4, 3)),
            group=(group, sub_group0, 2),
            chord=harmony.find_harmony(name="A", gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=8,
            start=-0.75,
            dynamic_range_of_voices=(0.8, 1),
            anticipation_time=0.1,
            overlaying_time=0.25,
            voices_entry_delay_per_voice=(0, 0.05, 0.08),
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
            glitter_type="drone",
            glitter_register_per_voice=(4, 5, 5),
            glitter_volume_per_voice=(0.85, 0.94, 0.95),
            glitter_modulater_per_voice=("lfo", "lfo", "lfo"),
            glitter_release_duration=7,
            glitter_attack_duration=0.2,
            radio_shadow_time=0,
            include_glitter=True,
            include_diva=False,
            include_natural_radio=True,
            include_percussion=False,
        ),
        segments.MelodicCP(
            "{}_2".format(name),
            volume_envelope=interpolations.InterpolationLine(
                [
                    interpolations.FloatInterpolationEvent(0.1, 0),
                    interpolations.FloatInterpolationEvent(24, 1),
                    interpolations.FloatInterpolationEvent(3, 1),
                    interpolations.FloatInterpolationEvent(2, 0.9),
                    interpolations.FloatInterpolationEvent(0, 0.45),
                ]
            ),
            volume_envelope_per_track={
                "voiceP0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(2, 0.65),
                        interpolations.FloatInterpolationEvent(30, 0.8),
                        interpolations.FloatInterpolationEvent(5, 0.8),
                        interpolations.FloatInterpolationEvent(0, 0.1),
                    ]
                )
            },
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(8, 1), ji.r(3, 1), ji.r(2, 1)),
            random_seed=1000,
            group=(group, sub_group0, 2),
            action_per_voice=(0.82, 0.81),
            sound_per_voice=(0.75, 0.74),
            phrases=(3, 3),
            melody_register=1,
            melodic_weight=0,
            weight_range=(0.5, 1),
            harmonicity_range=(0.25, 1),
            gender=gender,
            duration_per_bar=12.75,
            start=-3.5,
            dynamic_range_of_voices=(0.3, 0.5),
            anticipation_time=2,
            overlaying_time=3.2,
            voices_overlaying_time=4.5,
            pteq_engine_per_voice=(
                pteq.mk_super_soft_trippy_pte(
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
                pteq.mk_super_soft_pte(
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    empty_attack_dynamic_maker=infit.Value(0.2),
                    fxp='"pbIII/fxp/Marimba_no_stretching.fxp"',
                    preset=None,
                    sustain_pedal=0,
                ),
                pteq.mk_super_soft_pte(
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    empty_attack_dynamic_maker=infit.Value(0.2),
                    fxp='"pbIII/fxp/Marimba_no_stretching.fxp"',
                    preset=None,
                    sustain_pedal=0,
                ),
            ),
            diva_engine_per_voice=(diva.FlageoletDivaMidiEngine, None, None),
            percussion_engine_per_voice=(
                percussion.Rhythmizer(
                    voice_meters2occupy=(0, 1, 2),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_RADIO_ROEHRENRADIO_KEYS),
                                pitch_factor=infit.Uniform(0.8, 2),
                                distortion=infit.Uniform(0, 1, seed=0),
                            ),
                        )
                    ),
                    likelihood_range=(0.1, 0.2),
                    volume_range=(0, 0.001),
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(0, 1, 2),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_RADIO_ROEHRENRADIO_KEYS),
                                pitch_factor=infit.Uniform(0.7, 1.7),
                                distortion=infit.Uniform(0, 2, seed=0),
                            ),
                        )
                    ),
                    likelihood_range=(0.08, 0.55),
                    volume_range=(0.54, 0.8),
                    ignore_beats_occupied_by_voice=True,
                    seed=39,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(0, 1, 2),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_RADIO_ROEHRENRADIO_KEYS),
                                pitch_factor=infit.Uniform(0.4, 1),
                                distortion=infit.Uniform(0.4, 1.8),
                            ),
                        )
                    ),
                    likelihood_range=(0.1, 0.2),
                    volume_range=(0, 0.01),
                ),
            ),
            speech_init_attributes={},
            include_glitter=True,
            include_diva=True,
            include_natural_radio=True,
            include_percussion=True,
            radio_silent_channels=tuple([]),
            glitter_modulater_per_voice=("randomh", "randomh", "randomh"),
            glitter_attack_duration=infit.Gaussian(0.75, 0.15),
            glitter_release_duration=infit.Gaussian(1.8, 0.25),
            tracks2ignore=("speech0", "speech1", "speech2"),
            radio_samples=(globals.SAM_RADIO_ITALY[-1], globals.SAM_RADIO_ITALY[-2]),
            radio_n_changes=4,
            radio_average_volume=0.4,
            radio_shadow_time=0.08,
            radio_min_volume=0.855,
        ),
        segments.Silence(name="{}_silence0".format(name), duration=11),
    )
