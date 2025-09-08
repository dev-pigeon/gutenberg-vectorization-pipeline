from chunk import Chunk
from sentence_transformers import SentenceTransformer  # type: ignore
from multiprocessing import Process
from ingestor import Ingestor


class Vectorizer(Process):

    def __init__(self, pinecone_index_name, input_queue, id):
        super().__init__()
        self.pinecone_index_name = pinecone_index_name
        self.input_queue = input_queue
        self.id = id

    def embed_chunk(self, model, chunk: Chunk):
        raw_embedding = model.encode(chunk.text)
        raw_embedding = raw_embedding.astype('float32')
        embedding_list = raw_embedding.tolist()
        chunk.embedding = embedding_list
        return chunk

    def run(self):
        # init resources
        model = SentenceTransformer("all-MiniLM-L6-v2")
        ingestor = Ingestor(id=f"{self.id}-Ingestor")
        api_key = ingestor.get_pinecone_api_key()
        pinecone = ingestor.get_pinecone_instance(api_key)
        index = ingestor.get_pinecone_index(pinecone, self.pinecone_index_name)

        # process chunks as they arrive
        while True:
            task = self.input_queue.get()
            if task is None:
                if (len(ingestor.buffer) > 0):
                    ingestor.flush_buffer(index)
                break
            embedded_chunk = self.embed_chunk(
                model=model, chunk=task)
            ingestor.process_chunk(embedded_chunk, index)
