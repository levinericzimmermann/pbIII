from mu.utils import infit
from mu.utils import interpolations

from mutools import ambitus

from mu.mel import ji

from mutools import counterpoint

from pbIII.engines import pteq
from pbIII.engines import speech

from pbIII.fragments import harmony
from pbIII.segments import segments

GROUP0 = 4
SUB_GROUP0 = 1
# SUB_GROUP0 = 0

GENDER = False

PART = (
    segments.DensityBasedThreeVoiceCP(
        "part0_0",
        # ambitus_maker=ambitus.SymmetricalRanges(ji.r(4, 1), ji.r(5, 2), ji.r(5, 4)),
        group=(GROUP0, SUB_GROUP0, 0),
        start_harmony=harmony.find_harmony("A", True, 0, (1, 2), gender=GENDER),
        density_per_voice=(0.75, 0.95, 0.875),
        gender=GENDER,
        n_bars=3,
        duration_per_bar=19,
        dynamic_range_of_voices=(0.285, 0.9),
        anticipation_time=1,
        overlaying_time=1,
        cp_constraints_harmonic=(
            counterpoint.constraints.HR_forbid_too_empty_harmonies(1, [0]),
            # counterpoint.constraints.HR_nth_voice_contain_all_possible_pitches(2),
        ),
        cp_constraints_interpolation=(
            counterpoint.constraints.AP_tremolo(
                1, add_tremolo_decider=infit.ActivityLevel(4)
            ),
            counterpoint.constraints.AP_tremolo(
                2,
                add_tremolo_decider=infit.ActivityLevel(3),
                tremolo_size_generator_per_tone=infit.MetaCycle(
                    (infit.Multiplication, (2, 2)),
                    (infit.Addition, (4, 15)),
                    (infit.Power, (2, 2)),
                ),
            ),
        ),
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
        ),
        # curve_per_voice=((0, 1, 1, 0), (0.15, 1, 1, 0), (0.25, 1, 1, 0)),
        curve_per_voice=((0, 1, 1, 0), (0.1, 1, 1, 0), (0.15, 1, 1, 0)),
        tracks2ignore=("voice0", "voice1", "voice2"),
        speech_init_attributes={
            "voice0": {
                "start": 1.26,
                "duration": 85,
                "sound_engine": speech.BrokenRadio(
                    ("pbIII/samples/speech/sliced/fisher/0/",),
                    duration=85,
                    volume=0.25,
                    activity_lv_per_effect={
                        "original": 7,
                        "harmonizer": 6,
                        "filter": 9,
                        "noise": 10,
                        "lorenz": 10,
                        "chenlee": 5,
                    },
                    level_per_effect={
                        "original": infit.Gaussian(0.1, 0.05),
                        "filter": infit.Gaussian(14.2, 3.25),
                        "harmonizer": infit.Gaussian(0.2, 0.15),
                        "chenlee": infit.Gaussian(0.04, 0.02),
                        "lorenz": infit.Gaussian(0.05, 0.02),
                        "noise": infit.Gaussian(0.08, 0.04),
                    },
                    transpo_maker=infit.Uniform(0.34, 0.9),
                    filter_freq_maker=infit.Gaussian(110, 50),
                    filter_q_maker=infit.Gaussian(23, 5),
                    curve=interpolations.InterpolationLine(
                        [
                            interpolations.FloatInterpolationEvent(0.25, 0.01),
                            interpolations.FloatInterpolationEvent(0.8, 1),
                            interpolations.FloatInterpolationEvent(0.3, 1),
                            interpolations.FloatInterpolationEvent(0, 0.1),
                        ]
                    ),
                ),
            },
            "voice2": {
                "start": 1.29,
                "duration": 80,
                "sound_engine": speech.BrokenRadio(
                    ("pbIII/samples/speech/sliced/fisher/0/",),
                    duration=80,
                    volume=0.25,
                    activity_lv_per_effect={
                        "original": 8,
                        "harmonizer": 3,
                        "ringmodulation": 4,
                        "filter": 9,
                        "noise": 10,
                        "lorenz": 7,
                        "chenlee": 6,
                    },
                    level_per_effect={
                        "original": infit.Gaussian(0.04, 0.03),
                        "filter": infit.Gaussian(14, 3.35),
                        "harmonizer": infit.Gaussian(0.3, 0.2),
                        "ringmodulation": infit.Gaussian(0.1, 0.085),
                        "chenlee": infit.Gaussian(0.1, 0.04),
                        "lorenz": infit.Gaussian(0.03, 0.02),
                        "noise": infit.Gaussian(0.08, 0.04),
                    },
                    curve=interpolations.InterpolationLine(
                        [
                            interpolations.FloatInterpolationEvent(0.25, 0.01),
                            interpolations.FloatInterpolationEvent(0.8, 1),
                            interpolations.FloatInterpolationEvent(0.3, 1),
                            interpolations.FloatInterpolationEvent(0, 0.1),
                        ]
                    ),
                    transpo_maker=infit.Uniform(0.24, 1.5),
                    rm_freq_maker=infit.Gaussian(180, 30),
                    filter_freq_maker=infit.Gaussian(120, 50),
                    filter_q_maker=infit.Gaussian(13, 3),
                ),
            },
        },
        include_natural_radio=True,
        radio_silent_channels=(0, 2, 5),
        radio_n_changes=5,
        radio_average_volume=0.2,
        radio_shadow_time=0.12,
        radio_min_volume=0.7,
    ),
    segments.DensityBasedThreeVoiceCP(
        "part0_0B",
        ambitus_maker=ambitus.SymmetricalRanges(ji.r(4, 3), ji.r(3, 1), ji.r(5, 4)),
        group=(GROUP0, SUB_GROUP0, 1),
        # start_harmony=harmony.find_harmony("A", True, 0, (1, 2), gender=GENDER),
        density_per_voice=(0.6, 0.95, 0.875),
        gender=GENDER,
        n_bars=2,
        duration_per_bar=19,
        dynamic_range_of_voices=(0.225, 0.875),
        anticipation_time=1,
        overlaying_time=1,
        cp_constraints_harmonic=(
            counterpoint.constraints.HR_forbid_too_empty_harmonies(1, [0]),
            # counterpoint.constraints.HR_nth_voice_contain_all_possible_pitches(2),
        ),
        cp_constraints_interpolation=(
            counterpoint.constraints.AP_tremolo(
                1, add_tremolo_decider=infit.ActivityLevel(4)
            ),
            counterpoint.constraints.AP_tremolo(
                2,
                add_tremolo_decider=infit.ActivityLevel(3),
                tremolo_size_generator_per_tone=infit.MetaCycle(
                    (infit.Multiplication, (2, 2)),
                    (infit.Addition, (4, 15)),
                    (infit.Power, (2, 2)),
                ),
            ),
        ),
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
        ),
        # curve_per_voice=((0, 1, 1, 0), (0.15, 1, 1, 0), (0.25, 1, 1, 0)),
        curve_per_voice=((0, 1, 1, 0), (0, 1, 1, 0), (0, 1, 1, 0)),
        include_natural_radio=True,
        radio_silent_channels=(1, 3, 5),
        radio_n_changes=5,
        radio_average_volume=0.2,
        radio_shadow_time=0.12,
        radio_min_volume=0.7,
    ),
    segments.Chord(
        "chordTEST_pre2",
        chord=harmony.find_harmony(gender=GENDER),
        dynamic_range_of_voices=(0.1, 0.7),
        group=(GROUP0, SUB_GROUP0, 1),
        start=-1,
        gender=GENDER,
        n_bars=1,
        duration_per_bar=2.75,
        anticipation_time=0.75,
        overlaying_time=0.85,
        include_diva=False,
        radio_silent_channels=(0, 2, 5),
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
        ),
    ),
    segments.DensityBasedThreeVoiceCP(
        "part0_1",
        # ambitus_maker=ambitus.SymmetricalRanges(ji.r(4, 1), ji.r(5, 2), ji.r(5, 4)),
        density_per_voice=(0.9, 0.95, 0.775),
        dynamic_range_of_voices=(0.225, 0.9),
        # curve_per_voice=((0, 1, 1, 0.5), (0, 1, 1, 0.6), (0, 1, 1, 0.2)),
        curve_per_voice=((0, 1, 1, 0), (0, 1, 1, 0), (0, 1, 1, 0)),
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
        ),
        glitter_modulater_per_voice=("randomh", "randomh", "randomh"),
        group=(GROUP0, SUB_GROUP0, 2),
        start=0,
        gender=GENDER,
        n_bars=2,
        duration_per_bar=19,
        anticipation_time=0.75,
        overlaying_time=1,
        cp_constraints_harmonic=(
            counterpoint.constraints.HR_forbid_too_empty_harmonies(1),
        ),
        cp_constraints_interpolation=(
            counterpoint.constraints.AP_tremolo(
                2,
                add_tremolo_decider=infit.ActivityLevel(5),
                tremolo_size_generator_per_tone=infit.MetaCycle(
                    (infit.Multiplication, (2, 2)),
                    (infit.Addition, (15, 8)),
                    (infit.Addition, (8, 10)),
                ),
            ),
        ),
        # include_diva=False,
        include_glitter=True,
        include_natural_radio=True,
        radio_silent_channels=(0, 2, 5, 6),
    ),
    segments.DensityBasedThreeVoiceCP(
        "part0_1B",
        # ambitus_maker=ambitus.SymmetricalRanges(ji.r(4, 1), ji.r(5, 2), ji.r(5, 4)),
        ambitus_maker=ambitus.SymmetricalRanges(ji.r(3, 4), ji.r(3, 1), ji.r(5, 4)),
        density_per_voice=(0.9, 0.95, 0.85),
        dynamic_range_of_voices=(0.225, 0.9),
        # curve_per_voice=((0, 1, 1, 0.5), (0, 1, 1, 0.6), (0, 1, 1, 0.2)),
        # curve_per_voice=((0, 1, 1, 0.2), (0, 1, 1, 0.3), (0, 1, 1, 0.1)),
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
        ),
        group=(GROUP0, SUB_GROUP0 + 1, 0),
        start=0,
        gender=GENDER,
        n_bars=2,
        duration_per_bar=15,
        anticipation_time=0.75,
        overlaying_time=1,
        cp_constraints_harmonic=(
            counterpoint.constraints.HR_forbid_too_empty_harmonies(1),
        ),
        cp_constraints_interpolation=(
            counterpoint.constraints.AP_tremolo(
                2,
                add_tremolo_decider=infit.ActivityLevel(5),
                tremolo_size_generator_per_tone=infit.MetaCycle(
                    (infit.Multiplication, (2, 2)),
                    (infit.Addition, (15, 8)),
                    (infit.Addition, (8, 10)),
                ),
            ),
        ),
        # include_diva=False,
        include_glitter=True,
        include_natural_radio=True,
        radio_silent_channels=(0, 2, 5, 6),
    ),
    segments.Chord(
        "chordTEST1",
        chord=harmony.find_harmony("C", True, 0, (0,), gender=GENDER),
        group=(GROUP0, SUB_GROUP0 + 1, 1),
        dynamic_range_of_voices=(0.1, 0.45),
        start=0,
        gender=GENDER,
        n_bars=1,
        duration_per_bar=3,
        anticipation_time=1,
        overlaying_time=0.25,
        include_diva=False,
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
        ),
    ),
    segments.Chord(
        "chordTEST2",
        chord=harmony.find_harmony("A", True, 0, (0,), gender=GENDER),
        dynamic_range_of_voices=(0.1, 0.4),
        group=(GROUP0, SUB_GROUP0 + 1, 1),
        start=0,
        gender=GENDER,
        n_bars=1,
        duration_per_bar=4,
        anticipation_time=1,
        overlaying_time=1,
        include_diva=True,
        pteq_engine_per_voice=(
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
            pteq.mk_dreamy_pte(),
        ),
        speech_init_attributes={
            "voice1": {
                "start": 1.25,
                "duration": 31,
                "sound_engine": speech.BrokenRadio(
                    (
                        "pbIII/samples/speech/sliced/weather_forecast/english0/",
                        "pbIII/samples/speech/sliced/weather_forecast/english2/",
                    ),
                    skip_n_samples_per_source=(0, 0),
                    duration=30,
                    volume=0.45,
                    order_per_source=("shuffle", "shuffle"),
                    interlocking="sequential",
                    activity_lv_per_effect={
                        "noise": 10,
                        "chenlee": 7,
                        "lorenz": 10,
                        "filter": 10,
                        "ringmodulation": 4,
                    },
                    level_per_effect={
                        "original": infit.Gaussian(0.3, 0.15),
                        "filter": infit.Gaussian(1.6, 0.25),
                        "harmonizer": infit.Gaussian(0.5, 0.2),
                        "ringmodulation": infit.Gaussian(0.3, 0.2),
                        "noise": infit.Gaussian(0.5, 0.1),
                        "chenlee": infit.Gaussian(0.2, 0.2),
                        "lorenz": infit.Gaussian(0.4, 0.2),
                    },
                    transpo_maker=infit.Uniform(0.14, 0.5),
                    filter_freq_maker=infit.Gaussian(120, 50),
                    filter_q_maker=infit.Gaussian(18, 4),
                    curve=interpolations.InterpolationLine(
                        [
                            interpolations.FloatInterpolationEvent(0.2, 0.01),
                            interpolations.FloatInterpolationEvent(0.8, 1),
                            interpolations.FloatInterpolationEvent(0.2, 1),
                            interpolations.FloatInterpolationEvent(0, 0.1),
                        ]
                    ),
                ),
            }
        },
    ),
)
