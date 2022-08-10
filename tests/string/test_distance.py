from biomics.string.distance import hamming_distance


def test_hamming_distance():
    assert hamming_distance('GGGCCGTTGGT', 'GGACCGTTGAC') == 3
    assert hamming_distance('ACGT', 'ACGT') == 0
