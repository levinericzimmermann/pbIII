from mutools import ambitus

from mu.mel import ji
from mu.utils import infit

from mutools import ornamentations

from pbIII.engines import percussion
from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.segments import segments

from pbIII.globals import globals


def make(name: str = "ONE", gender=False, group=0, sub_group0=0):
    return (
        # with activity level
        segments.FreeStyleCP(
            "{}_0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(3, 2), ji.r(3, 1), ji.r(5, 4)),
            decision_type="activity",
            energy_per_voice=(7, 10, 6),
            weight_range=(4, 10),
            metrical_numbers=(12, 6, 18),
            silence_decider_per_voice=(
                infit.ActivityLevel(1),
                infit.ActivityLevel(1),
                infit.ActivityLevel(1),
            ),
            group=(group, sub_group0, 2),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            gender=gender,
            n_bars=3,
            duration_per_bar=10,
            start=2,
            dynamic_range_of_voices=(0.2, 0.45),
            anticipation_time=0.2,
            overlaying_time=0.25,
            cp_add_dissonant_pitches_to_nth_voice=(False, True, False),
            glitter_include_dissonant_pitches=True,
            pteq_engine_per_voice=(
                pteq.mk_super_dreamy_pte(
                    empty_attack_dynamic_maker=infit.Value(0.2),
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    sustain_pedal=1,
                ),
                pteq.mk_dreamy_pte(
                    modulator=(ornamentations.SoftLineGlissandoMaker(),),
                    empty_attack_dynamic_maker=infit.Value(0.2),
                ),
                pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.2)),
            ),
            percussion_engine_per_voice=(
                percussion.Rhythmizer(
                    voice_meters2occupy=(0,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1)),
                                distortion=infit.Uniform(0, 1),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1)),
                                distortion=infit.Uniform(0, 1),
                            ),
                        )
                    ),
                    likelihood_range=(0.3, 1),
                    volume_range=(0.1, 0.8),
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
                                pitch_factor=infit.Cycle((0.5, 0.5, 1, 0.25, 1)),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1)),
                                distortion=infit.Uniform(0, 1),
                            ),
                        )
                    ),
                    likelihood_range=(0.3, 1),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(2,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1)),
                                distortion=infit.Uniform(0, 1),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1)),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_KENDANG_HIGH_LOW_FAR_HAND),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((1, 1, 0.5, 1)),
                            ),
                        )
                    ),
                    likelihood_range=(0.3, 1),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=False,
                ),
            ),
            speech_init_attributes={},
            include_glitter=True,
            include_diva=False,
            include_natural_radio=True,
            voices_overlaying_time=5,
            radio_silent_channels=(1, 3, 5),
            radio_samples=(
                "pbIII/samples/radio/carolina/3.wav",
                "pbIII/samples/radio/carolina/1.wav",
            ),
            radio_n_changes=1,
            radio_average_volume=0.095,
            radio_shadow_time=0.085,
            radio_min_volume=0.825,
        ),
    )
