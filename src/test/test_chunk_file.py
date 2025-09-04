import unittest
from task import ParseTask
from chunker import Chunker
from multiprocessing import Queue


class TestChunkFile(unittest.TestCase):

    chunker = Chunker(Queue(), Queue(), "test-chunker")

    def test_sets_properties(self):
        task = ParseTask(
            "/Users/jackyoungadmin/Documents/Projects/vectorization/text-vectorization-pipeline/data/books/oscar_wilde.txt")
        expected_author = "Oscar Wilde"
        expected_title = "The Picture of Dorian Gray"
        expected_rd = "October 1, 1994"
        self.chunker.chunk_file(task)
        self.assertEqual(expected_author, self.chunker.author)
        self.assertEqual(expected_title, self.chunker.title)
        self.assertEqual(expected_rd, self.chunker.release_date)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.chunker.chunk_file(ParseTask("fakepath/file.txt"))
