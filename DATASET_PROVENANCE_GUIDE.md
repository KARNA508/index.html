# Reference sequence dataset and provenance

## Purpose
The repository now includes a small reproducible workflow for fetching public bacterial 16S ribosomal RNA reference records from NCBI by accession. These records are intended for learning how to manage and compare sequence-composition summaries.

## Records in the accession list
- **J01859.1** — *Escherichia coli* 16S ribosomal RNA, complete sequence: https://www.ncbi.nlm.nih.gov/nuccore/J01859.1
- **NR_102783.2** — *Bacillus subtilis* subsp. *subtilis* strain 168 16S ribosomal RNA, complete sequence: https://www.ncbi.nlm.nih.gov/nuccore/NR_102783.2

Check the current NCBI record pages before using these records in formal work. The accession list is the source-of-record index; the fetched FASTA and manifest are generated outputs.

## Fetch and record provenance
From the repository root, with Python 3.10+ and internet access:

```bash
python code/fetch_reference_sequences.py
```

This fetches the accessions in `data/reference_accessions.csv` and creates:
- `data/reference_16s_sequences.fasta` — downloaded FASTA records with accession labels
- `data/reference_sequence_manifest.csv` — retrieval timestamp (UTC), accession, record title, sequence length, source URL, and SHA-256 digest

The SHA-256 digest helps identify whether a downloaded sequence string has changed between runs. Retrieval timestamps and hashes do not independently validate the biological accuracy of a record; the NCBI accession remains the traceable source.

The script makes requests to NCBI EFetch and pauses briefly between records. Run it again when you intentionally want to refresh the data; review any differences rather than silently replacing previously used results.

## Analyse the downloaded sequences
After the fetch completes:

```bash
python code/sequence_analysis.py data/reference_16s_sequences.fasta --output outputs/reference_sequence_summary.csv --chart outputs/reference_gc_comparison.svg
```

## Scientific scope and limitations
This small reference set is suitable for practising data provenance, FASTA parsing, sequence length, nucleotide composition, and GC-percentage comparisons. Two reference sequences are not enough for broad claims about a species or bacterial diversity. 16S rRNA composition alone does not identify an unknown organism conclusively and does not establish antibiotic resistance or other phenotypes.
