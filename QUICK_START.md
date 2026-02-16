# Quick Start Guide: run_allelicMeth.py

## TL;DR

### Explicit Mode (Specific Files)
```bash
python run_allelicMeth.py --mode explicit --fasta file.fasta --sam file.sam
```

### Directory Mode (Batch Processing)
```bash
python run_allelicMeth.py --mode directory --dir /path/to/data/
```

## Installation

Already installed! Located in: `/home/ubuntu/projects/EpiAlleles/run_allelicMeth.py`

```bash
# Make it executable (if needed)
chmod +x run_allelicMeth.py

# View help
./run_allelicMeth.py -h
```

## Common Tasks

### 1. Run Single FASTA/SAM Pair
```bash
python run_allelicMeth.py --mode explicit \
  --fasta reference.fasta \
  --sam aligned_reads.sam
```

### 2. Run Multiple SAM Files Against One FASTA
```bash
python run_allelicMeth.py --mode explicit \
  --fasta reference.fasta \
  --sam rep1.sam rep2.sam rep3.sam
```

### 3. Batch Process Directory
```bash
python run_allelicMeth.py --mode directory \
  --dir ./data/
```

The script will:
- Find all FASTA files
- Extract region IDs (e.g., "Region1")
- Find matching SAM files
- Process all pairs automatically

### 4. Custom Histogram Mode
```bash
python run_allelicMeth.py --mode directory \
  --dir ./data/ \
  --allelicmeth-mode multiple
```

### 5. Custom Number of Reads to Plot
```bash
python run_allelicMeth.py --mode directory \
  --dir ./data/ \
  --reads2plot 5000
```

### 6. Custom Log File Location
```bash
python run_allelicMeth.py --mode directory \
  --dir ./data/ \
  --log /var/log/allelicmeth/batch.log
```

### 7. Debug Mode (Verbose Logging)
```bash
python run_allelicMeth.py --mode directory \
  --dir ./data/ \
  --debug
```

### 8. All Options Combined
```bash
python run_allelicMeth.py --mode directory \
  --dir ./data/ \
  --log ./results/batch.log \
  --allelicmeth-mode multiple \
  --reads2plot 10000 \
  --debug
```

## File Naming Requirements

### For Directory Mode
Filenames must follow specific patterns for auto-matching:

**FASTA Files**:
- Must contain region identifier in square brackets
- Example: `Galaxy2-[SNCA_Promoter_Region1.fasta].fasta`
- Extracted ID: `Region1`

**SAM Files**:
- Must contain the same region identifier as matching FASTA
- Example: `Galaxy303-[sgRNA3_Region1_Rep1].sam`
- Contains: `Region1` → Matches FASTA!

## Log Files

Log files are automatically created with timestamps:
```
allelicMeth_log_2026-02-16_14-29-03.log
```

### Checking Logs
```bash
# View latest log
cat allelicMeth_log_*.log | tail -50

# Search for errors
grep ERROR allelicMeth_log_*.log

# Check summary
tail -15 allelicMeth_log_*.log
```

## Output Example

### Explicit Mode
```
[2026-02-16 14:28:25] INFO: Starting allelicMeth orchestrator - EXPLICIT mode
[2026-02-16 14:28:25] INFO: Input FASTA: /path/to/file.fasta
[2026-02-16 14:28:25] INFO: Input SAM files: ['/path/to/file.sam']
[2026-02-16 14:28:47] INFO: Execution completed successfully
[2026-02-16 14:28:47] INFO: Log file: allelicMeth_log_2026-02-16_14-28-25.log
```

### Directory Mode
```
[2026-02-16 14:35:10] INFO: Starting allelicMeth orchestrator - BATCH mode
[2026-02-16 14:35:10] INFO: Scanning directory: /data/samples/
[2026-02-16 14:35:10] INFO: Found 2 FASTA file(s)
[2026-02-16 14:35:10] INFO: Created 4 file pair(s)
[2026-02-16 14:35:11] INFO: [1/4] Processing: file1.fasta + file1_rep1.sam
[2026-02-16 14:35:16] INFO: [1/4] SUCCESS
[2026-02-16 14:36:02] INFO: BATCH PROCESSING COMPLETE
[2026-02-16 14:36:02] INFO: Total: 4 | Success: 4 | Failures: 0
```

## Troubleshooting

### "FASTA file not found"
```bash
# Make sure file path is correct
ls /path/to/file.fasta

# Use absolute paths
python run_allelicMeth.py --mode explicit \
  --fasta /full/path/to/file.fasta \
  --sam /full/path/to/file.sam
```

### "No SAM files found for region"
```bash
# Check SAM filename contains the region ID from FASTA
# FASTA: Galaxy2-[Region1.fasta].fasta
# SAM must contain: Region1

ls /data/samples/*Region1*
```

### "No valid FASTA/SAM pairs found"
```bash
# Verify file naming patterns
# FASTA needs: [*Region*] pattern
# SAM needs: matching region identifier

ls /data/samples/
# Look for patterns like:
# - [SNCA_Region1.fasta]
# - [sgRNA3_Region1_Rep1]
```

### "allelicMeth.py not found"
```bash
# Make sure both scripts are in same directory
ls /home/ubuntu/projects/EpiAlleles/
# Should show: run_allelicMeth.py, allelicMeth.py, utils/
```

### Performance Issues
```bash
# Process fewer files at once
# For very large datasets, split into subdirectories

# Create subdirectory with specific region
mkdir /data/batch1
mv /data/samples/*Region1* /data/batch1/

# Process batch
python run_allelicMeth.py --mode directory --dir /data/batch1/
```

## Return Codes

```bash
# Success (all processed)
python run_allelicMeth.py --mode explicit --fasta f.fasta --sam f.sam
echo $?  # Returns: 0

# Failure (something went wrong)
python run_allelicMeth.py --mode explicit --fasta /nonexistent
echo $?  # Returns: 1
```

## Integration Examples

### Bash Loop (Sequential Batches)
```bash
#!/bin/bash
for batch in batch1 batch2 batch3; do
  python run_allelicMeth.py --mode directory --dir "/data/$batch"
done
```

### Cron Job (Scheduled)
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 2 AM
0 2 * * * cd /home/user/EpiAlleles && python run_allelicMeth.py --mode directory --dir /data/samples/ --log /var/log/allelicmeth.log
```

### Check Status Interactively
```bash
# Start processing
python run_allelicMeth.py --mode directory --dir /data &
PID=$!

# Monitor progress
tail -f allelicMeth_log_*.log

# Wait for completion
wait $PID
echo "Completed with status: $?"
```

## More Information

- Full documentation: `RUN_ALLELICMETH_README.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`
- Test examples: `test_orchestrator.sh`

---

**Questions?** Check the comprehensive README or review log files for detailed error information.
