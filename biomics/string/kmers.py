from biomics.string.distance import hamming_distance


# TODO: consider creating a kmer class with methods such as complement
def count_ocurrences(s: str, t: str) -> int:
    """
    Return the number of ocurrences of t in s
    """
    count = 0
    for i in range(len(s) - len(t) + 1):
        chunk = s[i : i + len(t)]
        if chunk == t:
            count += 1
    return count


def kmer_frequencies(s: str, k: int):
    """
    Returns a series of k-mers and their frequencies in s.
    """
    freqs = {}
    for i in range(len(s) - k + 1):
        kmer = s[i : i + k]
        if kmer in freqs:
            freqs[kmer] += 1
        else:
            freqs[kmer] = 1
    return freqs


def kmer_locations(s: str, t: str):
    """
    Returns a list with the indexes where t is found within s.
    """
    locations = []
    for i in range(len(s) - len(t) + 1):
        chunk = s[i : i + len(t)]
        if chunk == t:
            locations.append(i)
    return locations


def find_clumps(genome: str, k: int, window_size: int, clump_density: int):
    """
    Returns a list of k-mers that occur at least clump_density times in a window of size window_size.

    Suggestion:
    1.  build dictionary mapping all possible kmers to their indices (3s total).
    2.  increment count when the 1st t consecutive indices of a given kmer fit within window length l (3s total).
    3.  return count
    """
    # TODO: very slow, takes a while on E. coli genome with k=9, w=500, n=3
    clumps = []
    for i in range(len(genome) - window_size + 1):
        window = genome[i : i + window_size]
        freqs = kmer_frequencies(window, k)
        for kmer, freq in freqs.items():
            if freq >= clump_density:
                clumps.append(kmer)
    return list(set(clumps))


def approximate_kmer_locations(genome: str, kmer: str, d: int):
    """
    Returns a list of the positions where variations of kmer of at most d differences occur in genome.
    """
    locations = []
    for i in range(len(genome) - len(kmer) + 1):
        chunk = genome[i : i + len(kmer)]
        if hamming_distance(chunk, kmer) <= d:
            locations.append(i)
    return locations


def kmer_neighbors(kmer: str, d: int, strict: bool = False) -> list[str]:
    """
    Args:
        kmer: a k-mer for which to find neighbors
        d: the number of differences.
        strict: if True, only return neighbors with exactly d differences,
                else return neighbors with at most d differences.
    """
    bases = ["A", "C", "G", "T"]
    if d == 0:
        return [kmer]
    if len(kmer) == 1:
        return bases
    kmers = set([])
    suffix_neighbors = kmer_neighbors(kmer[1:], d)
    for neighbor in suffix_neighbors:
        if strict:
            if hamming_distance(kmer[1:], neighbor) == (d - 1):
                for base in bases:
                    if base != kmer[0]:
                        kmers.add(base + neighbor)
            elif hamming_distance(kmer[1:], neighbor) == d:
                kmers.add(kmer[0] + neighbor)
        else:
            if hamming_distance(kmer[1:], neighbor) < d:
                for base in bases:
                    kmers.add(base + neighbor)
            else:
                kmers.add(kmer[0] + neighbor)
    return list(kmers)


def most_frequent_approximate_kmers(genome: str, k: int, d: int, strict: bool = False):
    patterns = []
    frequency_map = {}
    for i in range(len(genome) - k + 1):
        kmer = genome[i : i + k]
        neighbors = kmer_neighbors(kmer, d=d, strict=strict)
        for neighbor in neighbors:
            if neighbor in frequency_map:
                frequency_map[neighbor] += 1
            else:
                frequency_map[neighbor] = 1
    max_freq = max(frequency_map.values())
    for kmer, freq in frequency_map.items():
        if freq == max_freq:
            patterns.append(kmer)
    return patterns
