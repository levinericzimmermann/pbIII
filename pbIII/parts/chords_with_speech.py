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
        segments.FreeStyleCP(
            "{}_chords0".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(1, 1), ji.r(3, 1), ji.r(5, 4)),
            energy_per_voice=(6, 7, 7),
            weight_range=(0, 6),
            silence_decider_per_voice=(
                infit.ActivityLevel(0),
                infit.ActivityLevel(0),
                infit.ActivityLevel(0),
            ),
            group=(group, sub_group0, 0),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            gender=gender,
            n_bars=1,
            duration_per_bar=22,
            start=4,
            metrical_numbers=(12, 12, 12),
            dynamic_range_of_voices=(0.6, 0.8),
            anticipation_time=0.2,
            overlaying_time=1.25,
            cp_add_dissonant_pitches_to_nth_voice=(True, True, False),
            pteq_engine_per_voice=(
                pteq.mk_super_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.1)),
                pteq.mk_super_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.1)),
                pteq.mk_super_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.1)),
            ),
            percussion_engine_per_voice=(
                percussion.Rhythmizer(
                    voice_meters2occupy=(0,),
                    likelihood_range=(0.1, 0.6),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=True,
                    seed=100,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(1,),
                    # likelihood_range=(0.1, 0.8),
                    likelihood_range=(0, 0.1),
                    volume_range=(0.1, 1),
                    ignore_beats_occupied_by_voice=True,
                    seed=1000,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(2,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_SPEECH_SPACE),
                                pitch_factor=infit.Uniform(0.9, 1.2),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_SPEECH_TIME),
                                pitch_factor=infit.Uniform(0.9, 1.2),
                            ),
                        )
                    ),
                    # likelihood_range=(1, 0.2),
                    likelihood_range=(0, 0.1),
                    volume_range=(0.1, 0.3),
                    ignore_beats_occupied_by_voice=True,
                ),
            ),
            include_glitter=False,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=False,
            radio_silent_channels=(1, 5),
            radio_samples=(
                "pbIII/samples/radio/carolina/3.wav",
                "pbIII/samples/radio/carolina/1.wav",
            ),
            radio_n_changes=2,
            radio_average_volume=0.1,
            radio_shadow_time=0.2,
            radio_min_volume=0.825,
            # speech_init_attributes={
            #     "speech0": {
            #         "start": 5.85,
            #         "duration": 22.5,
            #         "sound_engine": speech.Sampler(
            #             "pbIII/samples/speech/ghost_dance/ghost_dance_quote0_noise_reduction0.wav",
            #             volume=0.58,
            #         ),
            #     },
            #     "speech2": {
            #         "start": 3,
            #         "duration": 37.5,
            #         "sound_engine": speech.Sampler(
            #             globals.SAM_SPEECH_IAN_CURTIS[2], volume=1
            #         ),
            #     },
            # },
        ),
        segments.FreeStyleCP(
            "{}_chords1".format(name),
            ambitus_maker=ambitus.SymmetricalRanges(ji.r(1, 1), ji.r(3, 1), ji.r(5, 4)),
            energy_per_voice=(3, 2, 2),
            weight_range=(0, 6),
            silence_decider_per_voice=(
                infit.ActivityLevel(0),
                infit.ActivityLevel(0),
                infit.ActivityLevel(0),
            ),
            group=(group, sub_group0, 1),
            start_harmony=harmony.find_harmony("A", True, 0, tuple([]), gender=gender),
            gender=gender,
            n_bars=2,
            duration_per_bar=11,
            start=2,
            metrical_numbers=(6, 12, 18),
            dynamic_range_of_voices=(0.6, 0.8),
            anticipation_time=0.2,
            overlaying_time=1.25,
            cp_add_dissonant_pitches_to_nth_voice=(True, True, False),
            pteq_engine_per_voice=(
                pteq.mk_super_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.1)),
                pteq.mk_super_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.1)),
                pteq.mk_super_dreamy_pte(empty_attack_dynamic_maker=infit.Value(0.1)),
            ),
            percussion_engine_per_voice=(
                percussion.Rhythmizer(
                    voice_meters2occupy=(0,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1)),
                                distortion=infit.Uniform(0, 1),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1)),
                                distortion=infit.Uniform(0, 1),
                            ),
                        )
                    ),
                    likelihood_range=(0.3, 1),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(1,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 0.5, 1, 0.25, 1)),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1)),
                                distortion=infit.Uniform(0, 1),
                            ),
                        )
                    ),
                    likelihood_range=(0.3, 1),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=False,
                ),
                percussion.Rhythmizer(
                    voice_meters2occupy=(2,),
                    sample_maker=infit.Cycle(
                        (
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_LOW_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_LOW_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1)),
                                distortion=infit.Uniform(0, 1),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(
                                    globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET
                                ),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_MALLET.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((0.5, 1, 0.25, 1)),
                            ),
                            percussion.Sample(
                                path=infit.Cycle(globals.SAM_KENDANG_HIGH_LOW_FAR_HAND),
                                frequency=globals.SAM_KENDANG_HIGH_LOW_FAR_HAND.information[
                                    "frequency"
                                ],
                                pitch_factor=infit.Cycle((1, 1, 0.5, 1)),
                            ),
                        )
                    ),
                    likelihood_range=(0.3, 1),
                    volume_range=(0.1, 0.8),
                    ignore_beats_occupied_by_voice=False,
                ),
            ),
            include_glitter=False,
            include_diva=False,
            include_natural_radio=False,
            include_percussion=True,
            radio_silent_channels=(1, 5),
            radio_samples=(
                "pbIII/samples/radio/carolina/3.wav",
                "pbIII/samples/radio/carolina/1.wav",
            ),
            radio_n_changes=2,
            radio_average_volume=0.1,
            radio_shadow_time=0.2,
            radio_min_volume=0.825,
            # speech_init_attributes={
            #     "speech0": {
            #         "start": 5.85,
            #         "duration": 22.5,
            #         "sound_engine": speech.Sampler(
            #             "pbIII/samples/speech/ghost_dance/ghost_dance_quote0_noise_reduction0.wav",
            #             volume=0.58,
            #         ),
            #     },
            #     "speech2": {
            #         "start": 3,
            #         "duration": 37.5,
            #         "sound_engine": speech.Sampler(
            #             globals.SAM_SPEECH_IAN_CURTIS[2], volume=1
            #         ),
            #     },
            # },
        ),
    )
