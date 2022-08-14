import numpy as np
import matplotlib.pyplot as plt

from biomics.plotting.utils import matplotlib_to_numpy


def plot_gc_skew_curve(gc_skew: np.ndarray, figsize=(20, 10)):
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(gc_skew)
    return matplotlib_to_numpy(fig)
