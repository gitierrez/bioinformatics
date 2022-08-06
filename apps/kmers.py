import io
import streamlit as st

from biomics.string.kmers import kmer_frequencies
from biomics.genetics.utils import group_values_by_complement
from biomics.plotting import plot_kmer_locations
from biomics.misc import sort_dict

# TODO:
# When does it make sense to treat complementary sequences as the same for counting purposes?
st.title("K-mers")

uploaded_file = st.file_uploader("Upload genome file", type=["txt"])
if uploaded_file is not None:
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    genome = stringio.read()

    k = st.number_input("K-mer size", value=3, min_value=1, max_value=len(genome))
    group_with_complement = st.checkbox(
        "Group with complementary sequence",
        help="If checked, 5'-ACG-3' and 5'-CGT-3' will be counted as the same k-mer.",
        value=False
    )

    if st.button("Run"):
        kmer_freqs = kmer_frequencies(genome, k)
        print(kmer_freqs)
        if group_with_complement:
            kmer_freqs = group_values_by_complement(kmer_freqs)
        kmer_freqs = sort_dict(kmer_freqs, ascending=False)
        # grab first 10 k-mers
        kmer_freqs = {kmer: freq for i, (kmer, freq) in enumerate(kmer_freqs.items()) if i < 10}

        print(kmer_freqs)

        # TODO: automatically detect the number of relevant points
        # Samples are not independent, so binomial approximation doesn't work
        # an alternative is to use Markov chains, as explained here:
        # https://stats.stackexchange.com/a/362638
        # also, is it viable to give a "hint" of what the sequence might represent?
        # e.g. TTAATATAT --> telomere, GCA --> some aminoacid, GTACCGAGC --> ori
        # Bacterial DnaA boxes (for replication origin) are usually 9 nucleotides long

        for i, (kmer, freq) in enumerate(kmer_freqs.items()):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.text(kmer)
            with c2:
                st.text(freq)
            with c3:
                st.image(plot_kmer_locations(genome, kmer, figsize=(1, 0.1)))
