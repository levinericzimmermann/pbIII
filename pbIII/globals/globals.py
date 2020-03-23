from mu.mel import ji

from mutools import MU

from pbIII.globals import soil

"""Defining global variables for the complete composition."""

CONCERT_PITCH = 240

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


# volume for stereo mixdown
GLITTER_VOLUME = 0.06
VOICE_VOLUME = 1.6
DIVA_VOLUME = 0.24
NATURAL_RADIO_VOLUME = 0.5

GENERAL_FACTOR = 1

GLITTER_VOLUME *= GENERAL_FACTOR
VOICE_VOLUME *= GENERAL_FACTOR
DIVA_VOLUME *= GENERAL_FACTOR
NATURAL_RADIO_VOLUME *= GENERAL_FACTOR

PBIII_ORCHESTRATION = MU.Orchestration(
    # pianoteq voices
    MU.Track("voiceP0", VOICE_VOLUME * 1.3, 0.6),
    MU.Track("voiceP1", VOICE_VOLUME * 1.1, 0.1),
    MU.Track("voiceP2", VOICE_VOLUME, 0.9),
    MU.Track("voiceN0", VOICE_VOLUME * 1.3, 0.4),
    MU.Track("voiceN1", VOICE_VOLUME * 1.1, 0.9),
    MU.Track("voiceN2", VOICE_VOLUME, 0.1),
    # diva voices
    MU.Track("divaP0", DIVA_VOLUME, 0.6),
    MU.Track("divaP1", DIVA_VOLUME * 0.7, 0.9),
    MU.Track("divaP2", DIVA_VOLUME * 0.4, 0.1),
    MU.Track("divaN0", DIVA_VOLUME, 0.4),
    MU.Track("divaN1", DIVA_VOLUME * 0.7, 0.1),
    MU.Track("divaN2", DIVA_VOLUME * 0.4, 0.9),
    # common harmonics between two voices
    MU.Track("glitterP01", GLITTER_VOLUME, 0.25),
    MU.Track("glitterP02", GLITTER_VOLUME, 0.75),
    MU.Track("glitterP12", GLITTER_VOLUME, 0.5),
    MU.Track("glitterN01", GLITTER_VOLUME, 0.75),
    MU.Track("glitterN02", GLITTER_VOLUME, 0.25),
    MU.Track("glitterN12", GLITTER_VOLUME, 0.5),
    # natural radio samples
    MU.Track("natural_radio_0", NATURAL_RADIO_VOLUME, 0),
    MU.Track("natural_radio_1", NATURAL_RADIO_VOLUME, 0.2),
    MU.Track("natural_radio_2", NATURAL_RADIO_VOLUME, 0.4),
    MU.Track("natural_radio_3", NATURAL_RADIO_VOLUME, 0.6),
    MU.Track("natural_radio_4", NATURAL_RADIO_VOLUME, 0.8),
    MU.Track("natural_radio_5", NATURAL_RADIO_VOLUME, 1),
    # voice samples
)

MU_NAME = "pbIII/build"


MALE_SOIL = soil.JICounterpoint()
FEMALE_SOIL = soil.JICounterpoint(harmonic_gender=False)
