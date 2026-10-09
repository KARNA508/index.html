#!/usr/bin/env python3
"""Download a small, documented set of public NCBI nucleotide FASTA records.

This script fetches general bacterial 16S rRNA reference records by accession.
It records retrieval time, length, and SHA-256 so the downloaded dataset can
be traced and checked later. It does not analyze or predict drug resistance.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

NCBI_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
DEFAULT_USER_AGENT = "EducationalBioinformaticsSequenceProject/1.0 (reference-data fetch)"


def read_accessions(csv_path: str | Path) -> list[dict[str, str]]:
    with Path(csv_path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {"accession", "organism", "gene", "record_note", "source_url"}
    if not rows:
        raise ValueError(f"No accessions found in {csv_path}.")
    if not required.issubset(rows[0]):
        raise ValueError("Accession CSV must contain: " + ", ".join(sorted(required)))
    seen: set[str] = set()
    for row in rows:
        accession = row["accession"].strip()
        if not accession:
            raise ValueError("An accession row is missing its accession value.")
        if accession in seen:
            raise ValueError(f"Duplicate accession: {accession}")
        seen.add(accession)
        if not accession.replace("_", "").replace(".", "").isalnum():
            raise ValueError(f"Unexpected accession format: {accession}")
    return rows


def fetch_fasta(accession: str, timeout: int = 30) -> str:
    """Fetch one accession from NCBI EFetch as FASTA text."""
    query = urlencode({
        "db": "nuccore",
        "id": accession,
        "rettype": "fasta",
        "retmode": "text",
    })
    request = Request(
        f"{NCBI_EFETCH}?{query}",
        headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "text/plain"},
    )
    with urlopen(request, timeout=timeout) as response:
        text = response.read().decode("utf-8")
    if not text.lstrip().startswith(">"):
        raise ValueError(
            f"NCBI did not return FASTA for {accession}. Check the accession and try again."
        )
    return text.strip() + "\n"


def parse_fasta_text(text: str) -> tuple[str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines or not lines[0].startswith(">"):
        raise ValueError("Invalid FASTA response: missing header.")
    record_id = lines[0][1:].strip()
    sequence = "".join(lines[1:]).upper()
    if not record_id or not sequence:
        raise ValueError("Invalid FASTA response: missing identifier or sequence.")
    invalid = sorted(set(sequence) - set("ACGTRYSWKMBDHVN"))
    if invalid:
        raise ValueError("Unexpected symbols in downloaded DNA sequence: " + ", ".join(invalid))
    return record_id, sequence


def download_dataset(
    accessions_csv: str | Path,
    output_fasta: str | Path,
    manifest_csv: str | Path,
    delay_seconds: float = 0.4,
) -> list[dict[str, str | int]]:
    """Fetch each listed accession and write FASTA plus a provenance manifest."""
    accessions = read_accessions(accessions_csv)
    fasta_records: list[str] = []
    manifest: list[dict[str, str | int]] = []
    for index, item in enumerate(accessions):
        accession = item["accession"].strip()
        if index:
            time.sleep(max(0.0, delay_seconds))
        fasta = fetch_fasta(accession)
        record_id, sequence = parse_fasta_text(fasta)
        retrieved = datetime.now(timezone.utc).isoformat(timespec="seconds")
        fasta_records.append(f">{accession} | {item['organism']} | {item['gene']}\n{sequence}\n")
        manifest.append({
            "accession": accession,
            "organism": item["organism"],
            "gene": item["gene"],
            "record_note": item["record_note"],
            "source_url": item["source_url"],
            "retrieved_utc": retrieved,
            "sequence_length_bp": len(sequence),
            "sha256": hashlib.sha256(sequence.encode("ascii")).hexdigest(),
            "ncbi_record_title": record_id,
        })

    fasta_path = Path(output_fasta)
    manifest_path = Path(manifest_csv)
    fasta_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    fasta_path.write_text("".join(fasta_records), encoding="utf-8")
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0].keys()))
        writer.writeheader()
        writer.writerows(manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch documented bacterial 16S rRNA records from NCBI."
    )
    parser.add_argument("--accessions", default="data/reference_accessions.csv")
    parser.add_argument("--fasta", default="data/reference_16s_sequences.fasta")
    parser.add_argument("--manifest", default="data/reference_sequence_manifest.csv")
    args = parser.parse_args()
    manifest = download_dataset(args.accessions, args.fasta, args.manifest)
    print(f"Downloaded {len(manifest)} reference sequence(s) from NCBI.")
    print(f"FASTA: {args.fasta}")
    print(f"Provenance manifest: {args.manifest}")
    print("This dataset is for general sequence-composition learning, not phenotype prediction.")


if __name__ == "__main__":
    main()
