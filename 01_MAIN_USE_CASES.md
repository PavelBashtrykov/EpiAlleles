# Main Use Cases

## Single File Analysis

Analyze one FASTA reference with one SAM file containing bisulfite sequencing reads.

```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam sample.sam
```

## Multiple SAM Files Against One Reference

Analyze multiple SAM replicates against a single FASTA reference sequence.

```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam rep1.sam rep2.sam rep3.sam
```

## Batch Processing by Directory

Automatically discover and process FASTA/SAM file pairs from a directory.

```bash
python3.10 run_allelicMeth.py --mode directory --dir ./data/
```

## Single Mode Histogram

Generate individual histogram for each SAM file.

```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam sample.sam
```

## Multiple Mode Histogram

Combine multiple datasets on a single histogram.

```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam rep1.sam rep2.sam --mode multiple
```

## Methylation Heatmap Generation

Visualize methylation patterns across selected reads.

```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam sample.sam --reads2plot 500
```

## CSV Methylation Data Export

Extract and save methylation levels of individual reads to CSV.

```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam sample.sam
```

## CpG Site Analysis

Identify and analyze CpG site positions from FASTA reference.

```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam sample.sam
```

## Batch Processing with Logging

Process large datasets with timestamped logs and progress tracking.

```bash
python3.10 run_allelicMeth.py --mode directory --dir ./data/ --log ./logs/batch.log
```

## Bisulfite Amplicon Sequencing (BSAS) Analysis

Analyze single-end or merged pair-end BSAS reads.

```bash
python3.10 allelicMeth.py --fasta reference.fasta --sam sample.sam --reads2plot 10000
```
