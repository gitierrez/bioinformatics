import pytest
from biomics.genetics.utils import group_values_by_complement


@pytest.mark.skip(reason='Refactoring in process')
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
