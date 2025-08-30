import unittest
from parser import extractAuthor


class TestExtractAuthor(unittest.TestCase):
    valid_header = """The Project Gutenberg eBook of The Picture of Dorian Gray
    
    Title: The Picture of Dorian Gray

    Author: Oscar Wilde

    Release date: October 1, 1994 [eBook #174]
                    Most recently updated: September 18, 2024

    Language: English

    Credits: Judith Boss. HTML version by Al Haines.
    """

    invalid_header = """The Project Gutenberg eBook of The Picture of Dorian Gray
    
    Title: The Picture of Dorian Gray

    Release date: October 1, 1994 [eBook #174]
                    Most recently updated: September 18, 2024

    Language: English

    Credits: Judith Boss. HTML version by Al Haines.
    """

    def test_valud_header(self):
        expected = "Oscar Wilde"
        actual = extractAuthor(self.valid_header)
        self.assertEqual(actual, expected)

    def test_invalid_header(self):
        expected = "Unknown"
        actual = extractAuthor(self.invalid_header)
        self.assertEqual(actual, expected)
