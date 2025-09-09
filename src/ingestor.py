from pinecone import Pinecone, ServerlessSpec  # type: ignore
from pinecone.exceptions import PineconeApiException  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os


class Ingestor():

    def __init__(self, id: str):
        self.buffer = []
        self.MAX_BUFFER_SIZE = 500  # chunks
        self.id = id
        self.api_key = os.getenv("PINECONE_API_KEY")

    def get_pinecone_instance(self, api_key):
        pinecone = Pinecone(api_key=api_key)
        return pinecone

    def get_pinecone_api_key(self):
        load_dotenv()
        api_key = os.getenv("PINECONE_API_KEY")
        return api_key

    def get_pinecone_index(self, pinecone, index_name):

        try:
            if not pinecone.has_index(index_name):
                pinecone.create_index(
                    name=index_name,
                    dimension=384,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
        except PineconeApiException as e:
            if e.status == 409:
                print(
                    f"Index '{index_name}' already exists, skipping creation.")
            else:
                raise

        index = pinecone.Index(index_name)
        return index

    def batch_insert(self, index, vectors):
        index.upsert(vectors)

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
