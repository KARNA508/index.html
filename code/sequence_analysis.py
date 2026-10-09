#!/usr/bin/env python3
"""Summarise DNA FASTA files for educational bioinformatics.

This module reports sequence composition only. It does not identify organisms,
genes, mutations, or phenotypes and must not be used to infer drug resistance.
Uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import csv
from html import escape
from pathlib import Path

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


def write_gc_chart(rows: list[dict[str, int | float | str]], output_path: str | Path) -> None:
    """Write a dependency-free SVG bar chart comparing GC percentages."""
    if not rows:
        raise ValueError("Cannot create a chart without sequence summary rows.")
    width = 760
    left = 220
    right = 70
    top = 65
    row_height = 42
    height = top + len(rows) * row_height + 35
    plot_width = width - left - right
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">GC percentage by DNA sequence</title>',
        '<desc id="desc">Bar chart of GC percentage calculated from canonical A, C, G, and T bases only.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="20" y="30" font-family="sans-serif" font-size="18" font-weight="bold" fill="#0f172a">GC percentage by sequence</text>',
    ]
    for tick in (0, 25, 50, 75, 100):
        x = left + plot_width * tick / 100
        parts.append(f'<line x1="{x:.1f}" y1="{top-8}" x2="{x:.1f}" y2="{height-25}" stroke="#e2e8f0"/>')
        parts.append(f'<text x="{x:.1f}" y="{height-8}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#475569">{tick}%</text>')
    for index, row in enumerate(rows):
        y = top + index * row_height
        label = escape(str(row["Sequence_ID"]))
        gc = max(0.0, min(100.0, float(row["GC_percent"])))
        parts.append(f'<text x="{left-12}" y="{y+17}" text-anchor="end" font-family="sans-serif" font-size="12" fill="#1e293b">{label}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{plot_width}" height="22" rx="4" fill="#f1f5f9"/>')
        parts.append(f'<rect x="{left}" y="{y}" width="{plot_width*gc/100:.2f}" height="22" rx="4" fill="#2563eb"/>')
        parts.append(f'<text x="{min(left + plot_width*gc/100 + 8, width-48):.1f}" y="{y+16}" font-family="sans-serif" font-size="11" fill="#0f172a">{gc:.2f}%</text>')
    parts.append("</svg>")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise DNA FASTA sequence composition.")
    parser.add_argument("input_fasta", help="Path to a DNA FASTA file")
    parser.add_argument("-o", "--output", default="sequence_summary.csv", help="Output CSV path (default: sequence_summary.csv)")
    parser.add_argument("--chart", help="Optional path for a GC percentage SVG chart")
    args = parser.parse_args()
    rows = analyse_fasta(args.input_fasta, args.output)
    print(f"Analysed {len(rows)} sequence(s). Results written to {args.output}")
    if args.chart:
        write_gc_chart(rows, args.chart)
        print(f"GC percentage chart written to {args.chart}")
    print("Reminder: sequence composition alone does not establish biological function or drug resistance.")


if __name__ == "__main__":
    main()
