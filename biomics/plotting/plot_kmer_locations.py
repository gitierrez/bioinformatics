import io
import numpy as np
import matplotlib.pyplot as plt

from biomics.string.kmers import kmer_locations


def plot_kmer_locations(genome, kmer, figsize=(2, 1)):
    """
    Returns numpy array with the kmer locations plot.
    """
    locations = kmer_locations(genome, kmer)

    template = np.arange(len(genome))
    locs = np.zeros(len(genome))
    for location in locations:
        locs[location:location + len(kmer)] = 1

    fig, ax = plt.subplots(figsize=figsize)

    ax.scatter(template[locs == 0], template[locs == 0] * 0, s=1, marker='s', color='white')
    ax.scatter(template[locs == 1], template[locs == 1] * 0, s=1, marker='s', color='orange')

    ax.set_ylim([-1, 1])
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])

    io_buf = io.BytesIO()
    fig.savefig(io_buf, format='raw')
    io_buf.seek(0)
    img_arr = np.reshape(
        np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
        newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1)
    )
    io_buf.close()
    return img_arr
