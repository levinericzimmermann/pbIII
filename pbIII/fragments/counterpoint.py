import itertools

from mu.mel import ji

from mutools import counterpoint

from pbIII.globals import globals


class ThreeVoiceRhythmicCP(counterpoint.RhythmicCP):
    def __init__(
        self,
        rhythm_per_voice: tuple,
        gender: bool = True,
        weight_per_beat=None,
        constraints_harmonic_resolution: tuple = tuple([]),
        constraints_added_pitches: tuple = tuple([]),
    ):
        super().__init__(
            self.mk_harmonies(gender),
            rhythm_per_voice,
            weights_per_beat=weight_per_beat,
            constraints_harmonic_resolution=constraints_harmonic_resolution,
            constraints_added_pitches=constraints_added_pitches,
        )

    @staticmethod
    def mk_harmonies(gender: tuple) -> tuple:
        empty_tuple = tuple([])

        harmonies = []
        for harmony in globals.BLUEPRINT_HARMONIES:
            harmony = globals.BLUEPRINT_HARMONIES[harmony]
            dissonant_pitches = harmony[1]
            useable_harmonies = harmony[0][0] + harmony[0][1]
            for inner_harmony_or_substitue in useable_harmonies:
                harmonies.append(
                    (inner_harmony_or_substitue, empty_tuple, dissonant_pitches)
                )
                for n_empty_pitches in range(1, 3):
                    for empty_pitches in itertools.combinations(
                        tuple(range(3)), n_empty_pitches
                    ):
                        new_blueprint_harmony = ji.BlueprintHarmony(
                            *tuple(
                                p
                                for p_idx, p in enumerate(
                                    inner_harmony_or_substitue.blueprint
                                )
                                if p_idx not in empty_pitches
                            )
                        )
                        harmonies.append(
                            (new_blueprint_harmony, empty_pitches, dissonant_pitches)
                        )

        if not gender:
            harmonies = tuple((h[0].inverse(), h[1], h[2].inverse()) for h in harmonies)

        return tuple(harmonies)
