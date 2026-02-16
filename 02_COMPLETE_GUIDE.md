# Complete Usage Guide

## Overview

allelicMeth is a script for analysis and visualization of methylation levels of individual DNA molecules. Input: FASTA file containing reference sequence and SAM file(s) with bisulfite sequencing reads aligned to reference. Processes bisulfite amplicon sequencing (BSAS) with single-end or pair-end sequencing (merged reads in one DNA molecule corresponding to an amplicon).

## Outputs

For every SAM file:
- CSV file with methylation level of individual reads
- Histogram showing distribution of methylation levels
- Heatmap showing methylation pattern of selected reads

## Core Script: allelicMeth.py

### Basic Usage

```bash
python3.10 allelicMeth.py [options]
```

Can be executed without arguments from working directory containing FASTA and SAM files.

### Arguments

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--fasta` | string | No | FASTA file for CpG site extraction. If not provided, searches CWD for `.fa` or `.fasta` file. |
| `--sam` | string(s) | No | SAM file(s) with bisulfite reads. Multiple files accepted. If not provided, analyzes all `.sam` files in CWD. |
| `--mode` | string | No | `single` or `multiple`. Single (default): one histogram per SAM file. Multiple: all datasets on one histogram. |
| `--reads2plot` | integer | No | Number of reads to visualize on heatmap. Default: 10000. If greater than total reads, uses last available. |
| `--help` | flag | No | Display help message. |

### Examples

#### Auto-detect files in current directory
```bash
python3.10 allelicMeth.py
```

#### Specify FASTA and single SAM file
```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam sample.sam
```

#### Specify FASTA and multiple SAM files (single mode)
```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam rep1.sam rep2.sam rep3.sam
```

#### Multiple mode (combine datasets on one histogram)
```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam rep1.sam rep2.sam --mode multiple
```

#### Limit reads plotted on heatmap
```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam sample.sam --reads2plot 500
```

#### Combined options
```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam rep1.sam rep2.sam rep3.sam --mode multiple --reads2plot 1000
```

## Orchestrator Script: run_allelicMeth.py

Wrapper for batch processing with two operation modes.

### Basic Usage

```bash
python3.10 run_allelicMeth.py --mode {explicit,directory} [options]
```

### Arguments

| Flag | Type | Required | Mode(s) | Description |
|------|------|----------|---------|-------------|
| `--mode` | string | Yes | Both | `explicit` or `directory` |
| `--fasta` | string | Yes | explicit | FASTA reference file path |
| `--sam` | string(s) | Yes | explicit | One or more SAM file paths |
| `--dir` | string | Yes | directory | Directory path to scan for files |
| `--log` | string | No | Both | Custom log file path. Default: auto-generated timestamp. |
| `--allelicmeth-mode` | string | No | Both | Pass through to allelicMeth.py: `single` or `multiple` |
| `--reads2plot` | integer | No | Both | Pass through to allelicMeth.py: reads to visualize |
| `--debug` | flag | No | Both | Enable debug-level logging (verbose output) |
| `--help` | flag | No | Both | Display help message |

### Explicit Mode

Run analysis on specific FASTA and SAM files.

#### Single SAM file
```bash
python3.10 run_allelicMeth.py --mode explicit --fasta reference.fasta --sam sample.sam
```

#### Multiple SAM files
```bash
python3.10 run_allelicMeth.py --mode explicit --fasta reference.fasta --sam rep1.sam rep2.sam rep3.sam
```

#### With custom log file
```bash
python3.10 run_allelicMeth.py --mode explicit \
  --fasta reference.fasta \
  --sam sample.sam \
  --log ./logs/analysis.log
```

#### With allelicMeth options
```bash
python3.10 run_allelicMeth.py --mode explicit \
  --fasta reference.fasta \
  --sam rep1.sam rep2.sam \
  --allelicmeth-mode multiple \
  --reads2plot 2000
```

#### Debug mode
```bash
python3.10 run_allelicMeth.py --mode explicit \
  --fasta reference.fasta \
  --sam sample.sam \
  --debug
```

### Directory Mode

Batch process directory with automatic file discovery and region-based matching.

#### Basic batch processing
```bash
python3.10 run_allelicMeth.py --mode directory --dir ./data/
```

#### With custom log location
```bash
python3.10 run_allelicMeth.py --mode directory --dir ./data/ --log ./logs/batch.log
```

#### With allelicMeth options
```bash
python3.10 run_allelicMeth.py --mode directory \
  --dir ./data/ \
  --allelicmeth-mode multiple \
  --reads2plot 1000
```

#### Debug mode for directory processing
```bash
python3.10 run_allelicMeth.py --mode directory --dir ./data/ --debug
```

## File Naming Convention (Directory Mode)

For automatic pairing in directory mode:

**FASTA files** must contain region identifier in square brackets:
```
Galaxy2-[SNCA_Promoter_Region1.fasta].fasta
Galaxy2-[SNCA_Region2.fasta].fasta
```

**SAM files** must contain the same region identifier:
```
Galaxy303-[sgRNA3_Region1_Rep1].sam
Galaxy304-[sgRNA3_Region1_Rep2].sam
Galaxy305-[sgRNA3_Region2_Rep1].sam
```

Script extracts region ID (e.g., `Region1`) and matches FASTA/SAM pairs automatically.

## Logging

Both scripts generate timestamped log files with:
- All operations logged
- DEBUG, INFO, WARNING, ERROR levels
- Console output (real-time)
- File output (persistent)

Default log file: `allelicMeth_log_YYYY-MM-DD_HH-MM-SS.log`

### Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Detailed execution trace (enable with `--debug`) |
| INFO | Standard operation messages |
| WARNING | Non-fatal issues |
| ERROR | Fatal errors with explanation |

## Exit Codes

| Code | Status |
|------|--------|
| 0 | Success |
| 1 | Failure (file not found, invalid arguments, execution error) |

## Processing Order

### allelicMeth.py
1. Locate FASTA file
2. Locate SAM file(s)
3. Extract CpG site coordinates from FASTA
4. Parse methylation from SAM reads
5. Generate CSV output
6. Generate histogram (single or multiple mode)
7. Generate heatmap

### run_allelicMeth.py (directory mode)
1. Scan directory for FASTA files
2. Extract region identifiers from filenames
3. Find matching SAM files for each region
4. Create FASTA/SAM pairs
5. Process each pair sequentially
6. Generate summary report with statistics

## Performance

- **Startup**: < 100ms
- **Per-pair processing**: Depends on allelicMeth.py execution
- **Memory**: Minimal overhead
- **Scalability**: Linear with file pairs
- **Parallel processing**: Sequential in current implementation

## Integration Examples

### Bash loop for multiple directories
```bash
for dir in /data/batch1 /data/batch2 /data/batch3; do
  python3.10 run_allelicMeth.py --mode directory --dir "$dir"
done
```

### Cron job for automated batch processing
```bash
0 2 * * * cd /home/user/EpiAlleles && python3.10 run_allelicMeth.py --mode directory --dir /data/
```

### Sequential explicit analysis
```bash
python3.10 run_allelicMeth.py --mode explicit --fasta ref.fasta --sam rep1.sam
python3.10 run_allelicMeth.py --mode explicit --fasta ref.fasta --sam rep2.sam
python3.10 run_allelicMeth.py --mode explicit --fasta ref.fasta --sam rep3.sam
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "File not found" | Use absolute paths: `/full/path/to/file` instead of relative paths |
| "No SAM files found" (directory mode) | Verify SAM filename contains region ID from FASTA filename |
| "No pairs found" (directory mode) | Check FASTA naming includes `[*Region*]` pattern |
| "allelicMeth.py not found" | Ensure both scripts in same directory |
| "Python 3.10 not found" | Check installation: `python3.10 --version` |
| "Module not found" | Reinstall requirements: `pip install -r requirements.txt` |

## File Formats

### FASTA Input

Standard FASTA format with sequence header and nucleotide sequence:
```
>sequence_name
ACGTACGTACGT...
```

### SAM Input

SAM format with bisulfite-converted reads aligned to reference. Must contain:
- QNAME (read name)
- FLAG (alignment flag)
- RNAME (reference name)
- POS (alignment position)
- MAPQ (mapping quality)
- CIGAR (alignment cigar)
- RNEXT (mate reference)
- PNEXT (mate position)
- TLEN (template length)
- SEQ (sequence)
- QUAL (quality scores)
- Optional fields (methylation status)

### CSV Output

Generated CSV contains:
- Read identifier
- Methylation status per CpG site (M/U notation)
- Overall methylation percentage
- Additional read statistics

## Output Files

Default output location: Same directory as input files

| File Type | Pattern | Description |
|-----------|---------|-------------|
| CSV | `{sam_basename}_methylation.csv` | Individual read methylation data |
| Histogram (single) | `{sam_basename}_histogram.png` | Single dataset distribution |
| Histogram (multiple) | `histogram_combined.png` | Multiple datasets overlay |
| Heatmap | `{sam_basename}_heatmap.png` | Methylation pattern across reads |
