from mutools import ambitus

from mu.mel import ji
from mu.utils import infit

from mu.utils import interpolations

from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.segments import segments


def make(name: str = "TWO", gender=False, group=0, sub_group0=1):
    return (
        segments.Chord(
            "{}_Bell0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(7, 1), ji.r(2, 1), ji.r(5, 4)),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="A", idx=0, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=15,
            start=0,
            dynamic_range_of_voices=(0.3, 0.385),
            voices_entry_delay_per_voice=(0.03, 0, 0.05),
            anticipation_time=1.25,
            overlaying_time=1.25,
            pteq_engine_per_voice=(
                pteq.mk_pianoteq_engine(
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
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
            ),
            speech_init_attributes={},
            include_glitter=False,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
        ),
        segments.Chord(
            "{}_Bell1".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(
                ji.r(11, 1), ji.r(2, 1), ji.r(15, 8)
            ),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="B", idx=0, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=8,
            start=-12.7,
            dynamic_range_of_voices=(0.45, 0.55),
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
            include_glitter=False,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
        ),
        segments.Chord(
            "{}_Bell2".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(
                ji.r(13, 1), ji.r(2, 1), ji.r(15, 8)
            ),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="F", idx=0, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=14,
            start=5.75,
            dynamic_range_of_voices=(0.8, 0.9),
            anticipation_time=0,
            overlaying_time=0,
            voices_entry_delay_per_voice=(0, 0.05, 0.1),
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
            glitter_type="drone",
            glitter_register_per_voice=(5, 5, 5),
            glitter_volume_per_voice=(0.3, 0.3, 0.3),
            glitter_modulater_per_voice=(None, None, None),
            glitter_release_duration=7,
            glitter_attack_duration=0.5,
            include_glitter=True,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
        ),
        segments.Chord(
            "{}_Bell3".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(4, 1), ji.r(2, 1), ji.r(5, 4)),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="A", idx=0, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=10,
            start=-4.25,
            # start=0,
            dynamic_range_of_voices=(0.95, 1),
            voices_entry_delay_per_voice=(0, 0.15, 0.225),
            anticipation_time=5.5,
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
                        interpolations.FloatInterpolationEvent(2, 0.5),
                        interpolations.FloatInterpolationEvent(5, 1),
                        interpolations.FloatInterpolationEvent(0, 0.3),
                    ]
                ),
                "glitterN02": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(3, 0),
                        interpolations.FloatInterpolationEvent(2, 0.5),
                        interpolations.FloatInterpolationEvent(5, 1),
                        interpolations.FloatInterpolationEvent(0, 0.3),
                    ]
                ),
                "glitterN12": interpolations.InterpolationLine(
                    [
                        interpolations.FloatInterpolationEvent(3, 0),
                        interpolations.FloatInterpolationEvent(2, 0.5),
                        interpolations.FloatInterpolationEvent(5, 1),
                        interpolations.FloatInterpolationEvent(0, 0.3),
                    ]
                ),
            },
            glitter_type="drone",
            glitter_register_per_voice=(5, 5, 5),
            glitter_volume_per_voice=(3.5, 3.5, 3.5),
            glitter_modulater_per_voice=(None, None, None),
            glitter_release_duration=5,
            glitter_attack_duration=8,
            include_glitter=True,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
        ),
    )
