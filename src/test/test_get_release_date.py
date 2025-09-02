import unittest
from parser import Parser


class TestGetReleaseDate(unittest.TestCase):
    parser = Parser()
    text = """
Title: Frankenstein; Or, The Modern Prometheus

Author: Mary Wollstonecraft Shelley

Release date: November 23, 2012 [eBook #41445]
                Most recently updated: October 23, 2024

Language: English

Original publication: United Kingdom: Lackington, Hughes, Harding, Mavor, & Jones, 1818
"""

    def test_valid_release_date(self):
        expected = "November 23, 2012"
        actual = self.parser.get_release_date(self.text)
        self.assertEqual(expected, actual,
                         f"Expected {expected} but was {actual}")
