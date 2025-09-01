import unittest
from parser import Parser


class TestExtractHeader(unittest.TestCase):

    parser = Parser()
    text = """
        The Project Gutenberg eBook of Frankenstein; Or, The Modern Prometheus

This ebook is for the use of anyone anywhere in the United States and
most other parts of the world at no cost and with almost no restrictions
whatsoever. You may copy it, give it away or re-use it under the terms
of the Project Gutenberg License included with this ebook or online
at www.gutenberg.org. If you are not located in the United States,
you will have to check the laws of the country where you are located
before using this eBook.

Title: Frankenstein; Or, The Modern Prometheus

Author: Mary Wollstonecraft Shelley

Release date: November 23, 2012 [eBook #41445]
                Most recently updated: October 23, 2024

Language: English

Original publication: United Kingdom: Lackington, Hughes, Harding, Mavor, & Jones, 1818

Credits: Produced by Greg Weeks, Mary Meehan and the Online
        Distributed Proofreading Team at http://www.pgdp.net
        Revised by Richard Tonsing.


*** START OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN; OR, THE MODERN PROMETHEUS ***
    [Transcriber’s Note: This text was produced from a photo-reprint of the
    1818 edition.]




                                FRANKENSTEIN;

                                    OR,

                            THE MODERN PROMETHEUS.


        IN THREE VOLUMES.
        VOL. I.

        London:

        _PRINTED FOR_
        LACKINGTON, HUGHES, HARDING, MAVOR, & JONES,
        FINSBURY SQUARE.
"""

    valid_expected = """The Project Gutenberg eBook of Frankenstein; Or, The Modern Prometheus

    This ebook is for the use of anyone anywhere in the United States and
    most other parts of the world at no cost and with almost no restrictions
    whatsoever. You may copy it, give it away or re-use it under the terms
    of the Project Gutenberg License included with this ebook or online
    at www.gutenberg.org. If you are not located in the United States,
    you will have to check the laws of the country where you are located
    before using this eBook.

    Title: Frankenstein; Or, The Modern Prometheus

    Author: Mary Wollstonecraft Shelley

    Release date: November 23, 2012 [eBook #41445]
                    Most recently updated: October 23, 2024

    Language: English

    Original publication: United Kingdom: Lackington, Hughes, Harding, Mavor, & Jones, 1818

    Credits: Produced by Greg Weeks, Mary Meehan and the Online
            Distributed Proofreading Team at http://www.pgdp.net
            Revised by Richard Tonsing."""

    def test_extract_valid_header(self):
        self.parser.extractHeader(self.text)
        actual = self.parser.header
        self.assertMultiLineEqual(self.parser.normalize(
            actual), self.parser.normalize(self.valid_expected.strip()))

    def test_extract_invalid_header(self):
        with self.assertRaises(ValueError):
            self.parser.extractHeader("Fake Header")
