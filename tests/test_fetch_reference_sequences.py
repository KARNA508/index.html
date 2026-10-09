import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from fetch_reference_sequences import parse_fasta_text, read_accessions


class ReferenceSequenceTests(unittest.TestCase):
    def test_parse_fasta_response(self):
        record_id, sequence = parse_fasta_text(">NCBI title\nACGT\nNN\n")
        self.assertEqual(record_id, "NCBI title")
        self.assertEqual(sequence, "ACGTNN")

    def test_reject_non_fasta(self):
        with self.assertRaises(ValueError):
            parse_fasta_text("No sequence here")

    def test_read_accession_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "accessions.csv"
            path.write_text(
                "accession,organism,gene,record_note,source_url\n"
                "J01859.1,Escherichia coli,16S rRNA,Complete,https://example.org/record\n",
                encoding="utf-8",
            )
            rows = read_accessions(path)
            self.assertEqual(rows[0]["accession"], "J01859.1")

    def test_reject_duplicate_accessions(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "accessions.csv"
            path.write_text(
                "accession,organism,gene,record_note,source_url\n"
                "J01859.1,E. coli,16S rRNA,Complete,https://example.org/1\n"
                "J01859.1,E. coli,16S rRNA,Complete,https://example.org/2\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                read_accessions(path)


if __name__ == "__main__":
    unittest.main()
