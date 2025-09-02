import unittest
from task import ParseTask
from parser import Parser


class TestChunkFile(unittest.TestCase):

    parser = Parser()

    def test_sets_properties(self):
        task = ParseTask(
            "/Users/jackyoungadmin/Documents/Projects/vectorization/text-vectorization-pipeline/data/books/oscar_wilde.txt")
        expected_author = "Oscar Wilde"
        expected_title = "The Picture of Dorian Gray"
        expected_rd = "October 1, 1994"
        self.parser.chunk_file(task)
        self.assertEqual(expected_author, self.parser.author)
        self.assertEqual(expected_title, self.parser.title)
        self.assertEqual(expected_rd, self.parser.release_date)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.parser.chunk_file(ParseTask("fakepath/file.txt"))
