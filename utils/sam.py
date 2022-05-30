import pandas as pd

METHYLATED_CG_FLAG = 1
UNMETHYLATED_CG_FLAG = 0
MISSING_CG_FLAG = "!"


def analyse_meth_pattern(
    coordinates,
    sequence,
    methylated_cg_flag=METHYLATED_CG_FLAG,
    unmethylated_cg_flag=UNMETHYLATED_CG_FLAG,
    missing_cg_flag=MISSING_CG_FLAG,
):
    """Analyse methylation pattern of a bisulfite read."""
    meth_pattern = []
    for start in coordinates:
        fragment = sequence[start : start + 2]
        if fragment == "CG":
            meth_pattern.append(methylated_cg_flag)
        elif fragment == "TG":
            meth_pattern.append(unmethylated_cg_flag)
        else:
            meth_pattern += (
                missing_cg_flag  # if we want to keep reads with partial CG information
            )
    return meth_pattern


def calculate_meth_level(meth_pattern):
    """Calculates methylation level of a bisulfite read."""
    if "!" in meth_pattern:
        return None
    else:
        return meth_pattern.count(METHYLATED_CG_FLAG) / len(meth_pattern)


def get_meth_sam2(coordinates, samfile):
    """Extract methylation patterns and methylation levels of individual reads in a sam file."""
    total_read_number = 0
    all_meth_patterns = []
    all_meth_levels = []
    with open(samfile, "r") as fh:
        for i in fh:
            meth_pattern = analyse_meth_pattern(coordinates, sequence=i.strip())
            meth_level = calculate_meth_level(meth_pattern)
            if not meth_level:
                continue
            all_meth_patterns.append(meth_pattern)
            all_meth_levels.append(meth_level)
            total_read_number += 1

    return total_read_number, all_meth_patterns, all_meth_levels


def get_meth_sam(coordinates, samfile):
    """Extract methylation patterns and methylation levels of individual reads in a sam file."""
    total_read_number = 0
    all_meth_patterns = []
    all_meth_levels = []
    df = pd.DataFrame()
    with open(samfile, "r") as fh:
        for i in fh:
            meth_pattern = analyse_meth_pattern(coordinates, sequence=i.strip())

            meth_level = calculate_meth_level(meth_pattern)
            if not meth_level:
                continue
            all_meth_patterns.append(meth_pattern)
            all_meth_levels.append(meth_level)
            total_read_number += 1
    df["meth_pattern"] = all_meth_patterns
    df["meth_level"] = all_meth_levels
    df["sample"] = samfile.strip(".sam")
    return total_read_number, all_meth_patterns, all_meth_levels, df
