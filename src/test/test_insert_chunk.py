import unittest
import ingestor
from chunk import Chunk


class TestInsertChunk(unittest.TestCase):
    chunk = Chunk("Title", "Author", "This is the chunk text",
                  "September 3, 2025", "Title-5")
    chunk.embedding = [-.042948, 0.39285, -0.398]

    def test_inserts_no_error(self):
        client = ingestor.get_chroma_client(
            "/Users/jackyoungadmin/Documents/Projects/vectorization/text-vectorization-pipeline/data/chromadb")
        collection = ingestor.get_collection("test_collection", client)
        ingestor.insert_chunk(collection, self.chunk)
        client.delete_collection(name="test_collection")
