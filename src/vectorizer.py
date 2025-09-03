from chunk import Chunk
from sentence_transformers import SentenceTransformer  # type: ignore


class Vectorizer:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_chunk(self, chunk: Chunk):
        raw_embedding = self.model.encode(chunk.text)
        raw_embedding = raw_embedding.astype('float32')
        embedding_list = raw_embedding.tolist()
        chunk.embedding = embedding_list
        return chunk
