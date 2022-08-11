from biomics.genetics.sequence import variations


def validate_nucleotides(value: str, valid_nucleotides: set = None):
    if valid_nucleotides is None:
        valid_nucleotides = {'A', 'T', 'C', 'G'}
    for i, nucleotide in enumerate(value):
        if nucleotide not in valid_nucleotides:
            raise ValueError(
                f"Invalid character {nucleotide} found at position {i} in DNA sequence"
            )
    return True


def get_region_in_circular_array(array, center, window_size):
    half_window = window_size // 2
    if center - half_window >= 0:
        return array[center - half_window : center + half_window + 1]
    return array[-(half_window - center):] + array[: center + half_window + 1]


def get_frequency_map(sequence: str, subsequence_length: int, **kwargs):
    frequency_map = {}
    for i in range(len(sequence) - subsequence_length + 1):
        subsequence = sequence[i: i + subsequence_length]
        similar_sequences = variations(subsequence, **kwargs)
        for seq in similar_sequences:
            if seq in frequency_map:
                frequency_map[seq] += 1
            else:
                frequency_map[seq] = 1
    return frequency_map
