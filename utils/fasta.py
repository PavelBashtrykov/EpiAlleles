def get_seq_from_fasta(fastafile) -> str:
    """Gets sequence from a fastafile.
    """
    sequence = ""
    with open(fastafile, "r") as fh:
        line = fh.readline()
        while line:
            if line.startswith(">"):
                line = fh.readline()
            sequence += line.strip()
            line = fh.readline()
    return sequence


def find_motif_coordates(sequence, motif="CG") -> list:
    """Finds motif (default: CG) coordinates in a sequence.
    """
    coordinates = []
    seq = sequence.upper()
    length = len(seq)
    motif_len = len(motif)
    index = 0
    while index < length:
        index = seq.find(motif, index)
        if index == -1:
            break
        coordinates.append(index)
        index += motif_len
    return coordinates


def get_coordinates(fastafile) -> list:
    sequence = get_seq_from_fasta(fastafile)
    return find_motif_coordates(sequence)
