#!/usr/bin/env python3
"""Global pairwise DNA alignment using the Needleman-Wunsch algorithm.

Uses a simple scoring scheme: match +1, mismatch -1, gap -1. This is an
educational implementation for short sequences, not a clinical or diagnostic
tool. An alignment alone does not establish gene function or phenotype.
"""
from __future__ import annotations

import argparse
from pathlib import Path

VALID_IUPAC_DNA = set("ACGTRYSWKMBDHVN")


def clean_sequence(sequence: str, label: str = "sequence") -> str:
    """Remove whitespace and FASTA header lines, uppercase, and validate DNA."""
    lines = [line.strip() for line in sequence.splitlines() if line.strip()]
    if lines and lines[0].startswith(">"):
        lines = [line for line in lines if not line.startswith(">")]
    cleaned = "".join("".join(lines).split()).upper()
    if not cleaned:
        raise ValueError(f"{label} is empty.")
    invalid = sorted(set(cleaned) - VALID_IUPAC_DNA)
    if invalid:
        raise ValueError(f"{label} contains invalid DNA symbols: " + ", ".join(invalid))
    return cleaned


def align_sequences(
    sequence_a: str,
    sequence_b: str,
    match_score: int = 1,
    mismatch_score: int = -1,
    gap_score: int = -1,
) -> dict[str, str | int | float]:
    """Return a global alignment and simple summary using Needleman-Wunsch."""
    a = clean_sequence(sequence_a, "Sequence A")
    b = clean_sequence(sequence_b, "Sequence B")
    rows, cols = len(a) + 1, len(b) + 1
    score = [[0] * cols for _ in range(rows)]
    trace = [[""] * cols for _ in range(rows)]

    for i in range(1, rows):
        score[i][0] = i * gap_score
        trace[i][0] = "up"
    for j in range(1, cols):
        score[0][j] = j * gap_score
        trace[0][j] = "left"

    for i in range(1, rows):
        for j in range(1, cols):
            diagonal = score[i - 1][j - 1] + (match_score if a[i - 1] == b[j - 1] else mismatch_score)
            up = score[i - 1][j] + gap_score
            left = score[i][j - 1] + gap_score
            best = max(diagonal, up, left)
            score[i][j] = best
            # Deterministic tie preference: diagonal, then up, then left.
            trace[i][j] = "diag" if diagonal == best else ("up" if up == best else "left")

    aligned_a: list[str] = []
    aligned_b: list[str] = []
    i, j = len(a), len(b)
    while i > 0 or j > 0:
        direction = trace[i][j]
        if i > 0 and j > 0 and direction == "diag":
            aligned_a.append(a[i - 1])
            aligned_b.append(b[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or direction == "up"):
            aligned_a.append(a[i - 1])
            aligned_b.append("-")
            i -= 1
        else:
            aligned_a.append("-")
            aligned_b.append(b[j - 1])
            j -= 1

    aligned_a.reverse()
    aligned_b.reverse()
    result_a = "".join(aligned_a)
    result_b = "".join(aligned_b)
    match_line = "".join("|" if x == y and x != "-" else " " for x, y in zip(result_a, result_b))
    matches = sum(x == y and x != "-" for x, y in zip(result_a, result_b))
    alignment_length = len(result_a)
    identity = (matches / alignment_length * 100) if alignment_length else 0.0
    return {
        "score": score[len(a)][len(b)],
        "aligned_a": result_a,
        "match_line": match_line,
        "aligned_b": result_b,
        "matches": matches,
        "alignment_length": alignment_length,
        "identity_percent": round(identity, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Globally align two short DNA sequences.")
    parser.add_argument("sequence_a", help="First DNA sequence or path to a text/FASTA file")
    parser.add_argument("sequence_b", help="Second DNA sequence or path to a text/FASTA file")
    parser.add_argument("--from-files", action="store_true", help="Read both arguments as file paths")
    args = parser.parse_args()
    if args.from_files:
        a = Path(args.sequence_a).read_text(encoding="utf-8")
        b = Path(args.sequence_b).read_text(encoding="utf-8")
    else:
        a, b = args.sequence_a, args.sequence_b
    result = align_sequences(a, b)
    print(f"Score: {result['score']}")
    print(f"Matches: {result['matches']}/{result['alignment_length']}")
    print(f"Identity: {result['identity_percent']}%")
    print(result["aligned_a"])
    print(result["match_line"])
    print(result["aligned_b"])
    print("Educational alignment only; this result does not establish gene function or phenotype.")


if __name__ == "__main__":
    main()
