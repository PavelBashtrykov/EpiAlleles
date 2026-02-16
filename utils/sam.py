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
            sequence, sam_position = _parse_sam_line(i)
            meth_pattern = _get_meth_pattern(coordinates=coordinates, sequence=sequence, sam_position=sam_position)
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

def _parse_sam_line(line: str) -> tuple:
    """Parse SAM line and extract sequence and alignment position.

    Returns tuple of (sequence, sam_position_0based)
    """
    fields = line.strip().split("\t")
    sequence = fields[9]
    sam_position = int(fields[3]) - 1  # SAM uses 1-based, convert to 0-based
    return sequence, sam_position

def _get_meth_pattern(coordinates: list, sequence: str, sam_position: int) -> list:
    """Analyse methylation pattern of a bisulfite read.

    Args:
        coordinates: List of reference CpG positions (0-based)
        sequence: Read sequence
        sam_position: Alignment position of read in reference (0-based)
    """
    meth_pattern = []
    for start in coordinates:
        # Calculate position in read: reference_position - read_alignment_position
        read_pos = start - sam_position

        # Check if position is within read bounds
        if 0 <= read_pos < len(sequence) - 1:
            fragment = sequence[read_pos : read_pos + 2]
            if fragment == "CG":
                meth_pattern.append(MethFlags.methylated_motif_flag)
            elif fragment == "TG":
                meth_pattern.append(MethFlags.unmethylated_motif_flag)
            else:
                meth_pattern.append(MethFlags.missing_motif_flag)
        else:
            # Position outside read bounds
            meth_pattern.append(MethFlags.missing_motif_flag)
    return meth_pattern

def _calculate_meth_level(meth_pattern: list):
    """Calculates methylation level of a bisulfite read."""
    if MethFlags.missing_motif_flag in meth_pattern:
        return None
    else:
        return meth_pattern.count(MethFlags.methylated_motif_flag) / len(meth_pattern)