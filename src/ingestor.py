import chromadb  # type: ignore
from chunk import Chunk
from multiprocessing import Process, Queue


class Ingestor(Process):

    def __init__(self, collection_name: str, chroma_path: str, input_queue: Queue, id: str):
        super().__init__()
        self.collection_name = collection_name
        self.chroma_path = chroma_path
        self.input_queue = input_queue
        self.id = id

    def get_chroma_client(self, client_path: str):
        # valid chroma path is enforced by main
        chroma_client = chromadb.PersistentClient(path=client_path)
        return chroma_client

    def get_collection(self, collection_name: str, client):
        collection = client.get_or_create_collection(name=collection_name)
        return collection

    def insert_chunk(self, collection, chunk: Chunk):
        metadata = chunk.package_metadata()
        collection.add(
            ids=[chunk.chunk_id],
            documents=[chunk.text],
            metadatas=[metadata],
            embeddings=[chunk.embedding]
        )

    def get_record(self, chunk_id: str, collection):
        record = collection.get(ids=[chunk_id], include=[
                                "embeddings", "metadatas", "documents"])
        return record

    def run(self):
        # get resources
        client = self.get_chroma_client(self.chroma_path)
        collection = self.get_collection(self.collection_name, client)

        # insert chunks as they arrive
        while True:
            chunk = self.input_queue.get()
            if chunk is None:
                break
            self.insert_chunk(collection, chunk)
