import random
from tkinter import N
from typing import Protocol
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from utils.meth_data import MethylationData, OneSampleMethylationData


class HeatmapMaker(Protocol):
    def plot(self, methdata: MethylationData, reads2plot: int) -> None:
        ...


class SimpleHeatmapMaker:
    """Makes individual heatmaps from data sets stored in MethylationData class instance.
    """
    def plot(self, methdata: MethylationData, reads2plot: int) -> None:
        for data in methdata.data:
            sorted_reads = _get_random_reads_for_heatmap(data, reads2plot)
            xaxisRange = len(data.meth_patterns[0])
            ax = _generate_heatmap(data=sorted_reads, xrange=xaxisRange)
            plt.savefig(data.file_name.strip(".sam") + "_heatmap.png")


def make_heatmap(methdata: MethylationData, heatmap_maker: HeatmapMaker, reads2plot: int) -> None:
    heatmap_maker.plot(methdata, reads2plot)

def _get_random_reads_for_heatmap(methdata: OneSampleMethylationData, reads2plot: int):
    """Generates a list of random methylation patterns for plotting."""
    if reads2plot >= methdata.reads_number:
        selected_reads = methdata.meth_patterns
    else:
        # generate a list of random indices for visualisation
        randomlist = []
        randomlist = random.sample(range(0, methdata.reads_number+1), reads2plot)
        
        # select the reads based on the list of random indices
        selected_reads = []
        selected_reads = [methdata.meth_patterns[ind] for ind in randomlist]
    sorted_reads = sorted(selected_reads, key=lambda x: sum(x), reverse=True)
    return sorted_reads

def _generate_heatmap(data: list, xrange: int, color="copper"):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(
        data,
        annot=False,
        xticklabels=np.arange(1,xrange+1,1),
        yticklabels=False,
        cbar=False,
        fmt="d",
        cmap=color,
        linewidths=0,
        ax=ax,
    )
    ax.set_xlabel("CpG site")
    ax.set_ylabel("Reads")
    return ax


# def get_random_reads_for_heatmap(reads2plot, total_reads_num, patterns):
#     """Generates a list of random methylation patterns for plotting."""
#     number = min(reads2plot, total_reads_num)

#     # generate a list of random indices for visualisation
#     randomlist = []
#     randomlist = random.sample(range(1, total_reads_num), number)

#     # select the reads based on the list of random indices
#     selected_reads = []
#     selected_reads = [patterns[ind] for ind in randomlist]
#     # sorted_reads = sorted(selected_reads, key=lambda x: x.meth_level, reverse=True)
#     sorted_reads = sorted(selected_reads, key=lambda x: sum(x), reverse=True)
#     return sorted_reads


# def heatmap(data, color, xrange):
#     plt.close("all")
#     fig, ax = plt.subplots(figsize=(9, 6))
#     sns.heatmap(
#         data,
#         annot=False,
#         xticklabels=np.arange(1,xrange+1,1),
#         yticklabels=False,
#         cbar=False,
#         fmt="d",
#         cmap=color,
#         linewidths=0,
#         ax=ax,
#     )
#     return fig


# def generate_heatmap(reads2plot, total_reads_num, patterns, color="copper"):
#     data = _get_random_reads_for_heatmap(reads2plot, total_reads_num, patterns)
#     xaxisRange = len(patterns[0])
#     return heatmap(data=data, color=color, xrange=xaxisRange)
