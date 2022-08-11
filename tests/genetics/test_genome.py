import os
import pytest

from biomics.genetics import ProkaryoticGenome


@pytest.fixture()
def correct_genome_file():
    with open('test-sample-genome.txt', 'w') as f:
        f.write('ACCCGAAAGCATT')
    yield 'test-sample-genome.txt'
    os.remove('test-sample-genome.txt')


@pytest.fixture()
def incorrect_genome_file():
    with open('test-sample-genome.txt', 'w') as f:
        f.write('ACCCGAAAGCZATT')
    yield 'test-sample-genome.txt'
    os.remove('test-sample-genome.txt')


def test_instantiate_genome_from_correct_file(correct_genome_file):
    genome = ProkaryoticGenome.from_file(correct_genome_file)
    assert genome.value == 'ACCCGAAAGCATT'


def test_instantiate_genome_from_incorrect_file_raises_exception(incorrect_genome_file):
    with pytest.raises(ValueError):
        _ = ProkaryoticGenome.from_file(incorrect_genome_file)


def test_locations_of_sequence_without_complement_and_variations():
    genome = ProkaryoticGenome('GATATATGCATATACTT')
    sequence = 'ATAT'
    locations = genome.locations_of_sequence(
        sequence, include_complement=False, include_variations_up_to=0
    )
    assert locations == [1, 3, 9]


def test_locations_of_sequence_with_variations():
    genome = ProkaryoticGenome(
        'CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAAT'
    )
    sequence = 'ATTCTGGA'
    assert genome.locations_of_sequence(
        sequence,
        include_complement=False,
        include_variations_up_to=3
    ) == [6, 7, 26, 27]


def test_gc_skew():
    genome = ProkaryoticGenome('CATGGGCATCGGCCATACGCC')
    expected = [-1, -1, -1, 0, 1, 2, 1, 1, 1, 0, 1, 2, 1, 0, 0, 0, 0, -1, 0, -1, -2]
    assert all(genome.gc_skew() == expected)
