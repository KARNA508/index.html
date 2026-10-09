# Bacterial Genetics & Data Visualisation — Educational Mini-Project

## Overview
This repository contains an educational website and a small Python bioinformatics module. The DNA sequence component reads FASTA records and reports sequence length, A/C/G/T counts, ambiguous-base count, and GC percentage. The website also visualises GC% and nucleotide composition; the Python CLI can export a GC% SVG chart.

**Educational only:** the sequence-composition workflow does not identify genes or organisms and cannot establish drug resistance or any clinical conclusion. The existing measurement records have undocumented provenance and must remain labelled **source unverified** until a traceable source is documented.

## Live website
https://karna508.github.io/index.html/

## DNA sequence analysis (Python)
Requires Python 3.10+ and no third-party packages for the analysis module. Fetching reference records requires internet access.

### Fetch a documented reference dataset

The accession list in `data/reference_accessions.csv` points to two bacterial 16S rRNA records in NCBI. Run:

```bash
python code/fetch_reference_sequences.py
python code/sequence_analysis.py data/reference_16s_sequences.fasta --output outputs/reference_sequence_summary.csv --chart outputs/reference_gc_comparison.svg
```

The fetcher records the retrieval timestamp, source URL, sequence length, and SHA-256 digest in a manifest. Read [the provenance guide](DATASET_PROVENANCE_GUIDE.md) before using the data in a report.

```bash
python code/sequence_analysis.py data/example_sequences.fasta --output outputs/sequence_summary.csv --chart outputs/gc_comparison.svg
python -m unittest discover -s tests -v
```

The example FASTA contains short illustrative test sequences, not real biological records. For real sequences, retain the original input and document the database/publication, accession, organism label as provided by the source, download date, and usage terms.

## Repository guide
- `index.html` — website, including a browser-based FASTA composition explorer.
- `code/sequence_analysis.py` — command-line FASTA parser and CSV summary generator.
- `data/example_sequences.fasta` — clearly labelled illustrative test input.
- `tests/test_sequence_analysis.py` — automated unit tests.
- `PROJECT_SEQUENCE_ANALYSIS.md` — methods, run instructions, provenance checklist, and limitations.
- `DATASET_PROVENANCE_GUIDE.md` — accession sources and reproducible reference-data workflow.
- `data/reference_accessions.csv` — NCBI accession list; downloaded FASTA/manifest files are generated locally.
- `code/fetch_reference_sequences.py` — fetches the reference FASTA and creates a provenance manifest.
- `tests/test_fetch_reference_sequences.py` — tests for accession and FASTA validation.
- `DATASET_PROVENANCE_TEMPLATE.md` — template for recording dataset provenance (where present).

## Method
GC percentage = 100 × (G + C) / (A + C + G + T). Ambiguous IUPAC symbols are counted separately and excluded from the denominator. If a sequence contains no canonical A/C/G/T bases, GC percentage is reported as 0.00.

## Limitations
Sequence length, nucleotide composition, and GC percentage alone do not establish biological function, identify a gene, or predict a phenotype. This is a descriptive educational workflow, not a diagnostic tool or validated resistance-prediction model.
