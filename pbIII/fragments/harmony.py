from mu.mel import ji

from pbIII.globals import globals


def find_harmony(
    name: str = "A",
    use_main_harmony: bool = True,
    idx: int = 0,
    empty_voices: tuple = tuple([]),
) -> tuple:
    harmony = globals.BLUEPRINT_HARMONIES[name]
    dissonant_pitches = harmony[-1]
    bp_harmony = harmony[0][not use_main_harmony][idx]
    bp_harmony = ji.BlueprintHarmony(
        *tuple(
            pitch
            for vox_idx, pitch in enumerate(bp_harmony.blueprint)
            if vox_idx not in empty_voices
        )
    )
    return (bp_harmony, empty_voices, dissonant_pitches)
