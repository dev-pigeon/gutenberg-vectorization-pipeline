import chromadb  # type: ignore
from chunk import Chunk
from multiprocessing import Process, Queue


class Ingestor(Process):

    def __init__(self, collection_name: str, chroma_path: str, input_queue: Queue, id: str):
        super().__init__()
        self.buffer = []
        self.MAX_BUFFER_SIZE = 500  # chunks
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

    def batch_insert(self, collection, parameters):
        collection.add(
            ids=parameters['ids'],
            documents=parameters['documents'],
            metadatas=parameters['metadatas'],
            embeddings=parameters['embeddings']
        )

    def get_record(self, chunk_id: str, collection):
        record = collection.get(ids=[chunk_id], include=[
                                "embeddings", "metadatas", "documents"])
        return record

    def process_chunk(self, chunk, collection):
        self.buffer.append(chunk)
        if len(self.buffer) > self.MAX_BUFFER_SIZE:
            self.flush_buffer(collection)

    def flush_buffer(self, collection):
        parameters = self.get_parameters()
        self.batch_insert(collection, parameters)
        self.buffer = []

    def get_parameters(self):
        ids = []
        metas = []
        docs = []
        embeds = []
        for chunk in self.buffer:
            ids.append(chunk.chunk_id)
            docs.append(chunk.text)
            metas.append(chunk.package_metadata())
            embeds.append(chunk.embedding)

        parameters = {
            "ids": ids,
            "documents": docs,
            "metadatas": metas,
            "embeddings": embeds
        }

        return parameters

    def run(self):
        # get resources
        client = self.get_chroma_client(self.chroma_path)
        collection = self.get_collection(self.collection_name, client)

        # process chunks as they arrive
        while True:
            chunk = self.input_queue.get()
            if chunk is None:
                if (len(self.buffer) > 0):
                    self.flush_buffer(collection)
                break
            self.process_chunk(chunk, collection)
