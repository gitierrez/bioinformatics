import io
import streamlit as st

from biomics.string.kmers import kmer_frequencies, count_ocurrences, kmer_locations
from biomics.genetics.utils import complement, group_values_by_complement
from biomics.plotting import plot_kmer_locations
from biomics.misc import sort_dict

# TODO:
# When does it make sense to treat complementary sequences as the same for counting purposes?
st.title("Prokaryomers")
st.write(
    "Helps answers questions like 'where is the origin of replication?' "
    "and 'what are interesting k-mers?' in prokaryotic genomes."
)

uploaded_file = st.file_uploader("Upload genome file", type=["txt"])
if uploaded_file is not None:
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    genome = stringio.read()

    # TODO: add widget for clumps
    t1, t2 = st.tabs(['Frequent k-mers', 'Search k-mer'])

    with t1:
        k = st.number_input("K-mer size", value=3, min_value=1, max_value=len(genome))
        group_with_complement = st.checkbox(
            "Group with complementary sequence",
            help="If checked, 5'-ACG-3' and 5'-CGT-3' will be counted as the same k-mer.",
            value=False,
            key="kmer_freq_complement"
        )

        if st.button("Run", key="kmer_freq_run"):
            kmer_freqs = kmer_frequencies(genome, k)
            if group_with_complement:
                kmer_freqs = group_values_by_complement(kmer_freqs)
            kmer_freqs = sort_dict(kmer_freqs, ascending=False)
            # grab first 10 k-mers
            kmer_freqs = {kmer: freq for i, (kmer, freq) in enumerate(kmer_freqs.items()) if i < 10}

            # TODO: automatically detect the number of relevant points
            # Samples are not independent, so binomial approximation doesn't work
            # an alternative is to use Markov chains, as explained here:
            # https://stats.stackexchange.com/a/362638
            # also, is it viable to give a "hint" of what the sequence might represent?
            # e.g. TTAATATAT --> telomere, GCA --> some aminoacid, GTACCGAGC --> ori
            # Bacterial DnaA boxes (for replication origin) are usually 9 nucleotides long
            # Idea to find relevant k: experiment with multiple k, find the most frequent patterns and how "surprising"
            # they are - this requires calculating the probability first. Then, return the most "surprising" ones,
            # these are likely to be biologically relevant.

            for i, (kmer, freq) in enumerate(kmer_freqs.items()):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.text(kmer)
                with c2:
                    st.text(freq)
                with c3:
                    locations = kmer_locations(genome, kmer)
                    st.image(plot_kmer_locations(genome, kmer_length=len(kmer), locations=locations, figsize=(1, 0.1)))

    with t2:
        kmer = st.text_input("Sequence", value="TATTACTGCT")

        group_with_complement = st.checkbox(
            "Group with complementary sequence",
            help="If checked, 5'-ACG-3' and 5'-CGT-3' will be counted as the same k-mer.",
            value=False,
            key="kmer_search_complement"
        )

        if st.button("Run", key="kmer_search_run"):
            ocurrences = count_ocurrences(genome, kmer)
            locations = kmer_locations(genome, kmer)
            if group_with_complement:
                kmer_comp = complement(kmer)
                ocurrences += count_ocurrences(genome, kmer_comp)
                locations += kmer_locations(genome, kmer_comp)
                st.write(f"Sequences {kmer} and its complement {kmer_comp} appear {ocurrences} times in the genome.")
            else:
                st.write(f"Sequence {kmer} appears {ocurrences} times in the genome.")
            st.image(plot_kmer_locations(genome, kmer_length=len(kmer), locations=locations, figsize=(5, 0.5)))
