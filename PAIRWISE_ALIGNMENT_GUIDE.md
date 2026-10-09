# Pairwise DNA alignment module

## What it does
The module implements **global pairwise alignment** with the Needleman–Wunsch dynamic-programming algorithm. It aligns two complete short DNA sequences, introducing gaps where the scoring system makes that favourable.

Default scoring:
- Exact symbol match: +1
- Mismatch: -1
- Gap: -1

The score is a simple teaching choice, not a biological calibration. The traceback uses a deterministic tie rule: diagonal first, then up, then left.

## Run it

Align two sequences directly:

```bash
python code/pairwise_alignment.py ACGT ACGGT
```

Read sequences from FASTA/text files:

```bash
python code/pairwise_alignment.py first.fasta second.fasta --from-files
```

Run the tests:

```bash
python -m unittest discover -s tests -v
```

## Understanding the output
- **Alignment score:** sum of match, mismatch, and gap scores along the chosen alignment.
- **Match line:** a vertical bar marks identical non-gap symbols in the same aligned column.
- **Identity percentage:** identical non-gap symbols divided by total alignment columns, including columns with gaps.

Different scoring schemes or tie-breaking rules can produce different valid alignments. IUPAC ambiguous symbols are accepted, but only identical symbols count as exact matches.

## Limitations
This implementation is intended for short teaching examples; the dynamic-programming matrices use quadratic memory and time. It does not perform local alignment, multiple sequence alignment, infer evolutionary relationships, identify unknown sequences, or establish gene function, drug resistance, or any clinical phenotype.
