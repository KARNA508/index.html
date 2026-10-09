import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from sequence_analysis import parse_fasta, summarise_sequence, analyse_fasta


class SequenceAnalysisTests(unittest.TestCase):
    def test_gc_percent_and_ambiguous_bases(self):
        row = summarise_sequence("demo", "ACGTNN")
        self.assertEqual(row["Length_bp"], 6)
        self.assertEqual(row["Ambiguous_bases"], 2)
        self.assertEqual(row["GC_percent"], 50.0)

    def test_parse_multiline_fasta(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "input.fasta"
            path.write_text(">one\nACG\nTN\n>two\nGGCC\n", encoding="utf-8")
            self.assertEqual(parse_fasta(path), [("one", "ACGTN"), ("two", "GGCC")])

    def test_invalid_symbol_rejected(self):
        with self.assertRaises(ValueError):
            summarise_sequence("bad", "ACGTZ")

    def test_empty_record_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "empty.fasta"
            path.write_text(">empty\n>next\nACGT\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_fasta(path)

    def test_csv_export(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "input.fasta"
            target = Path(temp) / "out" / "summary.csv"
            source.write_text(">one\nACGT\n", encoding="utf-8")
            rows = analyse_fasta(source, target)
            self.assertEqual(len(rows), 1)
            self.assertTrue(target.exists())
            self.assertIn("GC_percent", target.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
