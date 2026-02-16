# run_allelicMeth.py - Orchestrator for allelicMeth.py

A comprehensive orchestrator script that wraps `allelicMeth.py` with two operation modes: **explicit input** and **batch directory processing** with intelligent file matching.

## Features

- **Explicit Mode**: Run analysis on specific FASTA and SAM files
- **Directory Mode**: Automatically scan a directory, extract region identifiers from FASTA filenames, find matching SAM files, and process them in batches
- **Comprehensive Logging**: Detailed logging to both console and timestamped log files for both modes
- **Error Handling**: Robust error handling and reporting of failures
- **Progress Tracking**: Real-time progress indicators during batch processing

## Installation

The script is self-contained and requires Python 3.10+. Ensure `allelicMeth.py` and its dependencies are in the same directory.

## Usage

### Explicit Mode

Run analysis on specific FASTA and SAM files:

```bash
python run_allelicMeth.py --mode explicit \
  --fasta /path/to/reference.fasta \
  --sam /path/to/file1.sam /path/to/file2.sam
```

### Directory Mode

Scan a directory for matching FASTA/SAM file pairs:

```bash
python run_allelicMeth.py --mode directory --dir /path/to/data/
```

## Command Line Arguments

### Required Arguments

| Argument | Mode | Description |
|----------|------|-------------|
| `--mode` | both | Operation mode: `explicit` or `directory` |

### Mode-Specific Arguments

#### Explicit Mode
| Argument | Required | Description |
|----------|----------|-------------|
| `--fasta` | Yes | Path to FASTA reference file |
| `--sam` | Yes | Paths to one or more SAM files (space-separated) |

#### Directory Mode
| Argument | Required | Description |
|----------|----------|-------------|
| `--dir` | Yes | Directory containing FASTA and SAM files |

### Optional Arguments

| Argument | Description |
|----------|-------------|
| `--log` | Custom log file path (auto-generated if not provided) |
| `--allelicmeth-mode` | Histogram mode: `single` or `multiple` (default: single) |
| `--reads2plot` | Number of reads to visualize on heatmap (default: 10000) |
| `--debug` | Enable debug-level logging |

## Examples

### Example 1: Explicit Mode with Single SAM File

```bash
python run_allelicMeth.py --mode explicit \
  --fasta /data/SNCA_Promoter_Region1.fasta \
  --sam /data/sgRNA3_Region1_Rep1.sam
```

**Output:**
```
[2026-02-16 14:32:45] INFO: Starting allelicMeth orchestrator - EXPLICIT mode
[2026-02-16 14:32:45] INFO: Input FASTA: /data/SNCA_Promoter_Region1.fasta
[2026-02-16 14:32:45] INFO: Input SAM files: ['/data/sgRNA3_Region1_Rep1.sam']
[2026-02-16 14:32:47] INFO: Execution completed successfully
[2026-02-16 14:32:47] INFO: Log file: allelicMeth_log_2026-02-16_14-32-45.log
```

### Example 2: Explicit Mode with Multiple SAM Files

```bash
python run_allelicMeth.py --mode explicit \
  --fasta /data/Galaxy2-[SNCA_Promoter_Region1.fasta].fasta \
  --sam /data/Galaxy303-[sgRNA3_Region1_Rep1].sam \
       /data/Galaxy304-[sgRNA3_Region1_Rep2].sam \
       /data/Galaxy305-[sgRNA3_Region1_Rep3].sam \
  --allelicmeth-mode single \
  --reads2plot 5000
```

### Example 3: Directory Mode - Batch Processing

```bash
python run_allelicMeth.py --mode directory --dir /data/samples/
```

**Directory Structure:**
```
/data/samples/
├── Galaxy2-[SNCA_Promoter_Region1.fasta].fasta
├── Galaxy3-[SNCA_Promoter_Region2.fasta].fasta
├── Galaxy303-[sgRNA3_Region1_Rep1].sam
├── Galaxy304-[sgRNA3_Region1_Rep2].sam
├── Galaxy305-[sgRNA3_Region2_Rep1].sam
└── Galaxy306-[sgRNA3_Region2_Rep2].sam
```

**Output:**
```
[2026-02-16 14:35:10] INFO: Starting allelicMeth orchestrator - BATCH mode
[2026-02-16 14:35:10] INFO: Scanning directory: /data/samples/
[2026-02-16 14:35:10] INFO: Found 2 FASTA file(s)
[2026-02-16 14:35:10] INFO: Extracted region 'SNCA_Promoter_Region1' from Galaxy2-[SNCA_Promoter_Region1.fasta].fasta
[2026-02-16 14:35:10] INFO: Found 2 SAM file(s) for region 'SNCA_Promoter_Region1'
[2026-02-16 14:35:10] INFO: Extracted region 'SNCA_Promoter_Region2' from Galaxy3-[SNCA_Promoter_Region2.fasta].fasta
[2026-02-16 14:35:10] INFO: Found 2 SAM file(s) for region 'SNCA_Promoter_Region2'
[2026-02-16 14:35:10] INFO: Created 4 file pair(s)
[2026-02-16 14:35:11] INFO: [1/4] Processing: Galaxy2-[SNCA_Promoter_Region1.fasta].fasta + ['Galaxy303-[sgRNA3_Region1_Rep1].sam']
[2026-02-16 14:35:16] INFO: [1/4] SUCCESS
[2026-02-16 14:35:16] INFO: [2/4] Processing: Galaxy2-[SNCA_Promoter_Region1.fasta].fasta + ['Galaxy304-[sgRNA3_Region1_Rep2].sam']
[2026-02-16 14:35:21] INFO: [2/4] SUCCESS
...
[2026-02-16 14:36:02] INFO: BATCH PROCESSING COMPLETE
[2026-02-16 14:36:02] INFO: Total pairs: 4 | Successful: 4 | Failed: 0
[2026-02-16 14:36:02] INFO: Log file: allelicMeth_log_2026-02-16_14-35-10.log
```

### Example 4: Directory Mode with Custom Log File

```bash
python run_allelicMeth.py --mode directory \
  --dir /data/samples/ \
  --log /logs/batch_processing_2026-02-16.log \
  --allelicmeth-mode multiple \
  --debug
```

## File Matching Logic

### Directory Mode Pairing

The script uses the following logic to match FASTA and SAM files:

1. **Extract Region ID from FASTA**: Searches for pattern `[*Region*]` in FASTA filename
   - Example: `Galaxy2-[SNCA_Promoter_Region1.fasta].fasta` → `SNCA_Promoter_Region1`

2. **Find Matching SAM Files**: Searches for SAM files containing the extracted region ID
   - Example: `Galaxy303-[sgRNA3_SNCA_Promoter_Region1_Rep1].sam` matches region `SNCA_Promoter_Region1`

3. **Create Pairs**: Each matching SAM file is paired with the FASTA file

### Requirements

- FASTA filenames must contain the region identifier in square brackets: `[*Region*]`
- SAM filenames must contain the same region identifier as the FASTA file
- Both file types must be in the same directory

## Log Files

### Log File Naming

- **Explicit mode**: `allelicMeth_log_YYYY-MM-DD_HH-MM-SS.log`
- **Directory mode**: `allelicMeth_log_YYYY-MM-DD_HH-MM-SS.log`

Log files are created in the current working directory by default, or in the location specified by `--log`.

### Log File Contents

Each log file contains:

- **Timestamp**: When each operation occurred
- **Log Level**: INFO, DEBUG, WARNING, ERROR
- **Message**: Descriptive status messages
- **File Paths**: Complete paths to processed files
- **Error Details**: Detailed error messages if operations fail
- **Summary Report**: Final statistics and status

### Example Log Entry

```
[2026-02-16 14:35:10] INFO: Starting allelicMeth orchestrator - BATCH mode
[2026-02-16 14:35:10] INFO: Scanning directory: /data/samples/
[2026-02-16 14:35:10] INFO: Found 2 FASTA file(s)
[2026-02-16 14:35:10] DEBUG:   - Galaxy2-[SNCA_Promoter_Region1.fasta].fasta
[2026-02-16 14:35:10] DEBUG:   - Galaxy3-[SNCA_Promoter_Region2.fasta].fasta
[2026-02-16 14:35:10] DEBUG: Extracted region 'SNCA_Promoter_Region1' from Galaxy2-[SNCA_Promoter_Region1.fasta].fasta
[2026-02-16 14:35:11] INFO: [1/4] Processing: Galaxy2-[SNCA_Promoter_Region1.fasta].fasta + ['Galaxy303-[sgRNA3_Region1_Rep1].sam']
[2026-02-16 14:35:16] INFO: [1/4] SUCCESS
```

## Error Handling

The script provides comprehensive error handling:

- **Missing Files**: Reports and skips missing FASTA/SAM files
- **Missing allelicMeth.py**: Stops execution with clear error message
- **Execution Failures**: Logs full error details and continues with next pair (batch mode)
- **Timeout**: Handles subprocess timeouts (1-hour limit per analysis)
- **Empty Directories**: Reports when no matching pairs are found

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (all operations completed successfully) |
| 1 | Failure (one or more operations failed) |

## Advanced Usage

### Running with Debug Output

Enable verbose logging to troubleshoot issues:

```bash
python run_allelicMeth.py --mode directory \
  --dir /data/samples/ \
  --debug
```

### Processing Multiple Regions

The script automatically handles multiple regions in a directory:

```bash
# Directory contains:
# Region1.fasta + Region1_Rep1.sam, Region1_Rep2.sam, Region1_Rep3.sam
# Region2.fasta + Region2_Rep1.sam, Region2_Rep2.sam
# Region3.fasta (no matching SAM files - will be skipped with warning)

python run_allelicMeth.py --mode directory --dir /data/samples/

# Result: 5 pairs processed (3 Region1 + 2 Region2)
```

### Custom Output Location

Specify a custom log directory:

```bash
python run_allelicMeth.py --mode directory \
  --dir /data/samples/ \
  --log /var/log/allelicmeth/batch.log
```

## Troubleshooting

### No matches found in directory mode

**Issue**: Log shows "No SAM files found for region 'X'"

**Solution**: Ensure SAM filenames contain the same region identifier as the FASTA filename

**Example**:
- FASTA: `Galaxy2-[SNCA_Region1.fasta].fasta` → Extracts `SNCA_Region1`
- SAM must contain: `SNCA_Region1` (case-sensitive)

### allelicMeth.py not found

**Issue**: Error "allelicMeth.py not found"

**Solution**: Ensure `run_allelicMeth.py` and `allelicMeth.py` are in the same directory

### Process timeout

**Issue**: Analysis takes longer than 1 hour

**Solution**: The script has a 1-hour timeout per pair. For very large datasets, consider processing fewer samples at once

### Permission denied

**Issue**: Cannot write log files

**Solution**: Ensure write permissions in the log file directory or use a different location with `--log`

## Performance Notes

- **Batch mode**: Process time depends on file sizes and number of SAM files
- **Parallel Processing**: Currently processes one pair at a time; can be extended for parallel processing
- **Memory**: Each analysis loads FASTA and SAM files into memory; consider file sizes

## Integration with Existing Workflows

### Shell Scripts

```bash
#!/bin/bash
# Process multiple data directories sequentially

for dir in /data/batch1 /data/batch2 /data/batch3; do
    python run_allelicMeth.py --mode directory --dir "$dir"
    echo "Completed processing $dir"
done
```

### Cron Jobs

```bash
# Daily batch processing at 2 AM
0 2 * * * cd /home/user/EpiAlleles && python run_allelicMeth.py --mode directory --dir /data/samples/ --log /var/log/allelicmeth/daily.log
```

## Support

For issues or feature requests related to this orchestrator, refer to the main project documentation.

For issues with `allelicMeth.py` itself, see its documentation.
