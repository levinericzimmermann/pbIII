from mutools import ambitus
from mutools import counterpoint

from mu.mel import ji
from mu.utils import infit
from mu.utils import interpolations

from pbIII.engines import percussion
from pbIII.engines import pteq
from pbIII.engines import speech

from pbIII.fragments import harmony
from pbIII.segments import segments

from pbIII.globals import globals


def make(name: str = "ONE", gender=False, group=0, sub_group0=1):
    return (
        segments.Silence(name="{}_start_silence".format(name), duration=18),
        segments.Chord(
            "{}_Speech0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(7, 1), ji.r(2, 1), ji.r(4, 3)),
            group=(group, sub_group0, 0),
            chord=harmony.find_harmony(name="A", gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=34,
            start=0,
            dynamic_range_of_voices=(0.8, 1),
            anticipation_time=2.25,
            overlaying_time=3.25,
            speech_init_attributes={
                "speech0": {
                    "start": 0,
                    "duration": 35,
                    "sound_engine": speech.BrokenRadio(
                        (globals.SAM_SPEECH_SLICED_DERRIDA_KAFKA.path,),
                        duration=32,
                        volume=0.42,
                        activity_lv_per_effect={
                            "original": 8,
                            "harmonizer": 6,
                            "filter": 10,
                            "noise": 10,
                            "lorenz": 10,
                            "chenlee": 6,
                        },
                        level_per_effect={
                            "original": infit.Gaussian(0.4, 0.05),
                            "filter": infit.Gaussian(10.2, 2.25),
                            "harmonizer": infit.Gaussian(0.7, 0.15),
                            "chenlee": infit.Gaussian(0.1, 0.02),
                            "lorenz": infit.Gaussian(0.4, 0.02),
                            "noise": infit.Gaussian(0.32, 0.04),
                        },
                        transpo_maker=infit.Uniform(0.14, 0.8),
                        filter_freq_maker=infit.Gaussian(110, 50),
                        filter_q_maker=infit.Gaussian(5, 1),
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
                "speech1": {
                    "start": 0.1,
                    "duration": 35,
                    "sound_engine": speech.BrokenRadio(
                        (globals.SAM_SPEECH_SLICED_DERRIDA_KAFKA.path,),
                        duration=32,
                        volume=0.3,
                        activity_lv_per_effect={
                            "original": 6,
                            "harmonizer": 4,
                            "filter": 9,
                            "noise": 9,
                            "lorenz": 8,
                            "chenlee": 7,
                        },
                        level_per_effect={
                            "original": infit.Gaussian(0.4, 0.05),
                            "filter": infit.Gaussian(10.2, 2.25),
                            "harmonizer": infit.Gaussian(0.7, 0.15),
                            "chenlee": infit.Gaussian(0.1, 0.02),
                            "lorenz": infit.Gaussian(0.4, 0.02),
                            "noise": infit.Gaussian(0.32, 0.04),
                        },
                        transpo_maker=infit.Uniform(1.14, 1.5),
                        filter_freq_maker=infit.Gaussian(200, 50),
                        filter_q_maker=infit.Gaussian(5, 1),
                        curve=interpolations.InterpolationLine(
                            [
                                interpolations.FloatInterpolationEvent(0.3, 0.01),
                                interpolations.FloatInterpolationEvent(0.8, 1),
                                interpolations.FloatInterpolationEvent(0.3, 1),
                                interpolations.FloatInterpolationEvent(0, 0.1),
                            ]
                        ),
                    ),
                },
                "speech2": {
                    "start": 0.075,
                    "duration": 35,
                    "sound_engine": speech.BrokenRadio(
                        (globals.SAM_SPEECH_SLICED_DERRIDA_KAFKA.path,),
                        duration=32,
                        volume=0.34,
                        activity_lv_per_effect={
                            "original": 6,
                            "harmonizer": 4,
                            "filter": 9,
                            "noise": 9,
                            "lorenz": 8,
                            "chenlee": 7,
                        },
                        level_per_effect={
                            "original": infit.Gaussian(0.4, 0.05),
                            "filter": infit.Gaussian(10.2, 2.25),
                            "harmonizer": infit.Gaussian(0.7, 0.15),
                            "chenlee": infit.Gaussian(0.1, 0.02),
                            "lorenz": infit.Gaussian(0.4, 0.02),
                            "noise": infit.Gaussian(0.32, 0.04),
                        },
                        transpo_maker=infit.Uniform(1.14, 1.5),
                        filter_freq_maker=infit.Gaussian(200, 50),
                        filter_q_maker=infit.Gaussian(5, 1),
                        curve=interpolations.InterpolationLine(
                            [
                                interpolations.FloatInterpolationEvent(0.4, 0.01),
                                interpolations.FloatInterpolationEvent(0.8, 1),
                                interpolations.FloatInterpolationEvent(0.3, 1),
                                interpolations.FloatInterpolationEvent(0, 0.1),
                            ]
                        ),
                    ),
                },
            },
            include_glitter=False,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
            include_voices=False,
        ),
    )
