import argparse
import os

import matplotlib.pyplot as plt

from utils.fasta import get_coordinates
from utils.heatmap import generate_heatmap
from utils.histogram import generate_histogram, generate_histogram_2sets
from utils.sam import get_meth_sam

# Plot 2 data sets on one


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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reads2plot",
        help="Number of reads to visualize on a heatmap (default: 10000)",
        type=int,
        required=False,
    )
    parser.add_argument(
        "--out", help="Name of the heatmap file .png", type=str, required=False
    )
    args = parser.parse_args()

    workdir = os.path.dirname(os.path.realpath(__file__))
    filenames = os.listdir(workdir)

    # get fasta file
    fastafile = None
    for f in filenames:
        if f.split(".")[-1] == "fasta" or f.split(".")[-1] == "fa":
            fastafile = f
            print("FASTA file: ", f)
            break
    if not fastafile:
        print("There is no fasta file in the working directory, provide at least one.")
        return

    # get sam files
    samfiles = []
    for f in filenames:
        if f.split(".")[-1] == "sam":
            samfiles.append(f)
    if not samfiles:
        print("There are no sam files in the working directory, provide at least one.")
        return

    # reads to plot on a heatmap
    reads2plot = 10000
    if args.reads2plot:
        reads2plot = args.reads2plot
    print(f"reads2plot: {reads2plot}")

    # analysis
    coordinates = get_coordinates(fastafile)
    plot_data = []
    for s in samfiles:
        print(f"sam file: {s}")
        tag = s.strip(".sam")
        num, pat, meth = get_meth_sam(coordinates=coordinates, samfile=s)
        plot_data.append(meth)
        generate_heatmap(reads2plot=reads2plot, total_reads_num=num, patterns=pat)
        plt.savefig(tag + "_heatmap.png")
        plt.close("all")
        generate_histogram(data=meth)
        plt.savefig(tag + "_histogram.png")
        with open(tag + ".csv", "w+") as fh:
            fh.write("\n".join([str(i) for i in meth]))
    plt.close()
    generate_histogram_2sets(plot_data)
    plt.savefig("overlay.png")


if __name__ == "__main__":
    main()
