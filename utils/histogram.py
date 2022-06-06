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
            formated_data = _format_data_2_df(methdata=data)
            _generate_histogram(data=formated_data)
            plt.savefig(data.file_name.strip(".sam") + "_histogram.png")


class MultipleDataHistogramMaker:
    def plot(self, methdata: MethylationData) -> None:
        main_df = pd.DataFrame(columns=["meth_pattern", "meth_level", "sample"])
        for data in  methdata.data:
            formated_data = _format_data_2_df(methdata=data)
            main_df = pd.concat([main_df, formated_data], axis=0, ignore_index=True)
        _generate_histogram_multiple_data(data=main_df)
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

def _generate_histogram(data: pd.DataFrame, color="b"):
    fig, ax = plt.subplots()
    sns.color_palette()
    sns.histplot(
        data=data,
        x="meth_level",
        hue="sample",
        bins=10,
        stat="probability",
        ax=ax,
    )
    ax.set_xlim(0,1)
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


# def generate_histogram(data, color="b"):
#     fig, ax = plt.subplots()
#     sns.set_theme(style="ticks")
#     sns.color_palette("Paired")
#     sns.histplot(data=data, stat="probability", bins=10, color=color, ax=ax)
#     ax.set_xlim(0,1)
#     # sns.despine()


# def generate_histogram_kde(data, color="0.8"):
#     ax = sns.histplot(
#         data=data,
#         stat="probability",
#         bins=10,
#         kde=True,
#         color=color,
#         kde_kws={"bw_adjust": 2},
#     )
#     ax.lines[0].set_color("crimson")
#     # sns.despine()


# def generate_histogram_2sets(data):
#     # sns.set_theme(style="ticks")
#     # sns.color_palette("Paired")
#     fig, ax = plt.subplots()
#     sns.color_palette()
#     sns.histplot(
#         data=data,
#         x="meth_level",
#         hue="sample",
#         bins=10,
#         stat="probability",
#         common_norm=False,
#         # multiple="stack",
#         # kde=True,
#         ax=ax,
#     )
#     ax.set_xlim(0,1)

