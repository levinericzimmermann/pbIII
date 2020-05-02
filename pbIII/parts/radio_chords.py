from mutools import ambitus

from mu.mel import ji
from mu.utils import infit

from pbIII.engines import percussion
from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.segments import segments

from pbIII.globals import globals


def make(name: str = "ONE", gender=True, group=0, sub_group0=0):
    return (
        segments.FreeStyleCP(
            "{}_3".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(1, 1), ji.r(3, 1), ji.r(5, 4)),
            energy_per_voice=(6, 6, 7),
            weight_range=(3, 10),
            silence_decider_per_voice=(
                infit.ActivityLevel(2),
                infit.ActivityLevel(1),
                infit.ActivityLevel(1),
            ),
            group=(group, sub_group0, 0),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=12 * 3,
            start=0,
            metrical_numbers=(12, 12, 12),
            dynamic_range_of_voices=(0.1, 0.65),
            anticipation_time=1,
            overlaying_time=1.55,
            cp_add_dissonant_pitches_to_nth_voice=(True, True, True),
            cp_constraints_interpolation=[],
            glitter_include_dissonant_pitches=False,
            pteq_engine_per_voice=(
                pteq.mk_dreamy_pte(
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0.1),
                ),
                pteq.mk_dreamy_pte(
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0.1),
                ),
                pteq.mk_dreamy_pte(
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                ),
            ),
            percussion_engine_per_voice=(
                percussion.Rhythmizer(
                    voice_meters2occupy=(0,),
                    likelihood_range=(0.1, 0.6),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=True,
                    seed=100,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(2,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_SPEECH_TIME),
                                pitch_factor=infit.Uniform(0.9, 1.1),
                            ),
                        )
                    ),
                    likelihood_range=(1, 0.2),
                    volume_range=(0.1, 0.3),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(2,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_SPEECH_SPACE),
                                pitch_factor=infit.Uniform(0.9, 1.1),
                            ),
                        )
                    ),
                    likelihood_range=(1, 0.2),
                    volume_range=(0.1, 0.3),
                    ignore_beats_occupied_by_voice=False,
                ),
            ),
            include_glitter=True,
            include_diva=False,
            include_natural_radio=True,
            include_percussion=True,
            radio_silent_channels=(1, 5),
            radio_samples=(
                "pbIII/samples/radio/carolina/3.wav",
                "pbIII/samples/radio/carolina/1.wav",
            ),
            radio_n_changes=2,
            radio_average_volume=0.385,
            radio_shadow_time=0.2,
            radio_min_volume=0.925,
            speech_init_attributes={},
        ),
    )
