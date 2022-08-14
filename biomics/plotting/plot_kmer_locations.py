import numpy as np
import matplotlib.pyplot as plt

from biomics.plotting.utils import matplotlib_to_numpy


def plot_kmer_locations(genome_length, locations, figsize=(2, 0.2), s=10):
    """
    Returns numpy array with the kmer locations plot.
    """
    template = np.arange(genome_length)
    locs = np.zeros(genome_length)
    for location in locations:
        locs[location] = 1

    fig, ax = plt.subplots(figsize=figsize)

    ax.scatter(template[locs == 0], template[locs == 0] * 0, s=s, marker='s', color='white')
    ax.scatter(template[locs == 1], template[locs == 1] * 0, s=s, marker='s', color='orange')

    ax.set_ylim([-1, 1])
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])

    return matplotlib_to_numpy(fig)
