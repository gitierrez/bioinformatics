import pytest

from biomics.genetics.utils import (
    validate_nucleotides,
    get_region_in_circular_array,
    get_frequency_map,
)


def test_validate_nucleotides_with_valid_string():
    assert validate_nucleotides('ATCG')


def test_validate_nucleotides_with_invalid_string():
    with pytest.raises(ValueError):
        validate_nucleotides('ATCGX')


@pytest.mark.parametrize(
    'array, center, window_size, expected',
    [
        ('CATGGGCATCGGCCATACGCC', 8, 10, 'GGGCATCGGCC'),
        ('CATGGGCATCGGCCATACGCC', 2, 10, 'GCCCATGGGCA'),
    ],
)
def test_get_region_in_circular_array(array, center, window_size, expected):
    assert get_region_in_circular_array(array, center, window_size) == expected


def test_frequency_map():
    freqs = get_frequency_map('ACGTTGCATGTCGCATGATGCATGAGAGCT', subsequence_length=4)
    assert freqs["GCAT"] == 3
    assert freqs["CATG"] == 3
    assert freqs["ATGA"] == 2
    assert freqs["TCGC"] == 1
