import pytest
import numpy as np

from biomics.genetics.utils import complement, group_values_by_complement, gc_skew


def test_dna_complementary_strand_with_standard_direction():
    assert complement("ATCG", type="DNA", standard_direction=True) == "CGAT"


def test_rna_complementary_strand_with_standard_direction():
    assert complement("AUCG", type="RNA", standard_direction=True) == "CGAU"


def test_dna_complementary_strand_without_standard_direction():
    assert complement("ATCG", type="DNA", standard_direction=False) == "TAGC"


def test_rna_complementary_strand_without_standard_direction():
    assert complement("AUCG", type="RNA", standard_direction=False) == "UAGC"


def test_raises_value_error_with_invalid_nucleotide():
    with pytest.raises(ValueError):
        complement("ATCX")


def test_raises_value_error_with_invalid_nucleotide_in_rna():
    with pytest.raises(ValueError):
        complement("ATCG", type="RNA")


def test_raises_value_error_with_invalid_nucleotide_in_dna():
    with pytest.raises(ValueError):
        complement("AUCG", type="DNA")


def test_raises_key_error_when_invalid_type_given():
    with pytest.raises(ValueError):
        complement("ATCG", type="DNAX")


def test_group_values_by_complement():
    test_case = {
        "AGCAG": 10,
        "GCATT": 8,
        "CTGCT": 9,
        "AAAAA": 5,
        "TTTTT": 7,
        "CCCCC": 6,
    }
    expected_result = {
        "AGCAG": 19,
        "GCATT": 8,
        "AAAAA": 12,
        "CCCCC": 6,
    }
    assert group_values_by_complement(test_case) == expected_result


def test_gc_skew():
    expected = np.array([
        0, -1, 0, 0, 1, 1, 1, -1, 0, 0, -1, 1, 1, -1, -1, 0, 0, 0, -1, 1, -1, -1
    ])
    assert (gc_skew("CATGGGCATCGGCCATACGCC", window_size=1) == expected).all()
