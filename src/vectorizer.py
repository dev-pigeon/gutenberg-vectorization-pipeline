from chunk import Chunk
from sentence_transformers import SentenceTransformer  # type: ignore
import ingestor
from multiprocessing import Process


class Vectorizer(Process):

    def __init__(self, chroma_path, collection_name, queue):
        super().__init__()
        self.chroma_path = chroma_path
        self.collection_name = collection_name
        self.queue = queue

    def embed_and_insert_chunk(self, model, collection, chunk: Chunk):
        raw_embedding = model.encode(chunk.text)
        raw_embedding = raw_embedding.astype('float32')
        embedding_list = raw_embedding.tolist()
        chunk.embedding = embedding_list
        ingestor.insert_chunk(collection, chunk)

    def run(self):
        # init model & collection here to avoid pickle error
        model = SentenceTransformer("all-MiniLM-L6-v2")
        collection = ingestor.get_collection(
            self.collection_name, ingestor.get_chroma_client(self.chroma_path))

        print("vectorizer starting", flush=True)
        while True:
            task = self.queue.get()
            if task is None:
                print("vectorizer ending")
                break
            print(f"vectorizing chunk {task.chunk_id}")
            self.embed_and_insert_chunk(
                model=model, collection=collection, chunk=task)
