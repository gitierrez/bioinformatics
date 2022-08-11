def hamming_distance(p: str, q: str):
    return sum(ch1 != ch2 for ch1, ch2 in zip(p, q))


def complement(sequence: str) -> str:
    pairings = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(pairings[nucleotide] for nucleotide in sequence[::-1])


def mutations(sequence: str, max_mutations: int = 1) -> set[str]:
    """
    Returns all mutations of the sequence up to max_mutations.

    For example, mutations('AT', 1) will return
    ['AT', 'AC', 'AG', 'AA', 'CT', 'GT', 'TT']
    """
    bases = {"A", "C", "G", "T"}
    if max_mutations == 0:
        return {sequence}
    if len(sequence) == 1:
        return bases
    mutations_ = set([])
    suffix_mutations = mutations(sequence[1:], max_mutations=max_mutations)
    for mutation in suffix_mutations:
        if hamming_distance(sequence[1:], mutation) < max_mutations:
            for base in bases:
                mutations_.add(base + mutation)
        else:
            mutations_.add(sequence[0] + mutation)
    return mutations_


# test when I want variations of only the base sequence, i.e. include_complement=False
def variations(
    sequence: str, include_complement: bool = False, include_variations_up_to: int = 0
) -> set[str]:
    """
    Returns all variations of the sequence up to include_variations_up_to.
    """
    variations = {sequence}

    # add mutations of original sequence
    for mutation in mutations(sequence, max_mutations=include_variations_up_to):
        variations.add(mutation)
    if include_complement:
        # add complement of original sequence
        complement_seq = complement(sequence)
        variations.add(complement_seq)
        # add variations of complement
        for mutation in mutations(
            complement_seq, max_mutations=include_variations_up_to
        ):
            variations.add(mutation)
    return variations
