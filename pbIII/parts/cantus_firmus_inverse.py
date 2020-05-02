from mutools import ambitus

from mu.mel import ji
from mu.utils import infit
from mu.utils import interpolations

from mutools import ornamentations

from pbIII.engines import percussion
from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.segments import segments

from pbIII.globals import globals


def make(name: str = "ONE", gender=False, group=0, sub_group0=1):
    return (
        segments.MelodicCP(
            "{}_0".format(name),
            volume_envelope=interpolations.InterpolationLine(
                [
                    interpolations.FloatInterpolationEvent(0.1, 0),
                    interpolations.FloatInterpolationEvent(0, 1),
                ]
            ),
            volume_envelope_per_track={
                "voiceN0": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(3, 0),
                        interpolations.FloatInterpolationEvent(18, 1),
                        interpolations.FloatInterpolationEvent(5, 1),
                        interpolations.FloatInterpolationEvent(0, 0),
                    ]
                )
            },
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(1, 1), ji.r(3, 1), ji.r(4, 3)),
            random_seed=1000,
            group=(group, sub_group0, 0),
            action_per_voice=(0.74, 0.73),
            sound_per_voice=(0.85, 0.85),
            phrases=(0, 1),
            melody_register=0,
            melodic_weight=0,
            weight_range=(0.5, 1),
            harmonicity_range=(0.25, 1),
            gender=gender,
            duration_per_bar=12,
            start=0,
            dynamic_range_of_voices=(0.5, 0.9),
            anticipation_time=0.7,
            overlaying_time=1.2,
            voices_overlaying_time=3.5,
            pteq_engine_per_voice=(
                pteq.mk_super_soft_pte(
                    empty_attack_dynamic_maker=infit.Value(0.2),
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    sustain_pedal=0,
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
                    voice_meters2occupy=(1, 2),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_CYMBALS_BIG_CLOSE),
                                pitch_factor=infit.Uniform(0.5, 2),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_CYMBALS_MIDDLE_CLOSE_LOUD),
                                pitch_factor=infit.Uniform(0.5, 2),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_CYMBALS_MIDDLE_CLOSE_QUIET
                                ),
                                pitch_factor=infit.Uniform(0.5, 2),
                            ),
                        )
                    ),
                    likelihood_range=(0.3, 1),
                    volume_range=(0.1, 0.5),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(likelihood_range=(0, 0.1), volume_range=(0, 0)),
                percussion.Rhythmizer(likelihood_range=(0, 0.1), volume_range=(0, 0)),
            ),
            speech_init_attributes={},
            include_glitter=True,
            include_diva=True,
            include_natural_radio=True,
            include_percussion=True,
            radio_silent_channels=tuple([]),
            tracks2ignore=("speech0", "speech1", "speech2"),
            radio_samples=(
                globals.SAM_RADIO_ITALY[-1],
                globals.SAM_RADIO_BIELEFELD[-1],
            ),
            radio_n_changes=8,
            radio_average_volume=0.45,
            radio_shadow_time=0.08,
            radio_min_volume=0.955,
        ),
    )
