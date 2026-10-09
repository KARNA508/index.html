#!/usr/bin/env python3
"""Summarise DNA FASTA files for educational bioinformatics.

This module reports sequence composition only. It does not identify organisms,
genes, mutations, or phenotypes and must not be used to infer drug resistance.
Uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

VALID_IUPAC_DNA = set("ACGTRYSWKMBDHVN")
BASES = "ACGT"


def parse_fasta(path: str | Path) -> list[tuple[str, str]]:
    """Read FASTA records, returning (identifier, sequence) pairs.

    Raises ValueError for malformed FASTA, empty sequences, duplicate IDs,
    or symbols outside the standard IUPAC DNA alphabet.
    """
    records: list[tuple[str, str]] = []
    current_id: str | None = None
    chunks: list[str] = []

    def finish_record() -> None:
        nonlocal current_id, chunks
        if current_id is None:
            return
        sequence = "".join(chunks).upper()
        if not sequence:
            raise ValueError(f"FASTA record {current_id!r} has an empty sequence.")
        invalid = sorted(set(sequence) - VALID_IUPAC_DNA)
        if invalid:
            raise ValueError(
                f"FASTA record {current_id!r} contains invalid DNA symbols: "
                + ", ".join(invalid)
            )
        records.append((current_id, sequence))

    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith(">"):
                finish_record()
                current_id = line[1:].strip()
                if not current_id:
                    raise ValueError(f"Missing FASTA identifier on line {line_number}.")
                chunks = []
            else:
                if current_id is None:
                    raise ValueError(
                        f"Sequence text appears before a FASTA header on line {line_number}."
                    )
                chunks.append("".join(line.split()))

    finish_record()
    if not records:
        raise ValueError("No FASTA records found.")
    ids = [record_id for record_id, _ in records]
    if len(ids) != len(set(ids)):
        raise ValueError("FASTA identifiers must be unique.")
    return records


def summarise_sequence(record_id: str, sequence: str) -> dict[str, int | float | str]:
    """Calculate length, base counts, ambiguous count, and GC percentage."""
    sequence = "".join(sequence.split()).upper()
    if not sequence:
        raise ValueError(f"Sequence {record_id!r} is empty.")
    invalid = sorted(set(sequence) - VALID_IUPAC_DNA)
    if invalid:
        raise ValueError(
            f"Sequence {record_id!r} contains invalid DNA symbols: " + ", ".join(invalid)
        )

    length = len(sequence)
    counts = {base: sequence.count(base) for base in BASES}
    canonical_count = sum(counts.values())
    gc_percent = round(((counts["G"] + counts["C"]) / canonical_count) * 100, 2) if canonical_count else 0.0
    return {
        "Sequence_ID": record_id,
        "Length_bp": length,
        "A_count": counts["A"],
        "C_count": counts["C"],
        "G_count": counts["G"],
        "T_count": counts["T"],
        "Ambiguous_bases": length - canonical_count,
        "GC_percent": gc_percent,
    }


def analyse_fasta(input_path: str | Path, output_path: str | Path) -> list[dict[str, int | float | str]]:
    """Parse a FASTA file and write one CSV summary row per sequence."""
    rows = [summarise_sequence(record_id, sequence) for record_id, sequence in parse_fasta(input_path)]
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise DNA FASTA sequence composition.")
    parser.add_argument("input_fasta", help="Path to a DNA FASTA file")
    parser.add_argument("-o", "--output", default="sequence_summary.csv", help="Output CSV path (default: sequence_summary.csv)")
    args = parser.parse_args()
    rows = analyse_fasta(args.input_fasta, args.output)
    print(f"Analysed {len(rows)} sequence(s). Results written to {args.output}")
    print("Reminder: sequence composition alone does not establish biological function or drug resistance.")


if __name__ == "__main__":
    main()
