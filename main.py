from mutools import MU

from pbIII.globals import globals
from pbIII.segments import segments

PART0 = (
    segments.ThreeVoiceCP(
        "part0_0",
        group=(3, 1, 0),
        gender=False,
        n_bars=2,
        duration_per_bar=8,
        anticipation_time=0.5,
        overlaying_time=2,
    ),
    segments.Silence("s0", 2.5),
    segments.ThreeVoiceCP(
        "part0_1",
        group=(3, 1, 1),
        gender=False,
        n_bars=1,
        duration_per_bar=12,
        anticipation_time=1.75,
        overlaying_time=0.5,
    ),
)

SEGMENTS = PART0

PBIII = MU.MU(globals.MU_NAME, globals.PBIII_ORCHESTRATION, *SEGMENTS, tail=15)

if __name__ == "__main__":
    PBIII.render()
    PBIII.stereo_mixdown(False)
