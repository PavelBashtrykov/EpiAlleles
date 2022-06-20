from utils.meth_data import MethFlags, MethylationData, OneSampleMethylationData

def extract_meth(coordinates: list, samfiles: list, storage: MethylationData):
    """Extracts methylation patterns and methylation levels of individual reads from a list of sam files."""
    for s in samfiles:
        meth = _get_meth_sam(coordinates, s)
        storage.add(meth)


def _get_meth_sam(coordinates: list, samfile: str) -> OneSampleMethylationData:
    """Extracts methylation patterns and methylation levels of individual reads in a sam file.

    Returns
    -------
    OneSampleMethylationData class with the following variables:
        file_name: str,
        reads_number: int,
        meth_patterns: list,
        meth_levels: list
    """
    total_read_number = 0
    all_meth_patterns = []
    all_meth_levels = []
    with open(samfile, "r") as fh:
        for i in fh:
            if i.startswith("@"):
                continue
            sequence = _parse_sam_line(i)
            meth_pattern = _get_meth_pattern(coordinates=coordinates, sequence=sequence)
            meth_level = _calculate_meth_level(meth_pattern)
            if not meth_level:
                continue
            all_meth_patterns.append(meth_pattern)
            all_meth_levels.append(meth_level)
            total_read_number += 1
    return OneSampleMethylationData(
        file_name=samfile,
        reads_number=total_read_number,
        meth_patterns=all_meth_patterns,
        meth_levels=all_meth_levels,
    )

def _parse_sam_line(line: str) -> str:
    return line.strip().split("\t")[9]

def _get_meth_pattern(coordinates: list, sequence: str) -> list:
    """Analyse methylation pattern of a bisulfite read."""
    meth_pattern = []
    for start in coordinates:
        fragment = sequence[start : start + 2]
        if fragment == "CG":
            meth_pattern.append(MethFlags.methylated_motif_flag)
        elif fragment == "TG":
            meth_pattern.append(MethFlags.unmethylated_motif_flag)
        else:
            meth_pattern.append(MethFlags.missing_motif_flag)
    return meth_pattern

def _calculate_meth_level(meth_pattern: list):
    """Calculates methylation level of a bisulfite read."""
    if MethFlags.missing_motif_flag in meth_pattern:
        return None
    else:
        return meth_pattern.count(MethFlags.methylated_motif_flag) / len(meth_pattern)