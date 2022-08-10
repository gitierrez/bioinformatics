import numpy as np


def complement(seq: str, type: str = 'DNA', standard_direction: bool = True) -> str:
    """
    Return the complementary strand of a given DNA or RNA sequence.

    Args:
        seq: The sequence to complement.
        type: The type of sequence. Either 'DNA' or 'RNA'.
        standard_direction: If True, the complementary strand will be in the 5'-3' direction.
    """
    if type == 'DNA':
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    elif type == 'RNA':
        complement = {'A': 'U', 'U': 'A', 'C': 'G', 'G': 'C'}
    else:
        raise ValueError("Type must be 'DNA' or 'RNA'")
    try:
        if standard_direction:
            return ''.join(complement[nucleotide] for nucleotide in seq[::-1])
        return ''.join([complement[nuc] for nuc in seq])
    except KeyError:
        raise ValueError("Invalid nucleotide in sequence")


def group_values_by_complement(counts: dict) -> dict:
    """
    Group the values of dictionary by their complementary strand.
    """
    exclusions = set([])
    grouped_counts = {}
    for seq, count in counts.items():
        if seq in exclusions:
            continue
        complement_seq = complement(seq)
        grouped_counts[seq] = count + counts.get(complement_seq, 0)
        exclusions.add(complement_seq)
    return grouped_counts


def gc_skew(genome: str, window_size: int = 1):
    """
    Return the GC skew of a genome.
    """
    skew = np.zeros(len(genome) - window_size + 2)
    for i in range(len(genome) - window_size + 1):
        window = genome[i:i+window_size]
        skew[i+1] = window.count('G') - window.count('C')
    return skew
