from mutools import ambitus

from mu.mel import ji
from mu.utils import infit

from mutools import counterpoint

from pbIII.engines import speech
from pbIII.engines import pteq

from pbIII.fragments import harmony
from pbIII.segments import segments

NAME = "DS"

GENDER = False
GROUP = 2
# GROUP = 3
SUB_GROUP0 = 0

# high glitter
GENDER = False
GROUP = 3
SUB_GROUP0 = 0
PART = (
    segments.DensityBasedThreeVoiceCP(
        "{}_0".format(NAME),
        ambitus_maker=ambitus.SymmetricalRanges(ji.r(6, 1), ji.r(12, 5), ji.r(9, 4)),
        group=(GROUP, SUB_GROUP0, 0),
        start_harmony=harmony.find_harmony("A", True, 0, (1, 2), gender=GENDER),
        density_per_voice=(0.95, 0.64, 0.65),
        gender=GENDER,
        n_bars=3,
        duration_per_bar=7,
        start=0,
        dynamic_range_of_voices=(0.1, 0.2),
        anticipation_time=1.75,
        overlaying_time=1.25,
        cp_add_dissonant_pitches_to_nth_voice=(False, False, True),
        cp_constraints_harmonic=(
            counterpoint.constraints.HR_forbid_too_empty_harmonies(1, [0]),
        ),
        cp_constraints_interpolation=[],
        glitter_include_dissonant_pitches=False,
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(
                fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                preset=None,
                empty_attack_dynamic_maker=infit.Value(0),
            ),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0)),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0)),
        ),
        speech_init_attributes={},
        include_glitter=True,
        include_diva=False,
        include_natural_radio=True,
        radio_silent_channels=(1, 3, 5),
        radio_samples=(
            "pbIII/samples/radio/carolina/3.wav",
            "pbIII/samples/radio/carolina/1.wav",
        ),
        radio_n_changes=1,
        radio_average_volume=0.385,
        radio_shadow_time=0.2,
        radio_min_volume=0.925,
    ),
    segments.DensityBasedThreeVoiceCP(
        "{}_1".format(NAME),
        ambitus_maker=ambitus.SymmetricalRanges(ji.r(16, 5), ji.r(5, 2), ji.r(8, 5)),
        group=(GROUP, SUB_GROUP0, 1),
        start_harmony=harmony.find_harmony("A", True, 0, (0,), gender=GENDER),
        density_per_voice=(0, 0.6, 0.6),
        gender=GENDER,
        n_bars=1,
        duration_per_bar=10,
        start=1.25,
        dynamic_range_of_voices=(0.15, 0.45),
        anticipation_time=0.8,
        overlaying_time=0.5,
        cp_constraints_harmonic=(
            counterpoint.constraints.HR_forbid_too_empty_harmonies(1, [0]),
        ),
        cp_constraints_interpolation=[],
        cp_add_dissonant_pitches_to_nth_voice=(False, False, False),
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0)),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0)),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0)),
        ),
        speech_init_attributes={},
        include_glitter=True,
        include_diva=False,
        include_natural_radio=True,
        radio_silent_channels=(1, 3, 5),
        radio_samples=(
            "pbIII/samples/radio/carolina/3.wav",
            "pbIII/samples/radio/carolina/1.wav",
        ),
        radio_n_changes=0,
        radio_average_volume=0.2,
        radio_shadow_time=0.175,
        radio_min_volume=0.875,
        glitter_include_dissonant_pitches=False,
    ),
    segments.DensityBasedThreeVoiceCP(
        "{}_2".format(NAME),
        ambitus_maker=ambitus.SymmetricalRanges(ji.r(6, 1), ji.r(5, 2), ji.r(9, 4)),
        group=(GROUP, SUB_GROUP0, 2),
        start_harmony=harmony.find_harmony("A", True, 0, (0,), gender=GENDER),
        density_per_voice=(0.775, 1, 1),
        gender=GENDER,
        n_bars=3,
        duration_per_bar=7,
        start=4.5,
        dynamic_range_of_voices=(0.1, 0.2),
        anticipation_time=1.25,
        overlaying_time=1.25,
        cp_add_dissonant_pitches_to_nth_voice=(False, False, True),
        cp_constraints_harmonic=(
            counterpoint.constraints.HR_forbid_too_empty_harmonies(1, [0]),
        ),
        cp_constraints_interpolation=[],
        glitter_include_dissonant_pitches=False,
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(
                fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                preset=None,
                empty_attack_dynamic_maker=infit.Value(0),
            ),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0)),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0)),
        ),
        speech_init_attributes={},
        include_glitter=True,
        include_diva=False,
        include_natural_radio=True,
        radio_silent_channels=(1, 3, 5),
        radio_samples=(
            "pbIII/samples/radio/carolina/3.wav",
            "pbIII/samples/radio/carolina/1.wav",
        ),
        radio_n_changes=1,
        radio_average_volume=0.285,
        radio_shadow_time=0.2,
        radio_min_volume=0.925,
    ),
    segments.Chord(
        "{}_3".format(NAME),
        ambitus_maker=ambitus.SymmetricalRanges(ji.r(8, 1), ji.r(5, 2), ji.r(9, 4)),
        group=(GROUP, SUB_GROUP0 + 1, 0),
        chord=harmony.find_harmony(gender=GENDER),
        gender=GENDER,
        n_bars=1,
        duration_per_bar=6,
        start=1.25,
        dynamic_range_of_voices=(0.04, 0.1),
        anticipation_time=1.25,
        overlaying_time=1.25,
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(
                fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                preset=None,
                empty_attack_dynamic_maker=infit.Value(0),
            ),
            pteq.mk_dreamy_pte(
                fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                preset=None,
                empty_attack_dynamic_maker=infit.Value(0),
            ),
            pteq.mk_dreamy_pte(
                fxp='"pbIII/fxp/VibraphoneV-BHumanizednostretching.fxp"',
                preset=None,
                empty_attack_dynamic_maker=infit.Value(0),
            ),
        ),
        speech_init_attributes={},
        include_glitter=True,
        include_diva=False,
        include_natural_radio=True,
        radio_silent_channels=(1,),
        radio_samples=(
            "pbIII/samples/radio/carolina/3.wav",
            "pbIII/samples/radio/carolina/1.wav",
        ),
        radio_n_changes=0,
        radio_average_volume=0.45,
        radio_shadow_time=0.35,
        radio_min_volume=0.7,
    ),
)


"""
# chords
GENDER = False
GROUP = 3
SUB_GROUP0 = 0
PART = (
    segments.FreeStyleCP(
        "{}_0".format(NAME),
        ambitus_maker=ambitus.SymmetricalRanges(ji.r(1, 1), ji.r(3, 1), ji.r(5, 4)),
        energy_per_voice=(6, 7, 7),
        weight_range=(3, 10),
        silence_decider_per_voice=(
            infit.ActivityLevel(0),
            infit.ActivityLevel(0),
            infit.ActivityLevel(0),
        ),
        group=(GROUP, SUB_GROUP0, 0),
        start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=GENDER),
        gender=GENDER,
        n_bars=1,
        duration_per_bar=25,
        start=0,
        metrical_numbers=(12, 12, 12),
        dynamic_range_of_voices=(0.1, 0.65),
        anticipation_time=1.75,
        overlaying_time=1.25,
        cp_add_dissonant_pitches_to_nth_voice=(True, True, True),
        cp_constraints_harmonic=(
            counterpoint.constraints.HR_forbid_too_empty_harmonies(1, [0]),
        ),
        cp_constraints_interpolation=[],
        glitter_include_dissonant_pitches=False,
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.1)),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.1)),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.1)),
        ),
        include_glitter=True,
        include_diva=True,
        include_natural_radio=True,
        radio_silent_channels=(1, 5),
        radio_samples=(
            "pbIII/samples/radio/carolina/3.wav",
            "pbIII/samples/radio/carolina/1.wav",
        ),
        radio_n_changes=2,
        radio_average_volume=0.385,
        radio_shadow_time=0.2,
        radio_min_volume=0.925,
        speech_init_attributes={
            "voice0": {
                "start": 5.85,
                "duration": 22.5,
                "sound_engine": speech.Sampler(
                    "pbIII/samples/speech/ghost_dance/ghost_dance_quote0_noise_reduction0.wav",
                    21.195,
                    volume=0.92,
                ),
            },
            "voice2": {
                "start": 5.88,
                "duration": 22.5,
                "sound_engine": speech.Sampler(
                    "pbIII/samples/speech/ghost_dance/ghost_dance_quote0_noise_reduction0.wav",
                    21.195,
                    volume=0.95,
                ),
            },
        },
    ),
)
"""

"""
# floating counterpoint
GENDER = False
GROUP = 2
SUB_GROUP0 = 0
PART = (
    # with random call
    segments.FreeStyleCP(
        "{}_0".format(NAME),
        ambitus_maker=ambitus.SymmetricalRanges(ji.r(1, 1), ji.r(3, 1), ji.r(5, 4)),
        decision_type="random",
        random_seed=1000,
        energy_per_voice=(8.87, 6, 6),
        weight_range=(0.6, 1),
        metrical_numbers=(3, 9, 12),
        silence_decider_per_voice=(
            infit.ActivityLevel(1),
            infit.ActivityLevel(1),
            infit.ActivityLevel(1),
        ),
        group=(GROUP, SUB_GROUP0, 0),
        start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=GENDER),
        gender=GENDER,
        n_bars=6,
        duration_per_bar=3,
        start=0,
        dynamic_range_of_voices=(0.075, 0.785),
        anticipation_time=0.3,
        overlaying_time=0.35,
        cp_add_dissonant_pitches_to_nth_voice=(True, True, False),
        glitter_include_dissonant_pitches=True,
        glitter_modulater_per_voice=("randomh", "randomh", "randomh"),
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.2)),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.2)),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.2)),
        ),
        speech_init_attributes={},
        include_glitter=True,
        include_diva=False,
        include_natural_radio=True,
        radio_silent_channels=(1, 3, 5),
        radio_samples=(
            "pbIII/samples/radio/carolina/3.wav",
            "pbIII/samples/radio/carolina/1.wav",
        ),
        radio_n_changes=1,
        radio_average_volume=0.095,
        radio_shadow_time=0.085,
        radio_min_volume=0.825,
    ),
    # with activity level
    segments.FreeStyleCP(
        "{}_1".format(NAME),
        ambitus_maker=ambitus.SymmetricalRanges(ji.r(1, 1), ji.r(3, 1), ji.r(5, 4)),
        decision_type="activity",
        energy_per_voice=(10, 10, 10),
        weight_range=(2, 10),
        metrical_numbers=(6, 12, 18),
        silence_decider_per_voice=(
            infit.ActivityLevel(1),
            infit.ActivityLevel(1),
            infit.ActivityLevel(1),
        ),
        group=(GROUP, SUB_GROUP0, 0),
        start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=GENDER),
        gender=GENDER,
        n_bars=3,
        duration_per_bar=7,
        start=2,
        dynamic_range_of_voices=(0.1, 0.95),
        anticipation_time=0.2,
        overlaying_time=0.25,
        cp_add_dissonant_pitches_to_nth_voice=(False, True, False),
        glitter_include_dissonant_pitches=True,
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(
                preset='"J. Schantz"',
                empty_attack_dynamic_maker=infit.Value(0.2),
            ),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.2)),
            pteq.mk_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.2)),
        ),
        speech_init_attributes={},
        include_glitter=True,
        include_diva=False,
        include_natural_radio=True,
        voices_overlaying_time=5,
        radio_silent_channels=(1, 3, 5),
        radio_samples=(
            "pbIII/samples/radio/carolina/3.wav",
            "pbIII/samples/radio/carolina/1.wav",
        ),
        radio_n_changes=1,
        radio_average_volume=0.095,
        radio_shadow_time=0.085,
        radio_min_volume=0.825,
    ),
)
"""
