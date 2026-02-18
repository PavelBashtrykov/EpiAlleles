#!/usr/bin/env python3.10
"""
Test script for the --retain-methylated flag feature.
Tests that the flag correctly filters reads with at least one methylated CpG.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add project to path
sys.path.insert(0, '/home/ubuntu/projects/EpiAlleles')

from utils.fasta import get_coordinates
from utils.meth_data import MethylationData, MethFlags
from utils.sam import extract_meth, _get_meth_sam, _parse_sam_line, _get_meth_pattern, _calculate_meth_level


def test_methylation_flags():
    """Test that methylation flags are correctly defined."""
    assert MethFlags.methylated_motif_flag == 1
    assert MethFlags.unmethylated_motif_flag == 0
    assert MethFlags.missing_motif_flag == "!"
    print("✓ Methylation flags are correct")


def test_get_meth_pattern():
    """Test the _get_meth_pattern function."""
    # CpG positions in reference sequence (0-based)
    coordinates = [1, 5, 10]

    # Test 1: Read with methylated CpGs (containing "CG" at those positions)
    sequence = "ACGAACGTACGTAC"  # "CG" at positions 1, 5, 10
    pattern = _get_meth_pattern(coordinates, sequence, sam_position=0)
    print(f"Test pattern 1 (methylated): {pattern}")
    methylated_count = pattern.count(MethFlags.methylated_motif_flag)
    assert methylated_count > 0, f"Expected methylated CpGs, got pattern {pattern}"

    # Test 2: Read with unmethylated CpGs (containing "TG" at those positions)
    sequence = "ATGAATGTACGTAC"  # "TG" at positions 1, 5
    pattern = _get_meth_pattern(coordinates, sequence, sam_position=0)
    print(f"Test pattern 2 (unmethylated): {pattern}")
    unmethylated_count = pattern.count(MethFlags.unmethylated_motif_flag)
    assert unmethylated_count > 0, f"Expected unmethylated CpGs, got pattern {pattern}"

    print("✓ _get_meth_pattern works correctly")


def test_retain_methylated_with_real_data():
    """Test the retain_methylated feature with real data files."""
    # Use real data files from the project
    fasta_file = "/home/ubuntu/projects/EpiAlleles/data/Galaxy2-[SNCA_Promoter_Region1.fasta].fasta"
    sam_file = "/home/ubuntu/projects/EpiAlleles/data/Galaxy303-[sgRNA3_Region1_Rep1].sam"

    if not os.path.exists(fasta_file) or not os.path.exists(sam_file):
        print("⚠ Real data files not found, skipping real data test")
        return

    # Get coordinates from FASTA
    coordinates = get_coordinates(fasta_file)
    print(f"Found {len(coordinates)} CpG sites in reference")

    # Test WITHOUT --retain-methylated flag
    print("\n--- Test WITHOUT --retain-methylated flag ---")
    meth_data_all = MethylationData()
    extract_meth(coordinates, [sam_file], meth_data_all, retain_methylated=False)

    total_reads_all = sum(data.reads_number for data in meth_data_all.data)
    print(f"Total reads (all): {total_reads_all}")

    if total_reads_all > 0:
        # Count reads with at least one methylated CpG in the all reads
        reads_with_methylated = 0
        reads_unmethylated = 0

        for sample in meth_data_all.data:
            for pattern in sample.meth_patterns:
                if MethFlags.methylated_motif_flag in pattern:
                    reads_with_methylated += 1
                else:
                    reads_unmethylated += 1

        print(f"Reads with at least one methylated CpG: {reads_with_methylated}")
        print(f"Completely unmethylated reads: {reads_unmethylated}")

    # Test WITH --retain-methylated flag
    print("\n--- Test WITH --retain-methylated flag ---")
    meth_data_retained = MethylationData()
    extract_meth(coordinates, [sam_file], meth_data_retained, retain_methylated=True)

    total_reads_retained = sum(data.reads_number for data in meth_data_retained.data)
    print(f"Total reads (retained only methylated): {total_reads_retained}")

    # Verify all retained reads have at least one methylated CpG
    all_have_methylated = True
    for sample in meth_data_retained.data:
        for pattern in sample.meth_patterns:
            if MethFlags.methylated_motif_flag not in pattern:
                all_have_methylated = False
                print(f"ERROR: Found unmethylated read in retained data: {pattern}")

    if all_have_methylated:
        print("✓ All retained reads have at least one methylated CpG")
    else:
        print("✗ ERROR: Some retained reads are completely unmethylated!")
        return False

    # Verify that retained reads are fewer than total reads
    if total_reads_retained <= total_reads_all:
        print(f"✓ Retained reads ({total_reads_retained}) <= Total reads ({total_reads_all})")
    else:
        print(f"✗ ERROR: Retained reads ({total_reads_retained}) > Total reads ({total_reads_all})")
        return False

    return True


def test_parse_sam_line():
    """Test the _parse_sam_line function."""
    # Example SAM line (simplified)
    sam_line = "read1\t0\tref\t10\t60\t100M\t*\t0\t0\tACGTACGTACGT\tIIIIIIIIIIII\n"

    sequence, position = _parse_sam_line(sam_line)

    assert sequence == "ACGTACGTACGT", f"Expected sequence 'ACGTACGTACGT', got '{sequence}'"
    assert position == 9, f"Expected position 9 (0-based), got {position}"  # 10 in 1-based becomes 9 in 0-based

    print("✓ _parse_sam_line correctly parses SAM lines")


def main():
    print("=" * 60)
    print("Testing --retain-methylated flag implementation")
    print("=" * 60)

    try:
        test_methylation_flags()
        test_get_meth_pattern()
        test_parse_sam_line()

        result = test_retain_methylated_with_real_data()
        if result is False:
            print("\n✗ Real data test FAILED")
            return 1

        print("\n" + "=" * 60)
        print("✓ All tests PASSED!")
        print("=" * 60)
        return 0

    except Exception as e:
        print(f"\n✗ Test FAILED with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
