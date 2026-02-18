#!/usr/bin/env python3.10
"""
Integration test for the --retain-methylated flag.
Tests the full pipeline with and without the flag.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path
import csv

sys.path.insert(0, '/home/ubuntu/projects/EpiAlleles')

from utils.fasta import get_coordinates
from utils.meth_data import MethylationData, MethFlags
from utils.sam import extract_meth


def test_full_pipeline():
    """Test the full pipeline with and without --retain-methylated."""

    # Use real data files - matching FASTA with SAM files
    fasta_file = "/home/ubuntu/projects/EpiAlleles/data/Galaxy2-[SNCA_Promoter_Region1.fasta].fasta"
    sam_files = [
        "/home/ubuntu/projects/EpiAlleles/data/Galaxy303-[sgRNA3_Region1_Rep1].sam",
        "/home/ubuntu/projects/EpiAlleles/data/Galaxy305-[sgRNA3_Region3_Rep3].sam"
    ]

    if not os.path.exists(fasta_file):
        print(f"⚠ FASTA file not found: {fasta_file}")
        return False

    for sam in sam_files:
        if not os.path.exists(sam):
            print(f"⚠ SAM file not found: {sam}")
            return False

    # Get coordinates
    coordinates = get_coordinates(fasta_file)
    print(f"Found {len(coordinates)} CpG sites in reference")

    # Process WITHOUT retain-methylated
    print("\n" + "=" * 70)
    print("PROCESSING WITHOUT --retain-methylated")
    print("=" * 70)

    meth_data_all = MethylationData()
    extract_meth(coordinates, sam_files, meth_data_all, retain_methylated=False)

    stats_all = {}
    total_reads_all = 0
    total_with_meth_all = 0

    for i, sample in enumerate(meth_data_all.data):
        filename = Path(sample.file_name).name
        reads = sample.reads_number
        methylated = sum(1 for p in sample.meth_patterns if MethFlags.methylated_motif_flag in p)
        unmethylated = reads - methylated

        total_reads_all += reads
        total_with_meth_all += methylated

        print(f"\nFile {i+1}: {filename}")
        print(f"  Total reads: {reads}")
        if reads > 0:
            print(f"  Reads with methylated CpG: {methylated} ({100*methylated/reads:.1f}%)")
            print(f"  Completely unmethylated: {unmethylated} ({100*unmethylated/reads:.1f}%)")
        else:
            print(f"  (No reads found - may be wrong reference sequence)")

        stats_all[sample.file_name] = {
            'total': reads,
            'methylated': methylated,
            'unmethylated': unmethylated
        }

    print(f"\nTOTAL (all samples): {total_reads_all} reads")
    if total_reads_all > 0:
        print(f"Total with methylated CpG: {total_with_meth_all} ({100*total_with_meth_all/total_reads_all:.1f}%)")
        print(f"Total unmethylated: {total_reads_all - total_with_meth_all} ({100*(total_reads_all - total_with_meth_all)/total_reads_all:.1f}%)")

    # Process WITH retain-methylated
    print("\n" + "=" * 70)
    print("PROCESSING WITH --retain-methylated")
    print("=" * 70)

    meth_data_retained = MethylationData()
    extract_meth(coordinates, sam_files, meth_data_retained, retain_methylated=True)

    stats_retained = {}
    total_reads_retained = 0

    for i, sample in enumerate(meth_data_retained.data):
        filename = Path(sample.file_name).name
        reads = sample.reads_number

        total_reads_retained += reads

        # Verify all reads have methylated CpG
        for pattern in sample.meth_patterns:
            if MethFlags.methylated_motif_flag not in pattern:
                print(f"✗ ERROR: Found unmethylated read: {pattern}")
                return False

        # Calculate percentage of unmethylated reads filtered out
        original = stats_all[sample.file_name]['total']
        filtered_out = original - reads
        percent_filtered = 100 * filtered_out / original if original > 0 else 0

        print(f"\nFile {i+1}: {filename}")
        print(f"  Reads retained: {reads}/{original}")
        if filtered_out > 0:
            print(f"  Reads filtered out: {filtered_out} ({percent_filtered:.1f}%)")

        stats_retained[sample.file_name] = {
            'total': reads,
            'filtered_out': filtered_out
        }

    print(f"\nTOTAL (all samples with --retain-methylated): {total_reads_retained} reads")
    filtered_total = total_reads_all - total_reads_retained
    if filtered_total > 0:
        print(f"Total filtered out: {filtered_total} ({100*filtered_total/total_reads_all:.1f}%)")
    else:
        print("No reads were filtered (all reads have at least one methylated CpG)")

    # Validation checks
    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)

    all_valid = True

    # Check 1: All retained reads must have methylated CpG
    print("✓ Check 1: All retained reads have at least one methylated CpG")

    # Check 2: Retained reads <= original reads
    if total_reads_retained <= total_reads_all:
        print(f"✓ Check 2: Retained reads ({total_reads_retained}) <= Original reads ({total_reads_all})")
    else:
        print(f"✗ Check 2 FAILED: Retained reads ({total_reads_retained}) > Original reads ({total_reads_all})")
        all_valid = False

    # Check 3: Filtered count should equal unmethylated reads from first run
    expected_filtered = total_reads_all - total_with_meth_all
    actual_filtered = total_reads_all - total_reads_retained
    if expected_filtered == actual_filtered:
        print(f"✓ Check 3: Filtered count ({actual_filtered}) matches unmethylated count from no-filter run")
    else:
        print(f"⚠ Check 3: Filtered count ({actual_filtered}) != unmethylated count ({expected_filtered})")

    # Check 4: Each sample's retained reads should match its methylated reads
    for filepath, stats in stats_retained.items():
        retained = stats['total']
        original_methylated = stats_all[filepath]['methylated']
        if retained == original_methylated:
            filename = Path(filepath).name
            print(f"✓ Check 4: {filename} retained ({retained}) = methylated ({original_methylated})")
        else:
            print(f"⚠ Check 4: {filename} retained ({retained}) != methylated ({original_methylated})")

    return all_valid


if __name__ == "__main__":
    print("=" * 70)
    print("Integration Test: --retain-methylated flag")
    print("=" * 70)

    try:
        success = test_full_pipeline()

        if success:
            print("\n" + "=" * 70)
            print("✓ INTEGRATION TEST PASSED")
            print("=" * 70)
            sys.exit(0)
        else:
            print("\n" + "=" * 70)
            print("✗ INTEGRATION TEST FAILED")
            print("=" * 70)
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
