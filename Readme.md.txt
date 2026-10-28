# FAIR Plant Bioinformatics Project

## Project Overview

This project explores plant gene expression responses
to drought stress using publicly available gene
expression data.

It demonstrates basic bioinformatics analysis,
gene annotation, data organization, and FAIR
data management principles.

## Objectives

1. Explore a public plant gene expression dataset.
2. Process and organize gene expression data.
3. Annotate probes with available gene information.
4. Identify the top 10 upregulated and top 10
   downregulated probes based on log2 fold change.
5. Prepare reproducible analysis scripts.
6. Apply FAIR data management principles.

## Dataset

Source: NCBI Gene Expression Omnibus (GEO)

Accession: GSE5624

Control dataset: GSE5620
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE5620

Drought-stress dataset: GSE5624
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE5624

Microarray annotation platform: GPL198
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL198

Dataset URL:
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE5624

## Tools Used

- Python
- Pandas
- Microsoft Excel
- NCBI GEO
- GitHub

## Methodology

1. Obtained the publicly available GEO dataset.
2. Organized the project into raw and processed
   data directories.
3. Processed gene expression information.
4. Annotated probes with available gene information.
5. Ranked probes using log2 fold change.
6. Extracted the 10 highest positive and
   10 lowest negative fold-change values.
7. Generated a summary table containing gene
   annotations and expression changes.

## Results

The analysis produced a summary of 20 probes:

- 10 upregulated probes
- 10 downregulated probes

The summary includes:

- Probe ID
- ORF
- Gene Symbol
- Gene Title
- Log2 Fold Change
- Direction
- Fold Change

Output file:
data/processed/drought_gene_summary.csv

## Limitations

The selected probes were ranked using fold-change
values.

Statistical significance has not yet been established
through differential expression testing.

Therefore, these results should be interpreted as
exploratory rather than confirmed statistically
significant differential expression.

## FAIR Data Principles

Findable:
The source dataset has a persistent GEO accession.

Accessible:
The public dataset can be retrieved from NCBI GEO.

Interoperable:
Processed results are stored in CSV format.

Reusable:
Analysis scripts, documentation, and data provenance
are provided to support reproducibility.

## Future Improvements

- Perform statistical differential expression analysis.
- Investigate the biological functions of selected genes.
- Explore relevant drought-response pathways.
- Improve data visualization and interpretation.

## Project Status

Exploratory analysis completed.
Statistical validation remains future work.
