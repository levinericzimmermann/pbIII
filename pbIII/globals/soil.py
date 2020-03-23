import functools
import itertools
import operator

from mu.mel import ji
from mu.mel import mel
from mu.rhy import indispensability
from mu.sco import old
from mu.utils import prime_factors


class JICounterpoint(object):
    max_vol = 0.65
    min_vol = 0.255
    diff_vol = max_vol - min_vol

    def __init__(
        self,
        n_bars_smallest_loop: int = 1,
        harmonic_primes: tuple = (3, 5, 7, 11, 13),
        metric_primes: tuple = (7, 8, 9, 10, 11),  # 10 is the big exception
        harmonic_gender: bool = True,
    ) -> None:
        """init object

        for the first voice: constant change of metre
        for the third voice: constant change of harmony

        for the second voice: secondary change of harmony
        for the third voice: secondary change of metre

        for the first voice: slow change of harmony
        for the second voice: slow change of metre

        there is no third parameter yet (no fitting
        parameter has been found yet):
            1. register is rather a global changing function
            2. instruments (timbre) is difficult to implement,
               because one voice is supposed to stay within
               the same sound family (piano, harp and metal).
               therefore there are not 5 version that are
               shifting between the instruments (even though
               it would be possible to implement this).

        maybe 2. should be tried as an option. if the model
        of parameter modulation (impedance etc.) keeps the
        same while the instrument preset is changing, it
        is likely that the change won't be that big.
        Therefore there are five instrument families:

            0. piano
            1. harp
            2. vibraphone
            3. harpsichord =>
            4. marimba => marimba + xylophone
        """
        assert len(harmonic_primes) == 5
        assert len(metric_primes) == 5

        self.harmonic_primes = harmonic_primes
        self.metric_primes = metric_primes
        self.harmonic_gender = harmonic_gender

        self.harmonic_primes = harmonic_primes
        self.pitches_per_vox_per_bar, self.missing_primes_per_bar = self.make_pitches(
            self.harmonic_primes, self.harmonic_gender
        )

        self.harmonic_primes_per_bar = self.make_harmonic_primes_per_bar(
            self.missing_primes_per_bar
        )

        self.available_pitches = tuple(
            set(
                p.normalize()
                for p in functools.reduce(
                    operator.add,
                    functools.reduce(operator.add, self.pitches_per_vox_per_bar),
                )
            )
        )
        self.amount_pitches = len(self.available_pitches)

        self.bar_size = functools.reduce(operator.mul, metric_primes)
        self.metre_per_vox_per_bar = tuple(
            (bar[2],) + bar[:2]
            for bar in self.make_symmetric_structure(self.metric_primes)
        )
        self.instrument_per_vox_per_bar = self.make_instrument_family()

        self.data_per_vox_per_bar = tuple(
            tuple(zip(harmony, metre, timbre))
            for harmony, metre, timbre in zip(
                self.pitches_per_vox_per_bar,
                self.metre_per_vox_per_bar,
                self.instrument_per_vox_per_bar,
            )
        )

        self.amount_bars = len(self.pitches_per_vox_per_bar)
        self.size = self.bar_size * self.amount_bars

    def make_harmonic_primes_per_bar(self, missing_primes_per_bar: tuple) -> tuple:
        hp_per_bar = []

        for missing_primes in missing_primes_per_bar:
            primes = tuple(p for p in self.harmonic_primes if p not in missing_primes)
            primes += tuple(reversed(missing_primes))
            hp_per_bar.append(primes)

        return tuple(hp_per_bar)

    def convert2real_rhythm(self, voice: tuple, voice_idx=None, duration=None) -> tuple:
        relative_attacks = []
        relative_attacks_broken_down = []
        for bar_idx, bar in enumerate(voice):
            start_with_rest = False
            if bar_idx > 0:
                try:
                    bar = list(bar)
                    bar[0] = bar[0][0]
                    start_with_rest = True
                except TypeError:
                    start_with_rest = False

            size = sum(bar)

            try:
                assert self.bar_size % size == 0
            except AssertionError:
                msg = "Bar {0} with size {1} in voice {2} is ".format(
                    bar, size, voice_idx
                )
                msg += "not well formed."
                raise ValueError(msg)

            pulse_size = self.bar_size // size
            for pulse_idx, n_pulses in enumerate(bar):
                added = n_pulses * pulse_size
                if pulse_idx == 0 and start_with_rest:
                    relative_attacks[-1] += added
                    relative_attacks_broken_down[-1][0] += n_pulses
                    for n in range(n_pulses):
                        relative_attacks_broken_down[-1][1].append(pulse_size)
                else:
                    relative_attacks.append(added)
                    relative_attacks_broken_down.append(
                        [n_pulses, [pulse_size for n in range(n_pulses)]]
                    )

        if duration:
            factor = duration / self.bar_size
            relative_attacks = [r * factor for r in relative_attacks]

        return (
            tuple(relative_attacks),
            tuple((b[0], tuple(b[1])) for b in relative_attacks_broken_down),
        )

    @staticmethod
    def detect_group_index(group: tuple) -> int:
        """Return index for the particular group"""
        primary_index, secondary_index, tertiary_index = group
        return functools.reduce(
            operator.add, (primary_index * 12, secondary_index * 3, tertiary_index)
        )

    def detect_inner_triad_for_group(self, group: tuple) -> tuple:
        missing_primes = self.missing_primes_per_bar[self.detect_group_index(group)]
        allowed_primes_by_level = tuple(
            tuple(p for p in self.harmonic_primes if p not in missing_primes[:i])
            for i in range(1, 4)
        )
        return tuple(
            self.mk_pitch_depending_on_gender(primes)
            for primes in allowed_primes_by_level
        )

    @staticmethod
    def is_inner_triad(triad: tuple) -> bool:
        triad = tuple(p.set_val_border(2) for p in triad)
        tests = (
            tuple(p.summed() for p in triad) == (4, 3, 2),
            all(
                tuple(
                    a is b
                    for a, b in itertools.combinations(
                        tuple(p.strict_gender for p in triad), 2
                    )
                )
            ),
        )
        return all(tests)

    def mk_pitch_depending_on_gender(
        self, primes0: tuple = None, primes1: tuple = None, gender: bool = None
    ):
        if gender is None:
            gender = self.harmonic_gender
        if primes0:
            p0 = functools.reduce(operator.mul, primes0)
        else:
            p0 = 1

        if primes1:
            p1 = functools.reduce(operator.mul, primes1)
        else:
            p1 = 1

        if gender:
            return ji.r(p0, p1)
        else:
            return ji.r(p1, p0)

    def find_allowed_triads_for_group(
        self, group: tuple, allow_silence: tuple = (True, True, True)
    ) -> tuple:
        def add_silence_to_triads(allowed_triads):
            if any(allow_silence):
                voices = tuple(
                    i for i, is_allowed in enumerate(allow_silence) if is_allowed
                )

                if len(voices) > 1:
                    n_voices_are_allowed = 2
                else:
                    n_voices_are_allowed = 1

                silence_triads = []
                for triad in allowed_triads:
                    for n in range(n_voices_are_allowed):
                        for com in itertools.combinations(voices, n + 1):
                            new_triad = list(p.copy() for p in triad)
                            for v in com:
                                new_triad[v] = mel.TheEmptyPitch
                            silence_triads.append(tuple(new_triad))

                return allowed_triads + list(set(silence_triads))

            else:

                return allowed_triads

        def mk_perfect_triads() -> tuple:
            allowed_triads = [
                (
                    self.mk_pitch_depending_on_gender(allowed_primes_by_level[0]),
                    self.mk_pitch_depending_on_gender(allowed_primes_by_level[1]),
                    self.mk_pitch_depending_on_gender(allowed_primes_by_level[2]),
                ),
                (
                    self.mk_pitch_depending_on_gender(
                        tuple(
                            p
                            for p in allowed_primes_by_level[0]
                            if p != missing_primes[-1]
                        )
                    ),
                    self.mk_pitch_depending_on_gender(allowed_primes_by_level[1]),
                    self.mk_pitch_depending_on_gender(allowed_primes_by_level[2]),
                ),
            ]

            for com0 in itertools.combinations(allowed_primes_by_level[0], 3):
                p0 = self.mk_pitch_depending_on_gender(com0)
                for com1 in itertools.combinations(
                    tuple(p for p in com0 if p != missing_primes[1]), 2
                ):
                    p1 = self.mk_pitch_depending_on_gender(com1)
                    for prime in allowed_primes_by_level[2]:
                        if prime in com1:
                            p2 = self.mk_pitch_depending_on_gender((prime,))
                            allowed_triads.append((p0, p1, p2))
                    if sorted(com1) == sorted(allowed_primes_by_level[2]):
                        allowed_triads.append((p0, p1, p1))
                        if missing_primes[-1] in com0:
                            p2 = self.mk_pitch_depending_on_gender(
                                com1, (missing_primes[-1],)
                            )
                            allowed_triads.append((p0, p1, p2))

                    elif all(tuple(p in com0 for p in allowed_primes_by_level[2])):
                        p2 = self.mk_pitch_depending_on_gender(
                            allowed_primes_by_level[2]
                        )
                        allowed_triads.append((p0, p1, p2))

                if sorted(com0) == sorted(allowed_primes_by_level[1]):
                    p2 = self.mk_pitch_depending_on_gender(allowed_primes_by_level[-1])
                    allowed_triads.append((p0, p0, p2))

            return tuple(set(add_silence_to_triads(allowed_triads)))

        def mk_imperfect_triads() -> tuple:
            allowed_triads = [
                (
                    self.mk_pitch_depending_on_gender(
                        allowed_primes_by_level[0], (missing_primes[0],)
                    ),
                    self.mk_pitch_depending_on_gender(allowed_primes_by_level[1]),
                    self.mk_pitch_depending_on_gender(allowed_primes_by_level[2]),
                ),
                (
                    self.mk_pitch_depending_on_gender(allowed_primes_by_level[0]),
                    self.mk_pitch_depending_on_gender(
                        allowed_primes_by_level[1], (missing_primes[1],)
                    ),
                    self.mk_pitch_depending_on_gender(allowed_primes_by_level[2]),
                ),
            ]

            for com0 in itertools.combinations(allowed_primes_by_level[0], 3):

                p0 = self.mk_pitch_depending_on_gender(com0)

                for com1 in itertools.combinations(
                    tuple(p for p in com0 if p != missing_primes[1]), 2
                ):
                    p1 = self.mk_pitch_depending_on_gender(com1)

                    if sorted(com1) == sorted(allowed_primes_by_level[2]):
                        if missing_primes[-1] in com0:
                            p2 = self.mk_pitch_depending_on_gender(
                                com1, (missing_primes[-1],)
                            )
                            allowed_triads.append((p0, p1, p2))

                if sorted(com0) == sorted(allowed_primes_by_level[1]):
                    p1 = self.mk_pitch_depending_on_gender(
                        allowed_primes_by_level[1], (missing_primes[1],)
                    )
                    p2 = self.mk_pitch_depending_on_gender(allowed_primes_by_level[-1])
                    allowed_triads.append((p0, p1, p2))

                p1 = self.mk_pitch_depending_on_gender(allowed_primes_by_level[1])
                p2 = self.mk_pitch_depending_on_gender(allowed_primes_by_level[2])
                if p1 != p0:
                    allowed_triads.append((p0, p1, p2))

            allowed_triads = add_silence_to_triads(allowed_triads)

            # if allow_silence[2]:
            #     for triad in delicate_triads:
            #         allowed_triads.append((triad[0], triad[1], mel.TheEmptyPitch))

            return tuple(set(allowed_triads))

        missing_primes = self.missing_primes_per_bar[self.detect_group_index(group)]
        allowed_primes_by_level = tuple(
            tuple(p for p in self.harmonic_primes if p not in missing_primes[:i])
            for i in range(1, 4)
        )

        return mk_perfect_triads(), mk_imperfect_triads()

    def make_pitches(self, harmonic_primes: tuple, harmonic_gender: bool) -> tuple:
        def make_primary_pitches(missing_prime: int) -> tuple:
            available_primes = tuple(p for p in harmonic_primes if p != missing_prime)
            pitches = [
                ji.r(functools.reduce(operator.mul, available_primes), missing_prime)
            ]
            for n in (3, 4):
                for combination in itertools.combinations(available_primes, n):
                    pitches.append(ji.r(functools.reduce(operator.mul, combination), 1))
            return tuple(pitches)

        def make_secondary_pitches(missing_prime0: int, missing_prime1: int) -> tuple:
            available_primes = tuple(
                p for p in harmonic_primes if p not in (missing_prime0, missing_prime1)
            )
            pitches = [
                ji.r(functools.reduce(operator.mul, available_primes), missing_prime1)
            ]
            for n in (2, 3):
                for combination in itertools.combinations(available_primes, n):
                    pitches.append(ji.r(functools.reduce(operator.mul, combination), 1))
            return tuple(pitches)

        def make_tertiary_pitches(missing_primes0: tuple, missing_prime1) -> tuple:
            available_primes = tuple(
                p
                for p in harmonic_primes
                if p not in missing_primes0 + (missing_prime1,)
            )
            pitches = [
                ji.r(functools.reduce(operator.mul, available_primes), missing_prime1)
            ]
            for n in (1, 2):
                for combination in itertools.combinations(available_primes, n):
                    pitches.append(ji.r(functools.reduce(operator.mul, combination), 1))
            return tuple(pitches)

        symmetric_structure = self.make_symmetric_structure(harmonic_primes)

        primary_pitches = {p: make_primary_pitches(p) for p in harmonic_primes}
        primary_pitches_transposition_model = (ji.r(1, 1),) + tuple(
            ji.r(1, prime) for prime in harmonic_primes
        )
        for prime in harmonic_primes:
            primary_pitches[prime] = self.sort_transposition(
                primary_pitches_transposition_model, primary_pitches[prime]
            )[1]

        secondary_pitches = {
            per: make_secondary_pitches(*per)
            for per in functools.reduce(
                operator.add,
                tuple(
                    tuple(itertools.permutations(com))
                    for com in itertools.combinations(harmonic_primes, 2)
                ),
            )
        }
        for prime in harmonic_primes:
            secondary_pitches_transposition_model = (ji.r(1, 1),) + tuple(
                ji.r(1, p) for p in harmonic_primes if p != prime
            )
            for prime1 in harmonic_primes:
                if prime1 != prime:
                    key = (prime, prime1)
                    secondary_pitches[key] = self.sort_transposition(
                        secondary_pitches_transposition_model, secondary_pitches[key]
                    )[1]

        tertiary_pitches = {}
        for combination in itertools.combinations(harmonic_primes, 2):
            for prime in harmonic_primes:
                if prime not in combination:
                    key = tuple(sorted(combination)) + (prime,)
                    tertiary_pitches.update(
                        {key: make_tertiary_pitches(key[:2], key[2])}
                    )
        for combination in itertools.combinations(harmonic_primes, 2):
            tertiary_pitches_transposition_model = (ji.r(1, 1),) + tuple(
                ji.r(1, p) for p in harmonic_primes if p not in combination
            )
            for prime in harmonic_primes:
                if prime not in combination:
                    key = tuple(sorted(combination)) + (prime,)
                    tertiary_pitches[key] = self.sort_transposition(
                        tertiary_pitches_transposition_model, tertiary_pitches[key]
                    )[1]

        if not harmonic_gender:
            for collection in (primary_pitches, secondary_pitches, tertiary_pitches):
                for key in collection:
                    collection[key] = tuple(p.inverse() for p in collection[key])

        pitches_per_voice_per_part = []
        for bar in symmetric_structure:
            pitches_per_voice_per_part.append(
                (
                    primary_pitches[bar[0]],
                    secondary_pitches[bar[:2]],
                    tertiary_pitches[tuple(sorted(bar[:2])) + (bar[2],)],
                )
            )
        return tuple(pitches_per_voice_per_part), symmetric_structure

    def calculate_volume_per_attack_per_voice(self) -> tuple:
        volume_per_voice = []
        for vox in self.time_points:
            volume = []
            for bar in vox:
                for item in bar:
                    volume.append((item[1] * self.diff_vol) + self.min_vol)
            volume_per_voice.append(tuple(volume))
        return tuple(volume_per_voice)

    def make_instrument_family(self):
        """explanation of instrument family tuple

        each subtuple contains member for
        one family. there are 5 families.
        the boolean value behind the
        instruments name indicate whether
        the instrument is saved as an
        fxp preset (True) or if it belongs
        to the default pianoteq instruments
        (False).
        """
        instrument_family_cycles = (
            (
                ("J. Schantz", False),
                ("J.E. Schmidt", False),
                ("Pleyel Player", False),
                ("A. Walter", False),
                ("D. Schoffstoss", False),
                ("C. Graf", False),
                ("Erard Player", False),
            ),
            (("Celtic Harp Bright", False), ("Concert Harp Daily", False)),
            (
                ("Vibraphone V-B Humanized no stretching", True),
                ("Glockenspiel Humanized no stretching", True),
                ("Celesta Bright no stretching", True),
                ("Vibraphone V-M Humanized no stretching", True),
                ("Toy Piano Dry no stretching", True),
            ),
            (
                ("F.E. Blanchet Harpsichord", False),
                ("C. Grimaldi Harpsichord A", False),
                ("Neupert Clavichord double", False),
            ),
            (
                ("Xylophone Bright no stretching", True),
                ("Marimba Bright no stretching", True),
            ),
        )

        instrument_family_cycles = (
            (
                ("J. Schantz", False),
                ("J.E. Schmidt", False),
                ("Pleyel Player", False),
                ("A. Walter", False),
                ("D. Schoffstoss", False),
                ("C. Graf", False),
            ),
            (("Concert Harp Daily", False),),
            (
                ("Vibraphone V-B Humanized no stretching", True),
                ("Vibraphone V-M Humanized no stretching", True),
            ),
            (
                ("Glockenspiel Humanized no stretching", True),
                ("Toy Piano Dry no stretching", True),
                ("Celesta Bright no stretching", True),
            ),
            (("CP-80 Amped", False),),
        )
        instrument_family_cycles = (
            (
                ("J. Schantz", False),
                ("J.E. Schmidt", False),
                ("Pleyel Player", False),
                ("A. Walter", False),
                ("D. Schoffstoss", False),
                ("C. Graf", False),
            ),
            (("Concert Harp Daily", False),),
            (
                ("Vibraphone V-B Humanized no stretching", True),
                ("Vibraphone V-M Humanized no stretching", True),
            ),
            (
                ("Glockenspiel Humanized no stretching", True),
                ("Toy Piano Dry no stretching", True),
                ("Celesta Bright no stretching", True),
            ),
            (("Pleyel Player", False), ("Erard Player", False)),
        )

        instrument_family_cycles = (
            (("Concert Harp Daily", False),),
            (("Concert Harp Daily", False),),
            (("Concert Harp Daily", False),),
            (("Concert Harp Daily", False),),
            (("Concert Harp Daily", False),),
        )

        if self.harmonic_gender is False:
            instrument_family_cycles = tuple(
                tuple(reversed(family)) for family in instrument_family_cycles
            )

        instrument_family_cycles = tuple(
            itertools.cycle(family) for family in instrument_family_cycles
        )
        index_tuple = (2, 5, 7, 11, 13)
        family_index_per_vox_per_bar = (
            bar[1:] + (bar[0],) for bar in self.make_symmetric_structure(index_tuple)
        )
        return tuple(
            tuple(next(instrument_family_cycles[index_tuple.index(idx)]) for idx in bar)
            for bar in family_index_per_vox_per_bar
        )

    @staticmethod
    def fix_inner_positions_of_symmetrical_sets(sets: tuple) -> tuple:
        available_elements = set.union(*sets)
        element_counter = {element: 0 for element in available_elements}
        last_elements = []
        n_sets = len(sets)
        for counter, s0, s1 in zip(range(n_sets), sets, sets[1:] + (sets[0],)):
            possible_elements = s0.intersection(s1)
            if last_elements:
                prohibited_items = [last_elements[-1]]
                if counter + 1 == n_sets:
                    prohibited_items.append(last_elements[0])

                possible_elements = tuple(
                    item for item in possible_elements if item not in prohibited_items
                )

            choosen_element = sorted(
                possible_elements, key=lambda x: element_counter[x]
            )[0]
            element_counter[choosen_element] += 1
            last_elements.append(choosen_element)

        fixed_sets = []
        for s, first_element, last_element in zip(
            sets, [last_elements[-1]] + last_elements, last_elements
        ):
            in_between = tuple(
                element for element in s if element not in (first_element, last_element)
            )
            fixed_sets.append((first_element,) + in_between + (last_element,))

        return tuple(fixed_sets)

    @staticmethod
    def fix_inner_positions_of_nested_structures(structures: tuple) -> tuple:
        structure1 = JICounterpoint.fix_inner_positions_of_symmetrical_sets(
            tuple(set(group) for group in structures[1])
        )
        new_order_of_structure1 = tuple(
            tuple(old_group.index(item) for item in group)
            for old_group, group in zip(structures[1], structure1)
        )
        structure2 = tuple(
            tuple(groups[idx] for idx in indices_per_group)
            for groups, indices_per_group in zip(structures[2], new_order_of_structure1)
        )
        structure2 = tuple(
            set(item) for item in functools.reduce(operator.add, structure2)
        )
        structure2 = JICounterpoint.fix_inner_positions_of_symmetrical_sets(structure2)
        return structures[0], structure1, structure2

    @staticmethod
    def combine_structures_to_progressing_list(structures: tuple) -> tuple:
        complete_length = len(structures[-1])
        progressing_list = [[] for i in structures[-1]]
        for structure in structures:
            length = len(structure)
            ratio = complete_length // length
            for item, valid_range in zip(
                structure,
                tuple(
                    zip(
                        range(0, complete_length, ratio),
                        range(ratio, complete_length + ratio, ratio),
                    )
                ),
            ):
                for n in range(*valid_range):
                    progressing_list[n].append(item)
        return tuple(tuple(bar) for bar in progressing_list)

    @staticmethod
    def make_symmetric_structure(elements: tuple) -> tuple:
        assert len(elements) == 5
        structure0 = tuple(elements)
        structure1 = tuple(
            tuple(element for element in elements if element not in (el0,))
            for el0 in structure0
        )
        structure2 = tuple(
            tuple(
                tuple(element for element in elements if element not in (el0, el1))
                for el1 in group1
            )
            for el0, group1 in zip(structure0, structure1)
        )
        fixed_positions = JICounterpoint.fix_inner_positions_of_nested_structures(
            (structure0, structure1, structure2)
        )
        fixed_positions = tuple(
            functools.reduce(operator.add, structure) if idx > 0 else structure
            for idx, structure in enumerate(fixed_positions)
        )
        return JICounterpoint.combine_structures_to_progressing_list(fixed_positions)

    @staticmethod
    def sort_transposition(original: tuple, *transposition: tuple) -> tuple:
        # TODO(add a description)
        """This method.

        """
        matrix = tuple(tuple(b - a for b in original) for a in original)
        sets = tuple(set(m) for m in matrix)
        r = []
        for group in transposition:
            intervals0 = tuple(p - group[0] for p in group)
            try:
                idx = sets.index(set(intervals0))
            except ValueError:
                msg = "Group {0} isn't a transposition of {1}.".format(group, original)
                raise ValueError(msg)

            compare = matrix[idx]
            new_group = [None for i in original]
            for idxi, interval in enumerate(intervals0):
                new_group[compare.index(interval)] = group[idxi]

            r.append(tuple(new_group))

        return (tuple(original),) + tuple(r)

    @staticmethod
    def mk_pitches_per_vox(primes: tuple, gender: bool = True) -> tuple:
        """This method return a tuple that contains pitches for each voice.

        Therefore the returning tuple contains 3 subtuples (one for each voice).
        Each of those voices [subtuples] is composed of further tuples. One of those
        tuples represents one transposition. Each transposition is made of different
        groups [tuples] again. Each of those groups contain pitch objects. The order
        of the pitch elements in those groups is organised in a way that makes sure
        that the same index in different groups of the same transposition returns
        a pitch that represents the same harmonic position (in the respective group).
        """

        from pbIII.soil import factory

        ct = factory.Factory(primes)
        pitches_per_transposition_per_voice = []
        for idx, vox0, vox1 in zip(range(len(ct.voices)), ct.voices, ct.voices[1:]):
            vox0 = tuple(item for item in vox0 if not item.is_fake)
            voice = []
            l0, l1 = len(vox0), len(vox1)
            size = l1 // l0
            transpositions = []
            for item, group in zip(
                vox0, tuple(vox1[i : i + size] for i in range(0, l1, size))
            ):
                if len(transpositions) == size:
                    transpositions = JICounterpoint.sort_transposition(
                        transpositions[0], *transpositions[1:]
                    )

                    voice.append(tuple(transpositions))
                    transpositions = []

                transpositions.append(
                    tuple(p.convert2pitch(gender=gender) for p in group + [item])
                )

            transpositions = JICounterpoint.sort_transposition(
                transpositions[0], *transpositions[1:]
            )
            voice.append(tuple(transpositions))
            for v_idx, trans in enumerate(voice):
                trans = list(trans)
                for t_idx, group in enumerate(trans):
                    group = tuple(p.normalize() for p in group)
                    trans[t_idx] = group
                voice[v_idx] = tuple(trans)

            pitches_per_transposition_per_voice.append(tuple(voice))

        return tuple(pitches_per_transposition_per_voice)

    def find_allowed_triads(self) -> tuple:
        def is_allowed_triad(triad: tuple) -> bool:
            interval_complexity = tuple(
                (b - a).set_val_border(2).summed() for a, b in zip(triad, triad[1:])
            )
            tests = (
                all(tuple(n in (0, 1) for n in interval_complexity)),
                all(
                    (
                        interval_complexity[0] == 2,
                        interval_complexity[1] == 1,
                        triad[0].set_val_border(2).summed() == 5,
                    )
                ),
            )
            return any(tests)

        """
        # if _ALLOWED_TRIADS_PER_GENDER[self.harmonic_gender] is not None:
        #     return _ALLOWED_TRIADS_PER_GENDER[self.harmonic_gender]
        # elif _ALLOWED_TRIADS_PER_GENDER[not self.harmonic_gender] is not None:
        #     return tuple(
        #         tuple(p.inverse() for p in triad)
        #         for triad in _ALLOWED_TRIADS_PER_GENDER[not self.harmonic_gender]
        #     )
        # else:
        #     return tuple(
        #         triad
        #         for triad in itertools.product(*self.uniqified_pitches_per_vox)
        #         if is_allowed_triad(triad)
        #     )
        """

    def find_drone_chord_per_bar(self) -> tuple:
        bars = [[] for i in range(self.amount_bars)]
        possible_pitches_per_voice = []
        for n in (4, 3, 2):
            pitches = tuple(
                ji.r(functools.reduce(operator.mul, comb), 1)
                for comb in itertools.combinations(self.harmonic_primes, n)
            )
            if not self.harmonic_gender:
                pitches = tuple(p.inverse() for p in pitches)
            pitches = tuple(p.normalize() for p in pitches)
            possible_pitches_per_voice.append(pitches)

        for vox, comparision in zip(self.pitches_per_vox, possible_pitches_per_voice):
            vox = functools.reduce(operator.add, vox)
            responsible_bars_per_pitch = tuple(
                range(0, self.amount_bars, self.amount_bars // len(vox))
            )
            responsible_bars_per_pitch = tuple(
                tuple(
                    range(n, m)
                    for n, m in zip(
                        responsible_bars_per_pitch,
                        responsible_bars_per_pitch[1:] + (self.amount_bars,),
                    )
                )
            )
            for pitch_set, scope in zip(vox, responsible_bars_per_pitch):
                pitch = tuple(p for p in pitch_set if p in comparision)
                assert len(pitch) == 1
                pitch = pitch[0]
                for bar_idx in scope:
                    bars[bar_idx].append(pitch)

        return tuple(tuple(b) for b in bars)

    @staticmethod
    def mk_meter_per_vox(primes: tuple) -> tuple:
        """Return tuple that contains n subtuples.

        Each subtuple represents a metrical subsection.
        The first element of each subtuple contains the meter for
        the first voice, the second elements represents the second
        voice and the third element represents the third voice.
        """
        parts = []
        for vox0 in primes:
            for vox1 in tuple(p for p in primes if p != vox0):
                for vox2 in tuple(p for p in primes if p not in (vox0, vox1)):
                    parts.append((vox0, vox1, vox2))
        return tuple(parts)

    @staticmethod
    def find_weight_per_beat(prime: int) -> tuple:
        weights = indispensability.indispensability_for_bar(
            tuple(prime_factors.factorise(prime))
        )
        maxima = max(weights)
        return tuple(w / maxima for w in weights)

    def mk_time_points_per_vox(
        self, primes: tuple, meters: tuple, smallest_loop_size: int
    ) -> tuple:
        """Return tuple with 3 subtuples where each subtuple represents one vox.

        Each vox is composed of bars. Each bar is composed of beats. Each beat
        is composed of (absolute_position: integer, metrical_weight: float).
        """

        absolute_numbers = tuple(
            tuple(range(0, self.bar_size, self.bar_size // p)) for p in primes
        )
        weights = tuple(JICounterpoint.find_weight_per_beat(p) for p in primes)
        bar_data = tuple(tuple(zip(n, w)) for n, w in zip(absolute_numbers, weights))

        voices = [[] for i in range(3)]

        for meter in meters:
            for n in range(smallest_loop_size):
                for v_idx, vox in enumerate(meter):
                    added = self.bar_size * len(voices[v_idx])
                    voices[v_idx].append(
                        tuple(
                            (bd[0] + added, bd[1]) for bd in bar_data[primes.index(vox)]
                        )
                    )

        return tuple(tuple(v) for v in voices)


def simple_synthesis(melodies: tuple, make_diva=True):
    import random

    random.seed(10)

    import pyteq

    for idx, voice in enumerate(melodies):
        # voice = old.Melody(voice[:120]).tie()
        voice = old.Melody(voice[:200])
        if make_diva:
            melody_diva = [
                pyteq.DivaTone(
                    ji.JIPitch(t.pitch, multiply=250),
                    t.delay,
                    t.duration,
                    glissando=t.glissando,
                    volume=t.volume,
                )
                if t.pitch != mel.TheEmptyPitch
                else pyteq.PyteqTone(t.pitch, t.delay, t.duration)
                for t in voice
            ]
            pyteq.Diva(melody_diva).export(
                "pianoteq_output/test_diva{0}.mid".format(idx)
            )
        melody_pteq = [
            pyteq.PyteqTone(
                ji.JIPitch(t.pitch, multiply=250),
                t.delay,
                t.duration,
                volume=t.volume,
                glissando=t.glissando,
                # impedance=random.uniform(2.801, 2.98),
                q_factor=random.uniform(0.201, 0.28),
                string_length=random.uniform(8.9, 9.8),
                sustain_pedal=1,
            )
            if t.pitch != mel.TheEmptyPitch
            else pyteq.PyteqTone(t.pitch, t.delay, t.duration)
            for t in voice
        ]
        f = pyteq.Pianoteq(
            melody_pteq, available_midi_notes=tuple(n for n in range(20, 125))
        )
        f.export2wav(
            "pianoteq_output/test{0}".format(idx), preset='"Concert Harp Daily"'
        )
        # f.export2wav("test{0}".format(idx), preset='"Erard Player"')


def harmonic_synthesis(poly_per_interlocking: tuple):
    import pyteq

    for poly_idx, poly in enumerate(poly_per_interlocking):
        for melody_idx, voice in enumerate(poly):
            voice = old.Melody(voice[:280])
            melody = [
                pyteq.PyteqTone(
                    ji.JIPitch(t.pitch, multiply=250),
                    t.delay,
                    t.duration,
                    volume=t.volume,
                    impedance=2,
                    q_factor=0.2,
                    string_length=9.9,
                    sustain_pedal=1,
                )
                if t.pitch != mel.TheEmptyPitch
                else pyteq.PyteqTone(t.pitch, t.delay, t.duration)
                for t in voice
            ]
            instr_range = tuple(n for n in range(10, 125))
            f = pyteq.Pianoteq(melody, available_midi_notes=instr_range)
            f.export2wav(
                "pianoteq_output/glitter_{0}_{1}".format(poly_idx, melody_idx),
                # preset='"Kalimba Spacey"',
                preset='"Celtic Harp Bright"',
            )
