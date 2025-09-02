import unittest
from parser import Parser


class TestGetTitle(unittest.TestCase):
    parser = Parser()

    valid_title = "Title: Alice's Adventures in Wonderland"
    case_insenvitive = "title: Alice's Adventures in Wonderland"
    invalid_title = "titld: fake title"

    def test_valid_title(self):
        expected = "Alice's Adventures in Wonderland"
        actual = self.parser.get_title(self.valid_title)
        self.assertEqual(expected, actual,
                         f"Expected {expected} but was {actual}")

    def test_insensitivity(self):
        expected = "Alice's Adventures in Wonderland"
        actual = self.parser.get_title(self.case_insenvitive)
        self.assertEqual(expected, actual,
                         f"Expected {expected} but was {actual}")

    def test_invalid_title(self):
        with self.assertRaises(ValueError):
            self.parser.get_title(self.invalid_title)
