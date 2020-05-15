from mutools import ambitus

from mu.mel import ji
from mu.utils import infit
from mu.utils import interpolations

from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.segments import segments


def make(name: str = "ONE", gender=True, group=0, sub_group0=0):
    return (
        segments.Silence(name="{}_silence0".format(name), duration=5),
        segments.Chord(
            "{}_Bell0".format(name),
            volume_envelope=interpolations.InterpolationLine(
                [
                    interpolations.FloatInterpolationEvent(0.1, 0),
                    interpolations.FloatInterpolationEvent(0.2, 1),
                    interpolations.FloatInterpolationEvent(0, 1),
                ]
            ),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(2, 1), ji.r(2, 1), ji.r(9, 8)),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="A", gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=22,
            start=0,
            dynamic_range_of_voices=(0.8, 0.9),
            voices_entry_delay_per_voice=(0, 0.05, 0.03),
            anticipation_time=1.25,
            overlaying_time=1.25,
            pteq_engine_per_voice=(
                pteq.mk_pianoteq_engine(
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
                pteq.mk_pianoteq_engine(
                    fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
                pteq.mk_pianoteq_engine(
                    preset='"Church Bells original"',
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
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(8, 1), ji.r(2, 1), ji.r(9, 8)),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="C", idx=1, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=9,
            start=0,
            dynamic_range_of_voices=(0.05, 0.4),
            anticipation_time=0,
            overlaying_time=0,
            voices_entry_delay_per_voice=(0.025, 0, 0.05),
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
                pteq.mk_bright_bell(
                    fxp='"pbIII/fxp/GlockenspielHumanizednostretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
            ),
            speech_init_attributes={},
            glitter_type="drone",
            glitter_register_per_voice=(2, 3, 4),
            glitter_volume_per_voice=(0.01, 0.02, 0.04),
            glitter_modulater_per_voice=("lfo", "randomi", "lfo"),
            glitter_release_duration=7,
            glitter_attack_duration=0.2,
            include_glitter=True,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
        ),
        segments.Chord(
            "{}_Bell2".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(6, 1), ji.r(2, 1), ji.r(9, 8)),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="B", gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=17,
            start=6,
            dynamic_range_of_voices=(0.87, 1),
            voices_entry_delay_per_voice=(0.015, 0, 0.03),
            anticipation_time=1.25,
            overlaying_time=1.25,
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
        segments.Silence(name="{}_silence1".format(name), duration=6),
    )
