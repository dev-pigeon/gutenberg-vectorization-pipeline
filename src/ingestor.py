import chromadb  # type: ignore
from chunk import Chunk
from multiprocessing import Process, Queue
from pinecone import Pinecone, ServerlessSpec  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os


class Ingestor(Process):

    def __init__(self, pinecone_index: str, input_queue: Queue, id: str):
        super().__init__()
        self.buffer = []
        self.MAX_BUFFER_SIZE = 500  # chunks
        self.pinecone_index = pinecone_index
        self.input_queue = input_queue
        self.id = id

    def get_chroma_client(self, client_path: str):
        # valid chroma path is enforced by main
        chroma_client = chromadb.PersistentClient(path=client_path)
        return chroma_client

    def get_collection(self, collection_name: str, client):
        collection = client.get_or_create_collection(name=collection_name)
        return collection

    def batch_insert(self, index, parameters):
        # IMPLEMENT
        pass

    def get_record(self, chunk_id: str, collection):
        record = collection.get(ids=[chunk_id], include=[
                                "embeddings", "metadatas", "documents"])
        return record

    def process_chunk(self, chunk, index):
        self.buffer.append(chunk)
        if len(self.buffer) > self.MAX_BUFFER_SIZE:
            self.flush_buffer(index)

    def flush_buffer(self, index):
        vectors = self.get_vectors()
        self.batch_insert(index, vectors)
        self.buffer = []

    def get_vectors(self):
        vectors = []
        for chunk in self.buffer:
            vectors.append(chunk.package_chunk())
        return vectors

    def run(self):
        # get resources
        print("intializing pinecone connection")
        load_dotenv()
        api_key = os.getenv("PINECONE_API_KEY")
        print(api_key)

        pinecone = Pinecone(api_key=api_key)
        if not pinecone.has_index(self.pinecone_index):
            pinecone.create_index(
                name=self.pinecone_index,
                dimension=384,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        index = pinecone.Index(self.pinecone_index)
        stats = index.describe_index_stats()
        print(stats)

        while True:
            chunk = self.input_queue.get()
            if chunk is None:
                if (len(self.buffer) > 0):
                    pass  # flush
                break
            pass  # process


if __name__ == "__main__":
    ingestor = Ingestor(pinecone_index="my-first-index",
                        input_queue=Queue(), id="test")
    ingestor.run()
