#!/usr/bin/env python3.10

################################################################################
# Main orchestrator script for allelicMeth.py
# Supports two modes: explicit (direct files) and directory (batch processing)
# Comprehensive logging for both modes
################################################################################

import argparse
import logging
import os
import sys
import subprocess
import re
from datetime import datetime
from pathlib import Path


class AllelicMethOrchestrator:
    """Orchestrates execution of allelicMeth.py with intelligent file matching."""

    def __init__(self, log_file=None, log_level=logging.INFO):
        """
        Initialize the orchestrator with logging setup.

        Args:
            log_file: Path to log file (auto-generated if None)
            log_level: Logging level (default: INFO)
        """
        self.logger = self._setup_logging(log_file, log_level)
        self.script_dir = Path(__file__).parent
        self.allelicmeth_script = self.script_dir / "allelicMeth.py"

    def _setup_logging(self, log_file, log_level):
        """Setup logging to both console and file."""
        logger = logging.getLogger("AllelicMethOrchestrator")
        logger.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_format = logging.Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)

        # File handler
        if log_file is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = f"allelicMeth_log_{timestamp}.log"

        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        self.log_file = log_file
        return logger

    def _verify_allelicmeth_script(self):
        """Verify that allelicMeth.py exists."""
        if not self.allelicmeth_script.exists():
            self.logger.error(f"allelicMeth.py not found at {self.allelicmeth_script}")
            return False
        self.logger.debug(f"allelicMeth.py found at {self.allelicmeth_script}")
        return True

    def _run_allelicmeth(self, fasta_file, sam_files, mode=None, reads2plot=None, retain_methylated=False):
        """
        Execute allelicMeth.py with given parameters.

        Args:
            fasta_file: Path to FASTA file
            sam_files: List of SAM file paths
            mode: Optional mode (single/multiple)
            reads2plot: Optional number of reads to plot
            retain_methylated: Optional flag to retain only methylated reads

        Returns:
            Tuple (success: bool, stdout: str, stderr: str)
        """
        cmd = [
            "python3.10",
            str(self.allelicmeth_script),
            "--fasta", str(fasta_file),
            "--sam", *[str(f) for f in sam_files]
        ]

        if mode:
            cmd.extend(["--mode", mode])
        if reads2plot:
            cmd.extend(["--reads2plot", str(reads2plot)])
        if retain_methylated:
            cmd.append("--retain-methylated")

        self.logger.debug(f"Executing: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )

            if result.returncode == 0:
                self.logger.debug(f"Process stdout: {result.stdout}")
                return True, result.stdout, result.stderr
            else:
                self.logger.error(f"Process stderr: {result.stderr}")
                return False, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            self.logger.error("Process timed out after 1 hour")
            return False, "", "Process timed out"
        except Exception as e:
            self.logger.error(f"Error executing allelicMeth.py: {e}")
            return False, "", str(e)

    def run_explicit_mode(self, fasta_file, sam_files, mode=None, reads2plot=None, retain_methylated=False):
        """
        Run in explicit mode with provided files.

        Args:
            fasta_file: Path to FASTA file
            sam_files: List of SAM file paths
            mode: Optional mode (single/multiple)
            reads2plot: Optional number of reads to plot
            retain_methylated: Optional flag to retain only methylated reads

        Returns:
            bool: Success status
        """
        self.logger.info("=" * 80)
        self.logger.info("Starting allelicMeth orchestrator - EXPLICIT mode")
        self.logger.info("=" * 80)

        if not self._verify_allelicmeth_script():
            return False

        # Validate input files
        fasta_path = Path(fasta_file)
        if not fasta_path.exists():
            self.logger.error(f"FASTA file not found: {fasta_file}")
            return False
        self.logger.info(f"Input FASTA: {fasta_file}")

        sam_paths = [Path(f) for f in sam_files]
        for sam_file in sam_paths:
            if not sam_file.exists():
                self.logger.error(f"SAM file not found: {sam_file}")
                return False
        self.logger.info(f"Input SAM files: {sam_files}")

        # Run analysis
        success, stdout, stderr = self._run_allelicmeth(
            fasta_path, sam_paths, mode, reads2plot, retain_methylated
        )

        if success:
            self.logger.info("Execution completed successfully")
        else:
            self.logger.error("Execution failed")

        self.logger.info("=" * 80)
        self.logger.info(f"Log file: {self.log_file}")
        self.logger.info("=" * 80)

        return success

    def _extract_region_from_fasta(self, filename):
        """
        Extract region identifier from FASTA filename.

        Extracts the "RegionX" identifier from patterns like:
        - Galaxy2-[SNCA_Promoter_Region1.fasta].fasta → Region1
        - Galaxy2-[Region1].fasta → Region1

        Uses the last "RegionX" match found in the filename for flexibility.

        Args:
            filename: FASTA filename

        Returns:
            str: Region identifier (e.g., "Region1", "Region2") or None
        """
        # Find all matches of RegionX pattern (case-insensitive)
        matches = re.findall(r'(Region\d+)', filename, re.IGNORECASE)
        if matches:
            # Return the last match (most specific/closest to file extension)
            return matches[-1]
        return None

    def _find_matching_sam_files(self, directory, region_identifier):
        """
        Find SAM files matching a region identifier.

        Args:
            directory: Directory to search in
            region_identifier: Region identifier to match

        Returns:
            list: Paths to matching SAM files
        """
        matching_files = []
        for filename in os.listdir(directory):
            if filename.endswith(".sam") and region_identifier in filename:
                matching_files.append(Path(directory) / filename)
        return sorted(matching_files)

    def run_directory_mode(self, directory, mode=None, reads2plot=None, retain_methylated=False):
        """
        Run in directory mode - scan for matching FASTA/SAM pairs.

        Args:
            directory: Directory containing FASTA and SAM files
            mode: Optional mode (single/multiple)
            reads2plot: Optional number of reads to plot
            retain_methylated: Optional flag to retain only methylated reads

        Returns:
            bool: Success status (True if all pairs processed successfully)
        """
        self.logger.info("=" * 80)
        self.logger.info("Starting allelicMeth orchestrator - BATCH mode")
        self.logger.info("=" * 80)

        if not self._verify_allelicmeth_script():
            return False

        directory = Path(directory)
        if not directory.exists():
            self.logger.error(f"Directory not found: {directory}")
            return False
        self.logger.info(f"Scanning directory: {directory}")

        # Find FASTA files
        fasta_files = [
            f for f in directory.iterdir()
            if f.suffix in ['.fa', '.fasta']
        ]
        self.logger.info(f"Found {len(fasta_files)} FASTA file(s)")

        if not fasta_files:
            self.logger.warning("No FASTA files found in directory")
            return False

        for fasta_file in fasta_files:
            self.logger.debug(f"  - {fasta_file.name}")

        # Extract region identifiers and find matching SAM files
        file_pairs = []
        for fasta_file in fasta_files:
            region_id = self._extract_region_from_fasta(fasta_file.name)

            if not region_id:
                self.logger.warning(f"Could not extract region from: {fasta_file.name}")
                continue

            self.logger.debug(f"Extracted region '{region_id}' from {fasta_file.name}")

            # Find matching SAM files
            sam_files = self._find_matching_sam_files(directory, region_id)

            if not sam_files:
                self.logger.warning(f"No SAM files found for region '{region_id}'")
                continue

            self.logger.info(f"Found {len(sam_files)} SAM file(s) for region '{region_id}'")
            for sam_file in sam_files:
                self.logger.debug(f"  - {sam_file.name}")
                file_pairs.append((fasta_file, [sam_file]))

        if not file_pairs:
            self.logger.error("No valid FASTA/SAM file pairs found")
            return False

        self.logger.info(f"Created {len(file_pairs)} file pair(s)")
        self.logger.info("=" * 80)
        self.logger.info(f"Processing {len(file_pairs)} pair(s)...")
        self.logger.info("=" * 80)

        # Process each pair
        success_count = 0
        failure_count = 0
        failed_pairs = []

        for idx, (fasta_file, sam_files) in enumerate(file_pairs, 1):
            self.logger.info(f"[{idx}/{len(file_pairs)}] Processing: {fasta_file.name} + {[f.name for f in sam_files]}")

            try:
                success, stdout, stderr = self._run_allelicmeth(
                    fasta_file, sam_files, mode, reads2plot, retain_methylated
                )

                if success:
                    self.logger.info(f"[{idx}/{len(file_pairs)}] SUCCESS")
                    success_count += 1
                else:
                    self.logger.error(f"[{idx}/{len(file_pairs)}] FAILED")
                    if stderr:
                        self.logger.error(f"Error details: {stderr}")
                    failure_count += 1
                    failed_pairs.append((fasta_file.name, [f.name for f in sam_files]))
            except Exception as e:
                self.logger.error(f"[{idx}/{len(file_pairs)}] FAILED with exception: {e}", exc_info=True)
                failure_count += 1
                failed_pairs.append((fasta_file.name, [f.name for f in sam_files]))

            self.logger.info("-" * 80)

        # Summary report
        self.logger.info("=" * 80)
        self.logger.info("BATCH PROCESSING COMPLETE")
        self.logger.info("=" * 80)
        self.logger.info(f"Total pairs: {len(file_pairs)}")
        self.logger.info(f"Successful: {success_count}")
        self.logger.info(f"Failed: {failure_count}")

        if failed_pairs:
            self.logger.warning("Failed pairs:")
            for fasta_name, sam_names in failed_pairs:
                self.logger.warning(f"  - {fasta_name} + {sam_names}")

        self.logger.info("=" * 80)
        self.logger.info(f"Log file: {self.log_file}")
        self.logger.info("=" * 80)

        return failure_count == 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Orchestrator for allelicMeth.py - Batch process methylation analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Explicit mode - provide specific files
  python run_allelicMeth.py --mode explicit --fasta file.fasta --sam file1.sam file2.sam

  # Directory mode - scan directory for matching pairs
  python run_allelicMeth.py --mode directory --dir ./data/

  # Directory mode with custom log file
  python run_allelicMeth.py --mode directory --dir ./data/ --log ./logs/batch.log
        """
    )

    parser.add_argument(
        "--mode",
        choices=["explicit", "directory"],
        required=True,
        help="Operation mode: explicit (provide files) or directory (batch scan)"
    )

    parser.add_argument(
        "--fasta",
        type=str,
        help="FASTA file (required for explicit mode)"
    )

    parser.add_argument(
        "--sam",
        nargs="+",
        help="SAM file(s) (required for explicit mode)"
    )

    parser.add_argument(
        "--dir",
        type=str,
        help="Directory to scan for FASTA/SAM pairs (required for directory mode)"
    )

    parser.add_argument(
        "--log",
        type=str,
        help="Log file path (auto-generated if not provided)"
    )

    parser.add_argument(
        "--allelicmeth-mode",
        choices=["single", "multiple"],
        help="Histogram mode for allelicMeth.py (default: single)"
    )

    parser.add_argument(
        "--reads2plot",
        type=int,
        help="Number of reads to visualize on heatmap (default: 10000)"
    )

    parser.add_argument(
        "--retain-methylated",
        action="store_true",
        help="Retain only reads with at least one methylated CpG site"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    # Determine log level
    log_level = logging.DEBUG if args.debug else logging.INFO

    # Create orchestrator
    orchestrator = AllelicMethOrchestrator(
        log_file=args.log,
        log_level=log_level
    )

    try:
        if args.mode == "explicit":
            # Explicit mode validation
            if not args.fasta or not args.sam:
                orchestrator.logger.error("Explicit mode requires --fasta and --sam arguments")
                return 1

            success = orchestrator.run_explicit_mode(
                args.fasta,
                args.sam,
                mode=args.allelicmeth_mode,
                reads2plot=args.reads2plot,
                retain_methylated=args.retain_methylated
            )

        else:  # directory mode
            # Directory mode validation
            if not args.dir:
                orchestrator.logger.error("Directory mode requires --dir argument")
                return 1

            success = orchestrator.run_directory_mode(
                args.dir,
                mode=args.allelicmeth_mode,
                reads2plot=args.reads2plot,
                retain_methylated=args.retain_methylated
            )

        return 0 if success else 1

    except Exception as e:
        orchestrator.logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
