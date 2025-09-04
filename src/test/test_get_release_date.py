import unittest
from chunker import Chunker
from multiprocessing import Queue


class TestGetReleaseDate(unittest.TestCase):
    chunker = Chunker(Queue(), "test-chunker")
    text = """
Title: Frankenstein; Or, The Modern Prometheus

Author: Mary Wollstonecraft Shelley

Release date: November 23, 2012 [eBook #41445]
                Most recently updated: October 23, 2024

Language: English

Original publication: United Kingdom: Lackington, Hughes, Harding, Mavor, & Jones, 1818
"""

    case_insensitive = """Author: Mary Wollstonecraft Shelley

Release date: june 24, 1999 [eBook #41445]
                Most recently updated: October 23, 2024"""

    def test_valid_release_date(self):
        expected = "November 23, 2012"
        actual = self.chunker.get_release_date(self.text)
        self.assertEqual(expected, actual,
                         f"Expected {expected} but was {actual}")

    def test_invalid_release_date(self):
        expected = "Unknown"
        actual = self.chunker.get_release_date("This is a fake header")
        self.assertEqual(expected, actual,
                         f"Expected {expected} but was {actual}")

    def test_case_insensitivity(self):
        expected = "june 24, 1999"
        actual = self.chunker.get_release_date(self.case_insensitive)
        self.assertEqual(expected, actual,
                         f"Expected {expected} but was {actual}")
