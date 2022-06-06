# EpiAlleles  
Contains scripts to analyse methylation of individual sequenced reads.

## TYPICAL USAGE:  
`epialleles [options]`  

## OPTIONS  
* `--reads2plot <INT>`  
Number of reads to be plotted on heatmaps. If more then total reads number in a input file(s), then the last one will be used.

* `--fasta <fasta_file>`
Fasta file used for generation of SAM files. Will be used to extract postitions of CpG sites. If not provided, scrip will read the `CWD` to find .fa or .fasta file.  
 