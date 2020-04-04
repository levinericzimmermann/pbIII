from mutools import MU

from pbIII.globals import globals
from pbIII.segments import segments

PART0 = (
    segments.ThreeVoiceCP(
        "part0_0",
        group=(1, 1, 0),
        gender=True,
        n_bars=1,
        duration_per_bar=7,
        anticipation_time=0.5,
        overlaying_time=1,
    ),
    segments.ThreeVoiceCP(
        "part0_1",
        group=(1, 1, 1),
        start=2,
        gender=True,
        n_bars=1,
        duration_per_bar=7,
        anticipation_time=0.75,
        overlaying_time=0.5,
    ),
    segments.ThreeVoiceCP(
        "part0_2",
        group=(1, 1, 2),
        gender=True,
        start=6,
        n_bars=1,
        duration_per_bar=7,
        anticipation_time=0.5,
        overlaying_time=0.5,
        include_voices=False,
        include_diva=False,
        radio_n_changes=0,
    ),
)

SEGMENTS = PART0

PBIII = MU.MU(globals.MU_NAME, globals.PBIII_ORCHESTRATION, *SEGMENTS, tail=15)

if __name__ == "__main__":
    PBIII.render()
    PBIII.stereo_mixdown(False)
