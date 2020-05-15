import functools
import operator

from mutools import MU

from pbIII.globals import globals
from pbIII import parts

SEGMENTS = functools.reduce(operator.add, parts.SEGMENTS)

PBIII = MU.MU(globals.MU_NAME, globals.PBIII_ORCHESTRATION, *SEGMENTS, tail=15)

if __name__ == "__main__":
    # PBIII.render()
    # PBIII.render_segment("ONE_CANTUS_FIRMUS_2")
    # PBIII.render_segment("ONE_CANTUS_FIRMUS_CF_BELL_0")
    # PBIII.render_segment("ONE_DENSE_GLITTER_0")
    PBIII.concatenate()
    PBIII.stereo_mixdown(False)
