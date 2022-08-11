from biomics.genetics import DNASequence


def validate_nucleotides(value: str, valid_nucleotides: set = None):
    if valid_nucleotides is None:
        valid_nucleotides = {'A', 'T', 'C', 'G'}
    for i, nucleotide in enumerate(value):
        if nucleotide not in valid_nucleotides:
            raise ValueError(
                f"Invalid character {nucleotide} found at position {i} in DNA sequence"
            )


def get_region_in_circular_array(array, center, window_size):
    half_window = window_size // 2
    if center - half_window >= 0:
        return array[center - half_window : center + half_window + 1]
    return array[-(half_window - center):] + array[: center + half_window + 1]


def get_frequency_map(sequence: DNASequence, subsequence_length: int, **kwargs):
    frequency_map = {}
    for i in range(len(sequence) - subsequence_length + 1):
        subsequence = DNASequence(sequence[i: i + subsequence_length])
        similar_sequences = subsequence.variations(**kwargs)
        for seq in similar_sequences:
            if seq in frequency_map:
                frequency_map[seq] += 1
            else:
                frequency_map[seq] = 1
    return frequency_map


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
