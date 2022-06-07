import random
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
            _generate_heatmap(sorted_reads, xaxisRange)
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
        randomlist = random.sample(range(0, methdata.reads_number), reads2plot)
        
        # select the reads based on the list of random indices
        selected_reads = []
        selected_reads = [methdata.meth_patterns[ind] for ind in randomlist]
    sorted_reads = sorted(selected_reads, key=lambda x: sum(x), reverse=True)
    return sorted_reads

def _generate_heatmap(data: list, xrange: int, color="copper"):
    plt.close("all")
    reads_number = len(data)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(
        data,
        annot=False,
        xticklabels=np.arange(1,xrange+1,1),  # type: ignore
        yticklabels=False,  # type: ignore
        cbar=False,
        fmt="d",
        cmap=color,
        linewidths=0,
        ax=ax,
    )
    ax.set_xlabel("CpG site")
    ax.set_ylabel(f"Reads ({reads_number})")
    ax.set_title("Methylation of individual reads",
        fontsize=14,
        color="black", # palette[3]
        fontweight="normal", #'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight'    
    )
    plt.tight_layout()
    return