from chunk import Chunk
from sentence_transformers import SentenceTransformer  # type: ignore
import ingestor
from multiprocessing import Process


class Vectorizer(Process):

    def __init__(self, chroma_path, collection_name, queue, id):
        super().__init__()
        self.chroma_path = chroma_path
        self.collection_name = collection_name
        self.queue = queue
        self.id = id

    def embed_and_insert_chunk(self, model, chunk: Chunk):
        raw_embedding = model.encode(chunk.text)
        raw_embedding = raw_embedding.astype('float32')
        embedding_list = raw_embedding.tolist()
        chunk.embedding = embedding_list
        # put into third queue

    def run(self):
        # init model here to avoid pickle error
        model = SentenceTransformer("all-MiniLM-L6-v2")

        print(f"{self.id} starting", flush=True)
        while True:
            task = self.queue.get()
            if task is None:
                print(f"{self.id} ending", flush=True)
                break
            self.embed_and_insert_chunk(
                model=model, chunk=task)
