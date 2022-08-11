import pytest

from biomics.genetics.sequence import (
    hamming_distance,
    complement,
    mutations,
    variations,
)


def test_hamming_distance():
    assert hamming_distance('GGGCCGTTGGT', 'GGACCGTTGAC') == 3
    assert hamming_distance('ACGT', 'ACGT') == 0


def test_complement():
    assert complement('ATCG') == 'CGAT'


@pytest.mark.parametrize(
    'sequence, max_mutations, expected',
    [
        ('AT', 1, {'AT', 'AC', 'AG', 'AA', 'CT', 'GT', 'TT'}),
        ('AT', 0, {'AT'}),
        ('AT', 2, {
            'AT', 'AC', 'AG', 'AA', 'CT', 'GT', 'TT', 'CA',
            'CG', 'CC', 'GA', 'GG', 'GC', 'TA', 'TG', 'TC',
        }),
    ]
)
def test_mutations(sequence, max_mutations, expected):
    assert mutations(sequence, max_mutations) == expected


@pytest.mark.parametrize(
    'sequence, include_complement, include_variations_up_to, expected',
    [
        ('GTATG', False, 0, {'GTATG'}),
        ('GTATG', True, 0, {'GTATG', 'CATAC'}),
        ('TT', False, 1, {'TT', 'TC', 'TG', 'TA', 'CT', 'GT', 'AT'}),
        ('TT', True, 1, {'TT', 'TC', 'TG', 'TA', 'CT', 'GT', 'AT', 'AA', 'AC', 'AG', 'CA', 'GA'}),
    ]
)
def test_variations(sequence, include_complement, include_variations_up_to, expected):
    assert variations(sequence, include_complement, include_variations_up_to) == expected
