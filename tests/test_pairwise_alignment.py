import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from pairwise_alignment import align_sequences, clean_sequence


class PairwiseAlignmentTests(unittest.TestCase):
    def test_identical_sequences(self):
        result = align_sequences("ACGT", "ACGT")
        self.assertEqual(result["aligned_a"], "ACGT")
        self.assertEqual(result["aligned_b"], "ACGT")
        self.assertEqual(result["score"], 4)
        self.assertEqual(result["identity_percent"], 100.0)

    def test_mismatch(self):
        result = align_sequences("ACGT", "AGGT")
        self.assertEqual(result["matches"], 3)
        self.assertEqual(result["alignment_length"], 4)
        self.assertEqual(result["identity_percent"], 75.0)

    def test_gap_alignment(self):
        result = align_sequences("ACGGT", "ACGT")
        self.assertEqual(len(result["aligned_a"]), len(result["aligned_b"]))
        self.assertIn("-", result["aligned_a"] + result["aligned_b"])
        self.assertEqual(result["matches"], 4)

    def test_fasta_header_and_whitespace(self):
        self.assertEqual(clean_sequence(">example\nac gt\n"), "ACGT")

    def test_invalid_and_empty_sequences(self):
        with self.assertRaises(ValueError):
            align_sequences("ACGTZ", "ACGT")
        with self.assertRaises(ValueError):
            align_sequences("", "ACGT")


if __name__ == "__main__":
    unittest.main()
