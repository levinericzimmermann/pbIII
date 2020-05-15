from mutools import ambitus

from mu.mel import ji
from mu.utils import infit

# from mu.utils import interpolations

from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.segments import segments


def make(name: str = "TWO", gender=False, group=0, sub_group0=1):
    return (
        segments.Chord(
            "{}_Bell0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(4, 1), ji.r(2, 1), ji.r(5, 4)),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="A", idx=0, gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=10,
            start=0,
            dynamic_range_of_voices=(0.95, 1),
            voices_entry_delay_per_voice=(0, 0.15, 0.225),
            anticipation_time=5,
            overlaying_time=0,
            pteq_engine_per_voice=(
                pteq.mk_trippy_bell_pte(
                    fxp='"pbIII/fxp/Bells_no_stretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
                pteq.mk_trippy_bell_pte(
                    fxp='"pbIII/fxp/Bells_no_stretching.fxp"',
                    preset=None,
                    empty_attack_dynamic_maker=infit.Value(0),
                ),
                pteq.mk_trippy_bell_pte(
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
    )
