import pytest

from biomics.genetics import DNASequence


def test_instantiation_fails_with_invalid_sequence():
    with pytest.raises(ValueError):
        DNASequence('ACGUACGT')


def test_complement():
    seq = DNASequence('ATCG')
    assert seq.complement.value == 'CGAT'
