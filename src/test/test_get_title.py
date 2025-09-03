import unittest
from chunker import Chunker


class TestGetTitle(unittest.TestCase):
    chunker = Chunker()

    valid_title = "Title: Alice's Adventures in Wonderland"
    case_insenvitive = "title: Alice's Adventures in Wonderland"
    invalid_title = "titld: fake title"

    def test_valid_title(self):
        expected = "Alice's Adventures in Wonderland"
        actual = self.chunker.get_title(self.valid_title)
        self.assertEqual(expected, actual,
                         f"Expected {expected} but was {actual}")

    def test_insensitivity(self):
        expected = "Alice's Adventures in Wonderland"
        actual = self.chunker.get_title(self.case_insenvitive)
        self.assertEqual(expected, actual,
                         f"Expected {expected} but was {actual}")

    def test_invalid_title(self):
        with self.assertRaises(ValueError):
            self.chunker.get_title(self.invalid_title)
