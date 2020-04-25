import natsort
import os
import re

import abjad

from mu.mel import ji
from mu.mel import shortwriting as sw

from mutools import MU

from pbIII.globals import soil

"""Defining global variables for the complete composition."""

CONCERT_PITCH = 250

# naming standard:
# y*z, x*y*z, w*x*y*z (/v)
# z -> 0
# y -> 1
# x -> 2
# w -> 3
# v -> 4

M1 = ji.BlueprintPitch([1])
M2 = ji.BlueprintPitch([2])
M3 = ji.BlueprintPitch([3])
M4 = ji.BlueprintPitch([4])

M2_1 = ji.BlueprintPitch([2], [1])
M3_1 = ji.BlueprintPitch([3], [1])
M4_1 = ji.BlueprintPitch([4], [1])

M01 = ji.BlueprintPitch([0, 1])
M11 = ji.BlueprintPitch([1, 1])
M02 = ji.BlueprintPitch([0, 2])

M21 = ji.BlueprintPitch([2, 1])
M12 = ji.BlueprintPitch([1, 2])

M31 = ji.BlueprintPitch([3, 1])
M22 = ji.BlueprintPitch([2, 2])

M11_1 = ji.BlueprintPitch([1, 1], [1])
M21_1 = ji.BlueprintPitch([2, 1], [1])
M02_1 = ji.BlueprintPitch([0, 2], [1])

BLUEPRINT_HARMONIES = {
    # 'inner harmony' and its subtitutes
    "A": (
        (
            # main harmony
            (ji.BlueprintHarmony((M4, (0, 1, 2, 3)), (M3, (0, 1, 2)), (M2, (0, 1))),),
            # and its substitutes
            (
                ji.BlueprintHarmony(
                    (M4, (0, 1, 2, 3)), (M3, (0, 1, 2)), (M2_1, (0, 1, 2))
                ),
                ji.BlueprintHarmony(
                    (M4, (0, 1, 2, 3)), (M3_1, (0, 1, 2, 3)), (M2, (0, 1))
                ),
                ji.BlueprintHarmony(
                    (M4_1, (0, 1, 2, 3, 4)), (M3, (0, 1, 2)), (M2, (0, 1))
                ),
                ji.BlueprintHarmony((M3, (0, 1, 3)), (M3, (0, 1, 2)), (M2, (0, 1))),
            ),
        ),
        # interpolation pitches:
        ji.BlueprintHarmony(
            (M11, (0, 1)),
            (M11, (1, 0)),
            (M02, (0, 1)),
            (M21, (1, 2, 0)),
            (M21, (0, 2, 1)),
            (M12, (2, 0, 1)),
            (M31, (1, 2, 3, 0)),
            (M31, (0, 2, 3, 1)),
            (M22, (2, 3, 0, 1)),
        ),
    ),
    # 'main harmony' and its subtitutes
    "B": (
        (
            # main harmony
            (
                ji.BlueprintHarmony((M3, (0, 1, 2)), (M2, (0, 1)), (M1, (0,))),
                ji.BlueprintHarmony((M3, (0, 1, 2)), (M2, (0, 1)), (M1, (1,))),
            ),
            # and its substitutes
            (
                ji.BlueprintHarmony((M3, (0, 1, 2)), (M2, (0, 1)), (M2, (0, 1))),
                ji.BlueprintHarmony((M3, (0, 1, 2)), (M3, (0, 1, 2)), (M2, (0, 1))),
                ji.BlueprintHarmony((M3, (0, 1, 2)), (M2, (0, 1)), (M2_1, (0, 1, 2))),
            ),
        ),
        # interpolation pitches:
        ji.BlueprintHarmony(
            (M01, (0,)),
            (M01, (1,)),
            (M11, (1, 0)),
            (M11, (0, 1)),
            (M02, (0, 1)),
            (M21, (1, 2, 0)),
            (M21, (0, 2, 1)),
            (M12, (2, 0, 1)),
        ),
    ),
    # 'pefect diverse harmony' and its subtitutes
    "C": (
        (
            # main harmony
            (
                ji.BlueprintHarmony((M3, (0, 1, 2)), (M2, (0, 2)), (M2, (0, 1))),
                ji.BlueprintHarmony((M3, (0, 1, 2)), (M2, (1, 2)), (M2, (0, 1))),
            ),
            # and its substitutes
            tuple([]),
        ),
        # interpolation pitches:
        ji.BlueprintHarmony(
            (M01, (0,)),
            (M01, (1,)),
            (M11, (1, 0)),
            (M11, (0, 1)),
            (M11, (2, 0)),
            (M11, (2, 1)),
            (M21, (1, 2, 0)),
            (M21, (0, 2, 1)),
        ),
    ),
    # 'imperfect diverse harmony' and its subtitutes
    "D": (
        (
            # main harmony
            (
                ji.BlueprintHarmony((M3, (3, 1, 2)), (M3, (0, 1, 2)), (M2, (0, 1))),
                ji.BlueprintHarmony((M3, (0, 3, 2)), (M3, (0, 1, 2)), (M2, (0, 1))),
            ),
            # and its substitutes
            tuple([]),
        ),
        # interpolation pitches:
        ji.BlueprintHarmony(
            (M11, (1, 0)),
            (M11, (0, 1)),
            (M21, (1, 2, 0)),
            (M21, (0, 2, 1)),
            (M21, (2, 3, 0)),
            (M21, (2, 3, 1)),
        ),
    ),
    # 'irregular harmony 0'
    "E": (
        (
            # main harmony
            (ji.BlueprintHarmony((M3, (0, 1, 2)), (M3_1, (0, 1, 2, 3)), (M2, (0, 1))),),
            # and its substitutes
            tuple([]),
        ),
        # interpolation pitches:
        ji.BlueprintHarmony(
            (M11, (1, 0)),
            (M11, (0, 1)),
            (M02, (0, 1)),
            (M21_1, (1, 2, 0, 3)),
            (M21_1, (0, 2, 1, 3)),
            (M21, (1, 2, 0)),
            (M21, (0, 2, 1)),
            (M12, (2, 0, 1)),
        ),
    ),
    # 'irregular harmony 1'
    "F": (
        (
            # main harmony
            (ji.BlueprintHarmony((M3, (0, 1, 2)), (M2, (0, 1)), (M2_1, (0, 1, 2))),),
            # and its substitutes
            tuple([]),
        ),
        # interpolation pitches:
        ji.BlueprintHarmony(
            (M11, (1, 0)),
            (M11, (0, 1)),
            (M02, (0, 1)),
            (M21, (1, 2, 0)),
            (M21, (0, 2, 1)),
            (M12, (2, 0, 1)),
            (M11_1, (0, 1, 2)),
            (M11_1, (1, 0, 2)),
            (M02_1, (0, 1, 2)),
        ),
    ),
}


GREGORIAN_CHANT_SCALE = sw.translate2line("1 11+5- 5+ 11+ 3+ 13+ 7+")[0]
# pitch that doesn't belong to usual harmonic / prime scale
GREGORIAN_CHANT_SCALE_ADDITIONAL_PITCH = GREGORIAN_CHANT_SCALE[1]

# gregorian chants copied from the book 'Chants of Church' by Monks of Solesmes
# from 1952
__CHANT_ANCTUS_SANCTUS_PITCH_DEGREES = (
    "1 4 2 1 .6 .7 1 1",
    "1 3 4 5 4 3 2 1",
    "1 4 2 1 .6 .7 1 1",
    "1 .6 .7 .6 .5 .7 2 1 .7 1 1",
    "x 1 3 4 5 4 3 5 4",
    "3 2 1 2 4 1 .6 .7 .6 .5 x",
    ".7 2 1 .7 1 1",
    "1 3 4 5 4 3 2 1 2 4 1 .6 .7 1 1",
    "x 1 3 4 5 4 3 2 1",
    "2 4 1 .6 .7 .6 .5 .7 2 1 .7 1 1 x",
    "1 .6 .7 .6 .5 .7 2 1 .7 1 1",
    "1 3 4 5 4 3 2 1 2 4 1 .6 .7 .6 .5 2 1 2 3 2 1",
)
__CHANT_ANCTUS_SANCTUS_RHYTHMS = (
    (1, 1, 1, 1, 1, 1, 1, 2),
    (1, 1, 1, 1, 1, 1, 1, 2),
    (1, 1, 1, 1, 1, 1, 1, 2),
    (1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2),
    tuple(1 for i in range(8)) + (2,),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1),
    (1, 1, 1, 1, 1, 2),
    tuple(1 for i in range(14)) + (2,),
    tuple(1 for i in range(8)) + (2,),
    (1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1),
    (1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2),
    tuple(1 for i in range(14)) + (2, 1, 1, 1, 1, 2, 2),
)
__CHANT_ANCTUS_SANCTUS_DECODEX = {
    str(idx + 1): pitch for idx, pitch in enumerate(GREGORIAN_CHANT_SCALE)
}
CHANT_ANCTUS_SANCTUS_PHRASES = tuple(
    (
        sw.translate2line(pitch_degrees, decodex=__CHANT_ANCTUS_SANCTUS_DECODEX)[0],
        rhythm,
    )
    for pitch_degrees, rhythm in zip(
        __CHANT_ANCTUS_SANCTUS_PITCH_DEGREES, __CHANT_ANCTUS_SANCTUS_RHYTHMS
    )
)


# volume for stereo mixdown
GLITTER_VOLUME = 0.0475
VOICE_VOLUME = 1.6
DIVA_VOLUME = 0.22
NATURAL_RADIO_VOLUME = 0.085
SPEECH_VOLUME = 0.15
PERCUSSION_VOLUME = 0.68

GENERAL_FACTOR = 0.775

GLITTER_VOLUME *= GENERAL_FACTOR
VOICE_VOLUME *= GENERAL_FACTOR
DIVA_VOLUME *= GENERAL_FACTOR
NATURAL_RADIO_VOLUME *= GENERAL_FACTOR
SPEECH_VOLUME *= GENERAL_FACTOR
PERCUSSION_VOLUME *= GENERAL_FACTOR


PBIII_ORCHESTRATION = MU.Orchestration(
    # pianoteq voices
    MU.Track("voiceP0", VOICE_VOLUME * 1.4, 0),
    MU.Track("voiceP1", VOICE_VOLUME * 1.2, 0.4),
    MU.Track("voiceP2", VOICE_VOLUME, 0.8),
    MU.Track("voiceN0", VOICE_VOLUME * 1.4, 0.6),
    MU.Track("voiceN1", VOICE_VOLUME * 1.2, 1),
    MU.Track("voiceN2", VOICE_VOLUME, 0.2),
    # diva voices
    MU.Track("divaP0", DIVA_VOLUME, 0.6),
    MU.Track("divaP1", DIVA_VOLUME * 0.8, 1),
    MU.Track("divaP2", DIVA_VOLUME * 0.5, 0.2),
    MU.Track("divaN0", DIVA_VOLUME, 0),
    MU.Track("divaN1", DIVA_VOLUME * 0.8, 0.4),
    MU.Track("divaN2", DIVA_VOLUME * 0.5, 0.8),
    # common harmonics between two voices
    MU.Track("glitterP01", GLITTER_VOLUME, 0.2),
    MU.Track("glitterP02", GLITTER_VOLUME, 0.4),
    MU.Track("glitterP12", GLITTER_VOLUME, 0.6),
    MU.Track("glitterN01", GLITTER_VOLUME, 0.8),
    MU.Track("glitterN02", GLITTER_VOLUME, 0.4),
    MU.Track("glitterN12", GLITTER_VOLUME, 0.6),
    # natural radio samples
    MU.Track("natural_radio_0", NATURAL_RADIO_VOLUME, 0),
    MU.Track("natural_radio_1", NATURAL_RADIO_VOLUME, 0.2),
    MU.Track("natural_radio_2", NATURAL_RADIO_VOLUME, 0.4),
    MU.Track("natural_radio_3", NATURAL_RADIO_VOLUME, 0.6),
    MU.Track("natural_radio_4", NATURAL_RADIO_VOLUME, 0.8),
    MU.Track("natural_radio_5", NATURAL_RADIO_VOLUME, 1),
    # voice samples
    MU.Track("speech0", SPEECH_VOLUME, 0),
    MU.Track("speech1", SPEECH_VOLUME, 0.5),
    MU.Track("speech2", SPEECH_VOLUME, 1),
    # percussion samples
    MU.Track("percussion_P0", PERCUSSION_VOLUME, 0.4),
    MU.Track("percussion_P1", PERCUSSION_VOLUME, 0.8),
    MU.Track("percussion_P2", PERCUSSION_VOLUME, 0),
    MU.Track("percussion_N0", PERCUSSION_VOLUME, 1),
    MU.Track("percussion_N1", PERCUSSION_VOLUME, 0.2),
    MU.Track("percussion_N2", PERCUSSION_VOLUME, 0.6),
)

MU_NAME = "pbIII/build"


MALE_SOIL = soil.JICounterpoint()
FEMALE_SOIL = soil.JICounterpoint(harmonic_gender=False)


# DEFINING POSITIONS IN 6 CHANNEL MIX WHERE THE FIRST INDEX EQUALS THE FIRST
# VOICE IN THE RESPECTIVE GENDER
POSITIVE_VOICES_POSITION = (0, 2, 4)
NEGATIVE_VOICES_POSITIONS = (3, 5, 1)


###########################################################################
#   generate globals variables for the different available samples        #
###########################################################################


class _Samples(object):
    def __init__(self, dictionary_path: str, information: dict = {}) -> None:
        samples = tuple(
            natsort.natsorted(
                tuple(
                    "{}{}".format(dictionary_path, f)
                    for f in os.listdir(dictionary_path)
                    if f[-3:] == "wav"
                )
            )
        )
        self.__samples = samples
        self.__path = dictionary_path
        self.__information = information

    @property
    def information(self) -> dict:
        return self.__information

    def __repr__(self) -> str:
        return repr(self.__samples)

    def __iter__(self):
        return iter(self.__samples)

    def __getitem__(self, idx):
        return self.__samples[idx]


def _find_files(
    path: str, redundant: str = "pbIII/samples/", info_file_name: str = "info.txt"
):
    contain_files = False
    files = os.listdir(path)
    for f in files:
        complete_path = "{}{}".format(path, f)
        if os.path.isdir(complete_path):
            _find_files("{}/".format(complete_path), redundant)
        else:
            contain_files = True

    if contain_files:
        variable_name = "SAM_{}".format(
            re.sub("/", "_", path).upper()[len(redundant) : -1]
        )

        if info_file_name in files:
            with open("{}{}".format(path, info_file_name), "r") as f:
                pitch_name = f.readline()[:-1]
                frequency = abjad.NamedPitch(pitch_name).hertz
        else:
            frequency = None

        globals().update({variable_name: _Samples(path, {"frequency": frequency})})


_find_files("pbIII/samples/")
