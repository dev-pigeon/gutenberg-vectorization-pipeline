import chromadb  # type: ignore
from chunk import Chunk


def get_chroma_client(client_path: str):
    # valid chroma path is enforced by main
    chroma_client = chromadb.PersistentClient()
    return chroma_client


def get_collection(collection_name: str, client):
    collection = client.get_or_create_collection(name=collection_name)
    return collection


def insert_chunk(client, chunk: Chunk):
    pass
