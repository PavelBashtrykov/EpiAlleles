from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


from typing import Protocol

from utils.meth_data import MethylationData, OneSampleMethylationData

class HistogramMaker(Protocol):
    """Interface for any histogarm maker"""
    def plot(self, methdata: MethylationData) -> None:
        ...

class SingleDataHistogramMaker:
    """Makes individual histograms from data stored in MethylationData class instance.
    """
    def plot(self, methdata: MethylationData) -> None:
        for data in  methdata.data:
            formated_data = _format_data_2_df(data)
            _generate_histogram(formated_data)
            plt.savefig(data.file_name.strip(".sam") + "_histogram.png")


class MultipleDataHistogramMaker:
    def plot(self, methdata: MethylationData) -> None:
        main_df = pd.DataFrame(columns=["meth_pattern", "meth_level", "sample"])
        for data in  methdata.data:
            formated_data = _format_data_2_df(data)
            main_df = pd.concat([main_df, formated_data], axis=0, ignore_index=True)
        _generate_histogram_multiple_data(main_df)
        plt.savefig("overlay_histogram.png")

def make_histogram(methdata: MethylationData, hist_maker: HistogramMaker) -> None:
    """Make a histogram"""
    hist_maker.plot(methdata)

def _format_data_2_df(methdata: OneSampleMethylationData) -> pd.DataFrame:
    df = pd.DataFrame()
    df["meth_pattern"] = methdata.meth_patterns
    df["meth_level"] = methdata.meth_levels
    df["sample"] = methdata.file_name.strip(".sam")
    return df

def _generate_histogram(data: pd.DataFrame):
    plt.close("all")
    palette = sns.color_palette("Paired") # ("Blues", 9)
    ax = sns.histplot(data, x='meth_level',
        stat="probability",
        bins=10,
        binrange=(0,1.),
        color=palette[2],
        edgecolor="white", # palette[3],
        linewidth=1,
        kde=False,
        cbar=True,
        # cbar_kws=dict(shrink=.75)
        )
    # ax.lines[0].set_color('crimson') # for kde=True
    ax.set_xlim(-0.05,1)
    ax.set_xlabel("Methylation level")
    ax.set_ylabel("Reads fraction")
    ax.set_title("Distribution of methylation levels within the sample", 
        fontsize=14,
        color="black", # palette[3]
        fontweight="normal", #'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight'
        )
    sns.despine()
    return ax

def _generate_histogram_multiple_data(data: pd.DataFrame):
    fig, ax = plt.subplots()
    sns.histplot(
        data=data,
        x="meth_level",
        hue="sample",
        bins=10,
        stat="probability",
        common_norm=False,
        kde=False,
        ax=ax,
    )
    ax.set_xlim(0,1)
    return ax