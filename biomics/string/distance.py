def hamming_distance(p: str, q: str):
    """
    Compute the Hamming distance between two strings.
    """
    return sum(ch1 != ch2 for ch1, ch2 in zip(p, q))
