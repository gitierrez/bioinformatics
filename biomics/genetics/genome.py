import numpy as np

from biomics.genetics import DNASequence
from biomics.genetics.utils import (
    validate_nucleotides,
    get_region_in_circular_array,
    get_frequency_map,
)


class ProkaryoticGenome:
    def __init__(self, value: str):
        validate_nucleotides(value, valid_nucleotides={"A", "C", "G", "T"})
        self.value = value

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r") as f:
            genome = f.read()
        return ProkaryoticGenome(genome)

    @classmethod
    def from_organism_name(cls, organism_name: str):
        raise NotImplementedError()

    def locations_of_sequence(
        self,
        seq: DNASequence,
        include_complement: bool = False,
        include_variations_up_to: int = 0,
    ):
        locations = []
        look_for = seq.variations(include_complement, include_variations_up_to)

        for i in range(len(self) - len(seq) + 1):
            current_seq = self.value[i : i + len(seq)]
            if current_seq in look_for:
                locations.append(i)
        return locations

    def ori_box_candidates(self, window_size: int = 1000):
        """
        Returns candidates for DnaA binding boxes.
        """
        skew = self.gc_skew()
        ori_center = np.argmin(skew)
        ori_region = get_region_in_circular_array(self, ori_center, window_size)
        freq_map = get_frequency_map(
            ori_region,
            subsequence_length=9,
            include_complement=True,
            include_variations_up_to=1
        )
        max_freq = max(freq_map.values())
        candidates = {seq for seq, freq in freq_map.items() if freq == max_freq}
        # dnaA boxes tend to have a high AT content
        return sorted(
            candidates, key=lambda x: x.count("A") + x.count("T"), reverse=True
        )

    def gc_skew(self):
        skew = np.zeros(len(self.value))
        for i, n in enumerate(self.value):
            if n == "G":
                skew[i] = 1
            elif n == "C":
                skew[i] = -1
        return skew.cumsum()

    def __len__(self):
        return len(self.value)

    def __getitem__(self, index):
        return self.value[index]
