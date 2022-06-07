#!/usr/bin/env python3.10
import argparse
import os

import matplotlib.pyplot as plt

from utils.fasta import get_coordinates
from utils.heatmap import SimpleHeatmapMaker, make_heatmap
from utils.histogram import MultipleDataHistogramMaker, SingleDataHistogramMaker, make_histogram
from utils.meth_data import MethylationData
from utils.sam import extract_meth
from utils.save import WriteMethlation2CSV, save_data


def main():
    """Computes methylation of individual reads and generates a heatmap.
    
    Inputs
    ------
    Save the script in a working directory containing one fasta file and 1 or more sam files.
    Fasta file is a source of CpG sites coordinates.
    Methylated reads are passed as sam files.
    
    Returns
    -------
    For every sam file:
        - csv file with methylation level of individual reads
        - histogram showing distribution of methylation levels
        - heatmap showing methylation pattern of selected number of reads
    """
    ####################################################################################
    # Settings
    ####################################################################################
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", help="Fasta file used to generate sam files, will be used to get positions of CpG sites.", type=str, required=False)
    parser.add_argument("--sam", help="A list of samfiles for the analysis. If not provided CWD will be read.", type=str, required=False)
    parser.add_argument("--mode", help="Options: single or multiple. Defines how many data sets to plot on a histogram (default: single).", type=str, required=False)
    parser.add_argument("--reads2plot", help="Number of reads to visualize on a heatmap (default: 10000)", type=int, required=False)
    args = parser.parse_args()

    workdir = os.path.dirname(os.path.realpath(__file__))
    filenames = os.listdir(workdir)

    # get fasta file
    fastafile = None
    if args.fasta:
        fastafile = args.fasta
    else:
        fastafile = [f for f in filenames if f.endswith(".fa") or f.endswith(".fasta")]
    if not fastafile:
        print("There is no fasta file in the working directory and none was passed in command line, provide one.")
        return
    elif len(fastafile)>1:
        print(f"There is more than one fasta file in the working dir, leave only one.")
        return
    print(f"Fasta file: {fastafile}")


    # get sam files
    samfiles = []
    if args.sam:
        samfiles.append(args.sam)
    else:
        samfiles = [f for f in filenames if f.endswith(".sam")]
    print(f"SAM files: {samfiles}")

    # histogram plotting mode
    if not args.mode:
        histmode = SingleDataHistogramMaker()
    elif args.mode == "multiple":
        histmode = MultipleDataHistogramMaker()
    elif args.mode == "single":
        histmode = SingleDataHistogramMaker()
    else:
        print(f"--mode can take only one of two parameters \"single\" or \"multiple\"")
        return

    # reads to plot on a heatmap
    reads2plot = 10000
    if args.reads2plot:
        reads2plot = args.reads2plot
    print(f"reads2plot: {reads2plot}")

    ####################################################################################
    # analysis
    ####################################################################################
    coordinates = get_coordinates(fastafile[0])
    meth_data = MethylationData()
    extract_meth(coordinates, samfiles, meth_data)
    make_histogram(meth_data, histmode)
    make_heatmap(meth_data, SimpleHeatmapMaker(), reads2plot)
    save_data(meth_data, WriteMethlation2CSV())


if __name__ == "__main__":
    main()