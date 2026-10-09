# DNA Sequence Analysis Extension

## Purpose

This is a beginner-friendly extension to the existing educational website. It accepts DNA sequences in FASTA format and reports simple sequence-composition statistics. The Python implementation uses only the Python standard library.

## What it reports

- Sequence identifier and length (bp)
- Counts of A, C, G, and T
- Count of ambiguous IUPAC DNA symbols (for example, N)
- GC percentage calculated from canonical A/C/G/T bases only
- Optional SVG bar chart comparing GC percentage across the input sequences

Ambiguous symbols are excluded from the denominator used for GC percentage. If a sequence contains only ambiguous symbols, GC percentage is reported as 0.00.

## Run the Python module

From the repository root:

```bash
python code/sequence_analysis.py data/example_sequences.fasta --output outputs/sequence_summary.csv --chart outputs/gc_comparison.svg
```

The optional `--chart` argument creates an SVG bar chart without requiring plotting libraries. The file `data/example_sequences.fasta` contains short illustrative sequences created for testing. They are not real organism records and should not be cited as biological reference data.

## Test the module

```bash
python -m unittest discover -s tests -v
```

## Data provenance checklist

For real biological sequences, record the database or publication, accession identifier, organism/strain as provided by the source, download date, licence/terms, and any filtering performed. Retain the original input and do not silently replace it with edited sequences.

## Limitations

This module does not identify a species, gene, mutation, function, or phenotype. GC percentage and base composition alone cannot establish antibiotic resistance or support clinical decisions. This is an educational quality-control and descriptive-analysis exercise, not a diagnostic tool.
