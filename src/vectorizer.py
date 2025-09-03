from chunk import Chunk
from sentence_transformers import SentenceTransformer  # type: ignore
import ingestor


class Vectorizer:

    def __init__(self, chroma_path, collection_name):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.collection = ingestor.get_collection(
            collection_name, ingestor.get_chroma_client(chroma_path))

    def embed_and_insert_chunks(self, chunks):
        for chunk in chunks:
            print(f"Embedding chunk: {chunk.chunk_id}")
            self.embed_and_insert_chunk(chunk)

    def embed_and_insert_chunk(self, chunk: Chunk):
        raw_embedding = self.model.encode(chunk.text)
        raw_embedding = raw_embedding.astype('float32')
        embedding_list = raw_embedding.tolist()
        chunk.embedding = embedding_list
        ingestor.insert_chunk(self.collection, chunk)
