def count_ocurrences(s: str, t: str) -> int:
    """
    Return the number of ocurrences of t in s
    """
    count = 0
    for i in range(len(s) - len(t) + 1):
        chunk = s[i:i+len(t)]
        if chunk == t:
            count += 1
    return count


def kmer_frequencies(s: str, k: int):
    """
    Returns a series of k-mers and their frequencies in s.
    """
    freqs = {}
    for i in range(len(s) - k + 1):
        kmer = s[i:i+k]
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
        chunk = s[i:i+len(t)]
        if chunk == t:
            locations.append(i)
    return locations
