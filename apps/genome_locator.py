import io
import numpy as np
import streamlit as st

from biomics.genetics import ProkaryoticGenome
from biomics.plotting import plot_kmer_locations, plot_gc_skew_curve


st.title("Sequence Finder for Prokaryotes")

uploaded_file = st.file_uploader("Upload genome file", type=["txt"])
if uploaded_file is not None:
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    genome = ProkaryoticGenome(stringio.read())

    # TODO: add widget for clumps
    t1, t2 = st.tabs(["Sequence locator", "DnaA box finder"])

    with t1:
        sequence = st.text_input("Sequence", value="GTACCGAGC")

        include_complement = st.checkbox(
            "Include complementary sequence",
            help="If checked, 5'-ACG-3' and 5'-CGT-3' will be counted as the same sequence.",
            value=False,
            key="chk_complement",
        )

        include_mutations = st.checkbox(
            "Include mutations",
            help="If checked, variations up to a determined degree will be counted as the same sequence.",
            value=False,
            key="chk_mutations",
        )
        if include_mutations:
            max_mutations = st.slider(
                "Maximum number of mutations",
                min_value=1,
                max_value=3,
                value=1,
                key="slider_mutations",
            )
        else:
            max_mutations = 0

        if st.button("Locate", key="btn_sequence-locator"):
            with st.spinner("Locating sequences in genome..."):
                locations = genome.locations_of_sequence(
                    sequence,
                    include_complement=include_complement,
                    include_variations_up_to=max_mutations,
                )

                locations_plot = plot_kmer_locations(
                    genome_length=len(genome),
                    locations=locations,
                    figsize=(10, 0.1),
                    s=1,
                )

            st.write(f"Found {len(locations)} occurrences.")
            st.image(locations_plot)

    with t2:
        window_size = st.number_input(
            "Window size",
            min_value=100,
            max_value=10000,
            value=1000,
        )

        if st.button("Find DnaA-box candidates", key="btn_dnaa-boxes"):
            with st.spinner("Finding DnaA-box candidates..."):
                candidates, freq = genome.ori_box_candidates(window_size)
                gc_skew = genome.gc_skew()
                skew_curve = plot_gc_skew_curve(gc_skew, figsize=(20, 10))

            st.write(
                f"Found {len(candidates)} candidates with frequency {freq} around "
                f"suspected ori in position {np.argmin(gc_skew)}."
            )
            st.table(candidates)
            st.image(skew_curve)


# TODO: automatically detect the number of relevant points
# Samples are not independent, so binomial approximation doesn't work
# an alternative is to use Markov chains, as explained here:
# https://stats.stackexchange.com/a/362638
# also, is it viable to give a 'hint' of what the sequence might represent?
# e.g. TTAATATAT --> telomere, GCA --> some aminoacid, GTACCGAGC --> ori
# Bacterial DnaA boxes (for replication origin) are usually 9 nucleotides long
# Idea to find relevant k: experiment with multiple k, find the most frequent patterns and how 'surprising'
# they are - this requires calculating the probability first. Then, return the most 'surprising' ones,
# these are likely to be biologically relevant.
