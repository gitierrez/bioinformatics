import pytest

from biomics.string.kmers import kmer_frequencies, count_ocurrences, kmer_locations


@pytest.mark.parametrize('s, t, expected', [
    ('GCGCG', 'GCG', 2),
    ('ACGTACGTACGT', 'CG', 3),
    ('TAACAGCCTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTGAGCCTTTGAGCCTTTTAGCCTTTCAGCCTTTAGCCTTTAAGCCTTTCCGCATCGAGCCTTTCAGCCTTTCGTAGCCTTTCGAGCCTTTAGCCTTTCAGCCTTTAGAGCCTTTAAGCCTTTAGTCGATGTAGCCTTTAGCCTTTAGCCTTTAGCCTTTGCAGCCTTTAGTAGGCAAGCCTTTTAGCCTTTGAGCCTTTCGAGCCTTTCTCGCTAGCCTTTAGCCTTTGGTGAGCCTTTTAGCCTTTAGCCTTTTCGCAGCCTTTTGAGCCTTTCTTGTTTGAATGGCAAGAGCCTTTTCGAGCCTTTAGCCTTTGAGCCTTTCAGCCTTTAAAAGCCTTTCGTTAGCCTTTAGCCTTTATCGAGCCTTTAAGCCTTTTATGCAAAGCCTTTGAGCCTTTAGCCTTTCAGCCTTTCAGCCTTTCATTGACAAGCCTTTCAGCCTTTAGCCTTTAGCCTTTCTCAGCCTTTGAGCCTTTGAGCCTTTGTCGAGCCTTTTTTCAGAGCCTTTTAGCCTTTAGCCTTTGAGCCTTTAGCCTTTAGCCTTTTACGAGCCTTTGCAAGCCTTTCAGCCTTTCCAAGCCTTTAGCCTTTGCTTTAGCCTTTCATGGGATAGCCTTTAGCCTTTATTAAGCCTTTTTTATCAAGCCTTTGTAGCCTTTAAGCCTTTCCAGCCTTTAGGAGCCTTTGTATAGCCTTTTGAGCCTTTCTACAGTAAAGCCTTTTTTGGTCAGCCTTTCTAGCCTTTGATAGCCTTTCTGAAGCCTTTGGCGGAGCCTTTCTGTTAACAGCCCAGCCTTTCTCATAGCCTTTGCGGTATCAGCCTTTGCAGCCTTTCTGGAGCGATAGCCTTTCAGCCTTTCCGAGCCTTTTTCAGAGCCTTTGAGCCTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTCCGAGCCTTTTCAGCCTTTACAGCCTTTTTAGCCTTTGAGCCTTTCACAGCCTTTGAGCTAGCCTTTAAGTTAAAGCCTTTAGCCTTTCAGCCTTTACATTAGCCTTTTAGCCTTTTCAGCCTTTAGAGCCTTTAGCCTTTGCTGAAGCCTTTAGTAGCCTTTAGCCTTTGCGAAGCCTTTCTGGTGCAACAAGTGAAGCCTTTGCCCTAGCCTTTGCTAGCCTTTCCGAGCCTTTGTCGATATAGCCTTTAGCCTTTAGAAAGCCTTTAGCCTTTGCTAGCCTTTATAGCCTTTAGCCTTTAGCCTTTCCCAGCCTTTAGCCTTTATCCTAAGCCTTTAGCCTTTTCCAGAAGCAGCCTTTTGATCAGAGCCTTTCTTCGGACTGCTCCCAGCCTTTAGCCTTTCAGCCTTTAGCCTTTAGCCTTTCAGCCTTTAGCCTTTTCTAGCCTTTAGCCTTTGTGTAGCCTTTCTAGCCTTTACGAGCCTTTGCCCAGCCTTTCCCAGCCTTTGAGAGCCTTTACCATATAGCCTTTACATAAGCCTTTGATGAGCCTTTAGCCTTTCGAGCCTTTCAGCCTTTACTCCAGCCTTTATAGCCTTTATATAGCCTTTCCTGTTAGGCCGTCGGTGCAGCCTTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTTAGCCTTTCAGCCTTTGCTAGCCTTTCCAGCCTTTACAGCCTTTTACCGAGCCTTTCCATCAGCCTTTAGCCTTTATATCTCTGATCGGGTAGCCTTTCGGCTAGCCTTTGGTAGCCTTTTTCAGCCTTTATGTAAAGCCTTTGTAGCCTTTGATGTGAGCCTTTAGAAGCCTTTGTCAGCCTTTTAGCCTTTAGCCTTTAGCCTTTTTAAGCCTTTTACAAGCCTTTACTCAGAGCCTTTACGAGCCTTTTAGCCTTTGCAGCCTTTTAGCCTTTTGATGAGCCTTTGCGGAGCCTTTTCTTTCAGCCTTTTGGCAGCCTTTAGCCTTTGTACAGCCTTTTTGAGCACAGCCTTTCGCGAAAGAGCCTTTATCAGCCTTTAAGCCTTTGCTAGCCTTTAGCCTTTTGAGCCTTTAGCCTTTGTATCTGTCTATCATCGAGCCTTTCTAAGCCTTTGCGGAAGCCTTTAGCCTTTGTCAGCCTTTCAAAGCCTTTAGCCTTTTATTCAAGCCTTTGAACCATAGCCTTTGGCAGCCTTTCAAGCCTTTGACGACAGCCTTTAGCCTTTCATTAGCCTTTTAGGAGGCTCATCCGTCTAGCCTTTAAATAGCCTTTAGCCTTTATAGCCTTTAAGCCTTTAGCCTTTTAAGCCTTTGAGAGCCTTTAAAGCCTTTAAACCAAGCCTTTGCGAAGCCTTTAGCCTTTAGCCTTTCGCAGCCTTTAGCCTTTCGAGCCTTTTGTAGCCTTTTGGAGAGCCTTTGGGCAAGCCTTTAGTATAAGCCTTTAGCCTTTTAGCCTTTCAAGCCTTTAGCCTTTAAGCCTTTGGCACAGCCTTTTGAGCCTTTCAGGAGCCTTTATTGGTGAGCCTTTAGTATAGCCTTTTCAGCCTTTGGCAGCCTTTAATGAAAGCCTTTGCTCAGCCTTTTTCAGCCTTTACAGCCTTTCAAGCCTTTAGCCACAAGCCTTTAGCCTTTAGCCTTTCAGCCTTTGCGAGCCTTTGTAGCCTTTAAGCCTTTCAGCCTTTAGCCTTTAGCCTTTTTCAAGCCTTTTCAGCCTTTCAAAGCCTTTCAAGCCTTTGAAGCCTTTCTAAGCCTTTGAGCCTTTGAGCCTTTGAGCCTTTAGCCTTTGTTCCTAGCCTTTATAGCCTTTTAGGCAGCCTTTCAGAGCCTTTTAAGCCTTTAGCCTTTCAGAAAGAGCCTTTAGCCCAGCCTTTTGATTAGCCTTTAGGGAACAGCCTTTAGCCTTTTAAGCCTTTGGTATACAATCAACGCAGCCTTTAGCCTTTAAGCCTTTTGGAGCCTTTCAGACTGATCCCAGCCTTTCAGCCTTTCTCAGCCTTTAAGCCTTTCTCCAAGCCTTTTGAGCCTTTTCGAGCCTTTAGTGAGCCTTTTGAAGCCTTTGTTTAGCCTTTTGTATAGGGTAGCCTTTAGCCTTTCCGGAAGCCTTTTGTAGCCTTTAAGCCTTTTGTCCGGGAAAGCCTTTGTAAGCCTTTAATGCAGCCTTTCCTATAGCCTTTAAGCCTTTCAGCCTTTTGGAGCCTTTTCTCAGCCTTTAGCCTTTCGCCAGCCTTTCTCCCGAGCAGCCTTTTAGAAAAAGCCTTTTAGCCTTTTACCGTGGACAGCCTTTCACGAGCCTTTACAGGCTAGCCTTTAGCCTTTGCTAGCCTTTTCCCAGCCTTTTGAGCCTTTAAGCCTTTCTAAGTTCTACGCTTGGGCTAAAGCCTTTAGCCTTTAAGCCTTTCAGCCTTTTGCAGCCTTTATATAACTTGAGCCTTTAGCCTTTAGCCTTTATAGCCTTTAGCCTTTTAGCCTTTTATATCCCTTAAGCCTTTGTAAGCCTTTAGCCTTTAAGCCTTTACGAGGAAAGCCTTTCATGCAGCCTTTAGCCTTTAGCCTTTGAGCCTTTCCAGCCTTTCAGCCTTTCAGCCTTTAGCCTTTAGCCTTTAGCCTTTTAGCCTTTATGAGCCTTTATAGCCTTTAGCCTTTTCACCAGCCTTTCCAGATGCACAAGCCTTTCAGCCTTTAGCCTTTCGAGCCTTTGGCTTATAGCCTTTCATCAGCCTTTCTAGCCTTTTAGCCTTTAGCCTTTAGCCTTTTCTAGCCTTTCAGCCTTTAGCCTTTTCGAAGCCTTTAGCCTTTTTAGCCTTTAGCTCAGCCTTTAGCCTTTATCTAACAGCCTTTAGCCTTTAGCCTTTAAAGCCTTTATGTCCAATTCTAACAGCCTTTAGCCTTTAAAGCCTTTGCAGCCTTTGAGCCTTTTAGCCTTTGAAGCCTTTAGCCTTTGTCAGCCTTTCCAGCCTTTTAGCCTTTAGCAGCCTTTAGTACGCCAGCCTTTAGCCTTTGTATAAGCCTTTAGCCTTTAGCCTTTCCACTAGCCTTTAGCCTTTAGAGGAGCGATAGCCTTTCAGCCTTTAGAAAGCCTTTGTTGCTGCTAGCCTTTGGGTTCTCAGCCTTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTTGTAGCCTTTTACATAGGATTGATTCAAAAGCCTTTTTGAGCCTTTCTGCATTAGCCTTTTCCTCTAGCCTTTAGCCTTTCGCAGCCTTTAGCCTTTTAGAGCCTTTAGATAGCCTTTCGCGACAGCCTTTTGTTTAGCCTTTAGCCTTTGTTAGCCTTTGAGCCTTTGAGCCTTTTAGCCTTTCCTAGCCTTTCAGCCTTTCCAAAGCCTTTGACAGGGTGTAGCCTTTCTAGCCTTTTTAGCCTTTAGCCTTTAAACTTAAGCCTTTTTAGCCTTTAGCCTTTCAACCCAGCCTTTAGCCTTTTAAGCCTTTAGCCTTTAGCCTTTTTAGAAGCCTTTTAGCCTTTAGCCTTTGGAGCCTTTCAGATCTCAGCCTTTTCGAGCCTTTTAGCCTTTTCAGAAAAGTAGCCTTTTTAGCAGCCTTTTAAAGCCTTTGGAGCCTTTAGCCTTTAGCCTTTGTAGCCTTTTCCCAAAAGCCTTTACAGCCTTTGTGAGCCTTTTAGTTCGTTTGAGCCTTTCCAGCCTTTCAGCCTTTAGCCTTTATAGCCTTTTGCGAGAAGCCTTTAAGCCTTTAGCCTTTTGACGTTCTAGAGCCTTTGGAGCCTTTCACGCGAGCCTTTCAAGCCTTTGACTCCGCAGCCTTTTCGCGACCAGCCTTTGCCGTGCCAGCCTTTAGCCTTTCAACACAGCCTTTAGCCTTTGGGCCGCAGAGCCTTTGAGTAGCCTTTAGCCTTTGACAGCCTTTAGCCTTTCTAGCCTTTGCAGCCTTTGTCTAGGTAGCCTTTAGCCTTTAGCCTTTCTAGCCTTTTAGCCTTTAGCCTTTTGAGCCTTTTGGAAGCCTTTCAGCCTTTAGCCTTTCGCGAGCCTTTGAGCCTTTACCCAGCCTTTACGGAGCCTTTAGCCTTTCCCATAGCCTTTAGCCTTTCCAGCCTTTAGCCTTTTAGCCTTTCAAATCTAAGCCTTTCGCATATATGGTAGCCTTTAGCCTTTAGCCTTTATGGTCCTTCAGTTTGAGCCTTTTAGAGCCTTTAAAGGAGCCTTTGTAAGACGAAGGTAGCCTTTAGCCTTTGCCAGCCTTTTTAGCCTTTAGCCTTTAAAAAGCCTTTGAGCCTTTAGCCTTTAGCCTTTGAGCCTTTAGCCTTTTCTCCTAGCCTTTCATAGCCTTTGAGCCTTTAGCCTTTTAGCCTTTTAGCCTTTAGCCTTTAGCCTTTGGAGGTCAGCCTTTATGTTAAAGCCTTTAGTTCCCAGCCTTTCAGCCTTTAGCCTTTAGCCTTTGAGCCTTTCAGCCTTTTAGCCTTTCAGCCTTTCAGCCTTTGAAGCCTTTTGTAGCCTTTGCCCGAGCCTTTAGCCTTTAGCCTTTCCCAACCCTGATCCGTAGCCTTTGGGCTGATCCTGAGCCTTTTCAGCCTTTAAGCCTTTAGCCTTTAGCCTTTGAGAAGCCTTTAGCCTTTCAGCCTTTAACAGCCTTTAAGCCTTTATAGCCTTTAGCCAGCCTTTGCAGCCTTTCAGTAGCCTTTAGCCTTTAGCCTTTCTAGCCTTTCTTGGAGCCTTTCCCAGCCTTTAAGAGCCTTTAGCCTTTTAGCCTTTCAGCCTTTAGCCTTTTCGTAGCCTTTGACCATTGTCAGCCTTTCTACTGAGCCTTTCATAGCCTTTTTTAGCCTTTCTAGCAGCCTTTGGAGCCTTTAGAAGAGCCTTTAGCCTTTTAAGCCTTTGAGCCTTTAACACAAGCCTTTATCTGGGCCGCGAGCCTTTTCAACCTAACTACAGCCTTTCTAAGCCTTTAGCCTTTAGCCTTTCAGCCTTTTAGCCTTTACCGAGCCTTTGCGGGAAGCCTTTAAAGAGCCTTTAGAAAAAGCCTTTGGGATAGCCTTTCCAGCCTTTCCAGCCTTTTTAGCCTTTTCCTCAAGATTTAGCCTTTGATGAAGCCTTTGAGCCTTTAGCCTTTCATTGAGCCTTTTAAGCCTTTCAGCCTTTTCTCATCAGCCTTTCACAGCCTTTCTACAGCCTTTAGCCTTTAGCCTTTGGAGCCTTTTCGCCCCGAGCCTTTAGCCTTTAGCCTTTTAGCCTTTCAGCCTTTGTAGCCTTTAGAGCCTTTGCTTAGCCTTTAGCCTTTAGTAGCCTTTAGATAGCCTTTTCTGGGAGCCTTTACAGCCTTTAGCCTTTAGCCTTTAGCCTTTTAAAGCCTTTCCCCAAAGCCTTTGTTGAGCCTTTAGCCTTTACAGTCTAGCCTTTAGCCTTTCAAGCCTTTACCTTAGCCTTTGGCAGCCTTTCTAGCCTTTAGCCTTTTCAGCCTTTAGCCTTTAAGCCTTTAGCCTTTTCGAGCCTTTGAGCCTTTAAGCCTTTATAAAAAGCCTTTAGCCTTTAAGCCTTTACCAGCCTTTAGCCTTTCAGCCTTTTATCGGAAAGCCTTTAAGCCTTTTAGCCTTTCAGCCTTTGAGCCTTTCAGCCTTTAGCCTTTGGCAAAGCCTTTTTGCAGCCTTTGGAAGCCTTTAGCCTTTTTCAAGCCTTTCAGCCTTTAGCCTTTGCACGTATTAGGAAGCCTTTTACTCTAAGCCTTTATCAGCCTTTAGCCTTTAGCCTTTAAGCCTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTAGCCTTTACGGTCAGCCTTTGGTAGCCTTTTCAGCCTTTAAGCCTTTAAGCCTTTGAGCCTTTAGCCTTTAGCCTTTGAGCCTTTAAGAGCCTTTCAGCCTTTTTTAGCCTTTTAGCCTTTGAGCCTTTCCTAGCCTTTCAAGCCTTTGAGCCTTTCGAAGCCTTTTAGCCTTTAGCCTTTAGCCTTTATGGAGCCTTTAGCCTTTAGCGGAGCCTTTGAGCCTTTACAGAGCCTTTAGCCTTTAGCCTTTTAAGCCTTTTGCAGCCTTTCAAAGAGCCTTTAGCCTTTACGGAGCCTTTAGCCTTTAAGCCTTTCTCACTAGCCTTTTTAGCCTTTGAGCCTTTATGACGAAGCCTTTAGCCTTTTGTCGTGACCTGAGCCTTTAGCCTTTACAGCCTTTCAGCCTTTAGCCTTTCTTAAAAGCCTTTTAGCCTTTTTGAGCCTTTACAGCCTTTCGAGCCTTTGAGCCTTTCCCAGCCTTTGAAGCCTTTTGGACAGAGCCTTTGCTAGCCTTTAGCCTTTTAGCCTTTAGCCTTTAGCCTTTACTTAGCCTTTTAGCCTTTATGGATAGCCTTTAGCCTTTGAGAGCCTTTGCCTAGCCTTTGAAGCCTTTTTAGCCTTTAACGAGCCTTTAGCCTTTAGCCTTTAGCCTTTAAGCCTTTAGCCTTTCGAGCCTTTCTCAGCCTTTGTAGCCTTTAGCCTTTAGAGCAGCCTTTAGCCTTTCCAGCCTTTAGCCTTTTCAGCCTTTAGCCTTTCAGCCTTTGCCCCGAGCACGTAGCCTTTACAGCCTTTAGCCTTTAGCCTTTTAGCCTTTACAGCCTTTTGAGCCTTTAGCCTTTGAAAGCCTTTTGAAGAGCCTTTCAGCCTTTCTTACTAGCCTTTGCAGCCTTTTAGCCTTTCCGAGCCTTTGATAGCCTTTGTCGGTAAGCCTTTGTAGAGCCTTTAGCCTTTAAGCCTTTGGTAAAGAGCCTTTTCAACAGCCTTTCGGAGCCTTTCGCTACAAGCCTTTTGGCCTAGCCTTTAGCCTTTCAGCCTTTCAAGAGCCTTTAGCCTTTCGCAGCCTTTATAGCCTTTCAGCCTTTCAGCCTTTAGCCTTTAGAGCCTTTGAGCCTTTCGTTATCTAAGCCTTTACTCCATAGCCTTTGAGCCTTTAGCCTTTGTCAGTCGAGCCTTTGTTCTTGAGCCTTTAGCCTTTGCAGCCTTTAGCCTTTTGTTTGTGGAGCCTTTAGCCTTTGAATACAGCCTTTAGCCTTTAGCCTTTAGCCTTTCTAGCCTTTCAGCAGCCTTTGTAGCCTTTGAACCAGCCTTTAGCCTTTTAGCCTTTTCCTTAGCCTTTCCAGCCTTTTAGTGAGCCTTTAGCCTTTGCACCAGCCTTTAGCCTTTAGCCTTTCAGCCTTTAGCCTTTCGAGCCTTTTAGCCTTTGAACAGCCTTTTGAGCCTTTGACGATATGAGCCTTTAGCCTTTTGTAGCCTTTTTTAGCCTTTGAACAGCCTTTGGAGTCAAGCCTTTACGCAGCCTTTCCAGCCTTTCAGCCTTTAGCCTTTGGTCAGCCTTTTCAGAGCCTTTGCGGTTAGCCTTTGAATAGCCTTTAAAGCCTTTCTCAGCCTTTGTAAGCCTTTAGCCTTTTAGCCTTTGTGAGCCTTTCAGCCTTTCCGAGCCTTTAGCCTTTGCCTACGGAAGCCTTTAGCCTTTGCTATCAGCTTGAGCCTTTTAGCCTTTAGTAGCAGCCTTTTAGCCTTTTAGCCTTTCAGCCTTTCTCTAGCCTTTAGCCTTTATCCGAGCCTTTACCAGCCTTTGAGCCTTTAGCCTTTATAGCCTTTATACGTAGCTAGCCTTTAGCCTTTAGAGCCTTTACCCTGTACCAGCCTTTAAGCCTTTCTCGTGAAGCCTTTAGCCTTTGAGCCTTTCGAGCCTTTAGCCTTTAGCCTTTAAGCCTTTTTGTGTGAGCCTTTAGCCTTTGGGGAGCCTTTAGCCTTTCAGCCTTTTAGCCTTTTCAAGCCTTTAGCCTTTAGCCTTTTGAGCCTTTAAAGCCTTTAGCCTTTAGGTAGCAAGCCTTTCGTTATAGCCTTTTATAAGCCTTTTTTAATGAGCCTTTAGCCTTTAGCCTTTGAGCAGCCTTTAGCCTTTAGTAGCCTTTTGATATTAGCCTTTCAGCCTTTAGCCTTTCCCCGAGCCTTTGTTAGAGCCTTTGCAGCCTTTGGAGCCTTTAGCCTTTCGGAGCCTTTAGCCTTTGGGACAGCCTTTAGCCTTTAGCCTTTGAAGCCTTTTGCAGCCTTTAAGATAGCCTTTGAGCCTTTTCAGCCTTTACAGCCTTTAAGCCTTTAGCCTTTGAGCCTTTGAGCCTTTTGAGCCTTTTAGCCTTTGTTGCAGCCTTTAGCCTTTAGCCTTTTAGCCTTTAGCCTTTAGCCTTTGAGCCTTTGAGCCTTTTAGCCTTTAGCCTTTGAGCCTTTTGGACAGCCTTTCTGAGCCTTTCGTAGCCTTTACCGCAAGCCTTTATAGCCTTTGAAGAGGAGCCTTTATAGCCTTTCAGAAGCCTTTTAAGCCTTTTCGCAGCCTTTTATCAGCCTTTAGCCTTTAGCCTTTTAGCCTTTCAGCCTTTAGCCTTTACAAGCCTTTAGCCTTTAGCCTTTATCAAGCCTTTCTAGCCTTTGAGCCTTTGTGAGCCTTTGTGTCAGCCTTTCAAGCCTTTTTAAGTACAGCCTTTACTCAGCCTTTATAGCCTTTGTCGTAAGCCTTTAGCCTTTAGCCTTTGAAAAGCCTTTACGCACAGACAAGTAGCCTTTCAGCCTTTAAGCCTTTGAGTATGTCCTTGAGCCTTTAAAAGAGCCTTTGGTAGCCTTTAGCCTTTAGCCTTTTATAGCCTTTAAGCCTTTAAGCCTTT', 'AGCCTTTAG', 294), 
])
def test_count_ocurrences(s, t, expected):
    assert count_ocurrences(s, t) == expected


def test_kmer_frequencies(genome):
    freqs = kmer_frequencies(genome, 4)
    assert freqs['GCAT'] == 3
    assert freqs['CATG'] == 3
    assert freqs['ATGA'] == 2
    assert freqs['TCGC'] == 1


def test_kmer_locations():
    assert kmer_locations('GATATATGCATATACTT', 'ATAT') == [1, 3, 9]