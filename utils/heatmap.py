import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def get_random_reads_for_heatmap(reads2plot, total_reads_num, patterns):
    """Generates a list of random methylation patterns for plotting."""
    number = min(reads2plot, total_reads_num)

    # generate a list of random indices for visualisation
    randomlist = []
    randomlist = random.sample(range(1, total_reads_num), number)

    # select the reads based on the list of random indices
    selected_reads = []
    selected_reads = [patterns[ind] for ind in randomlist]
    # sorted_reads = sorted(selected_reads, key=lambda x: x.meth_level, reverse=True)
    sorted_reads = sorted(selected_reads, key=lambda x: sum(x), reverse=True)
    return sorted_reads


def heatmap(data, color, xrange):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(
        data,
        annot=False,
        xticklabels=np.arange(1,xrange+1,1),
        yticklabels=False,
        cbar=True,
        fmt="d",
        cmap=color,
        linewidths=0,
        ax=ax,
    )
    return fig


def generate_heatmap(reads2plot, total_reads_num, patterns, color="copper"):
    data = get_random_reads_for_heatmap(reads2plot, total_reads_num, patterns)
    xaxisRange = len(patterns[0])
    return heatmap(data=data, color=color, xrange=xaxisRange)
