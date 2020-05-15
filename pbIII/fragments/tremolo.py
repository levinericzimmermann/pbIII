"""special tremolo maker for pbIII similar to the one defined in mutools"""

from mu.sco import old
from mu.utils import infit


class TremoloMaker(object):
    def __init__(
        self,
        add_tremolo_decider: infit.InfIt = infit.ActivityLevel(6),
        tremolo_size_generator_per_tone: infit.MetaCycle = infit.MetaCycle(
            (infit.Addition, (10, 2))
        ),
        tremolo_volume_factor: float = 0.75,
        only_on_non_dissonant_pitches: bool = True,
    ):
        self.__add_tremolo_decider = add_tremolo_decider
        self.__tremolo_size_generator_per_tone = tremolo_size_generator_per_tone
        self.__tremolo_volume_factor = tremolo_volume_factor
        self.__only_on_non_dissonant_pitches = only_on_non_dissonant_pitches

    def __call__(
        self,
        melody: old.Melody,
        is_consonance_per_tone: tuple,
        spectrum_profile_per_tone: tuple,
    ) -> old.Melody:
        new_melody = old.Melody([])

        new_is_consonance_per_tone = []
        new_spectrum_profile_per_tone = []

        for tone, is_consonance, spectrum_profile in zip(
            melody, is_consonance_per_tone, spectrum_profile_per_tone
        ):
            new_is_consonance_per_tone.append(is_consonance)
            new_spectrum_profile_per_tone.append(spectrum_profile)

            test0 = is_consonance or not self.__only_on_non_dissonant_pitches
            test0 = test0 and not tone.pitch.is_empty

            if test0 and next(self.__add_tremolo_decider):
                rhythm = tone.delay
                duration_per_attack = []

                tremolo_size_generator = next(self.__tremolo_size_generator_per_tone)

                while sum(duration_per_attack) < rhythm:
                    duration_per_attack.append(next(tremolo_size_generator))

                if len(duration_per_attack) > 1:
                    duration_per_attack = duration_per_attack[:-1]
                    difference = rhythm - sum(duration_per_attack)
                    duration_per_attack[-1] += difference
                else:
                    difference = sum(duration_per_attack) - rhythm
                    duration_per_attack[-1] -= difference

                is_first = True
                for duration in duration_per_attack:
                    if not is_first:
                        new_spectrum_profile_per_tone.append(spectrum_profile)
                        new_is_consonance_per_tone.append(False)
                        volume = tone.volume * self.__tremolo_volume_factor
                    else:
                        volume = tone.volume

                    new_melody.append(
                        old.Tone(tone.pitch.copy(), duration, volume=volume)
                    )

                    is_first = False

            else:
                new_melody.append(tone.copy())

        return (
            new_melody,
            tuple(new_is_consonance_per_tone),
            tuple(new_spectrum_profile_per_tone),
        )
