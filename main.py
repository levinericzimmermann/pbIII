from mutools import MU

from pbIII.globals import globals
from pbIII.segments import segments

PART0 = (
    segments.ThreeVoiceCP(
        "part0_0",
        group=(1, 1, 0),
        gender=True,
        n_bars=2,
        duration_per_bar=7,
        anticipation_time=0.5,
        overlaying_time=1,
    ),
    segments.Silence("s0", 1.5),
    segments.ThreeVoiceCP(
        "part0_1",
        group=(1, 1, 1),
        gender=True,
        n_bars=3,
        duration_per_bar=7,
        anticipation_time=0.75,
        overlaying_time=0.5,
    ),
)

SEGMENTS = PART0

PBIII = MU.MU(globals.MU_NAME, globals.PBIII_ORCHESTRATION, *SEGMENTS, tail=15)

if __name__ == "__main__":
    PBIII.render()
    PBIII.stereo_mixdown(False)
