from biomics.genetics.utils import validate_nucleotides


class DNASequence:

    def __init__(self, value: str, validate: bool = True):
        if validate:
            validate_nucleotides(value, valid_nucleotides={'A', 'C', 'G', 'T'})
        self.value = value
        self._complement = None

    @property
    def complement(self):
        if self._complement is None:
            self._complement = DNASequence(self._get_complement(self.value))
        return self._complement

    def mutations(self, max_mutations: int = 1):
        """
        Returns all mutations of the sequence up to max_mutations.

        For example, if the sequence is 'AT', mutations(1) will return
        ['AT', 'AC', 'AG', 'AA', 'CT', 'GT', 'TT']
        """
        bases = ['A', 'C', 'G', 'T']
        if max_mutations == 0:
            return [self]
        if len()

    def variations(self, include_complement: bool = False, include_variations_up_to: int = 0):
        """
        Returns all variations of the sequence up to include_variations_up_to.
        """
        variations = {self}
        if include_complement:
            variations.add(self.complement)
        if include_variations_up_to > 0:
            for mutation in self.mutations(max_mutations=include_variations_up_to):
                variations.add(mutation)
            for mutation in self.complement.mutations(max_mutations=include_variations_up_to):
                variations.add(mutation)
        return variations

    @staticmethod
    def _get_complement(value: str) -> str:
        pairings = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return ''.join(pairings[nucleotide] for nucleotide in value[::-1])

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]
