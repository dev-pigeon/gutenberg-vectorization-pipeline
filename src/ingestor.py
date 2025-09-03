import chromadb  # type: ignore
from chunk import Chunk


def get_chroma_client(client_path: str):
    # valid chroma path is enforced by main
    chroma_client = chromadb.PersistentClient(path=client_path)
    return chroma_client


def get_collection(collection_name: str, client):
    collection = client.get_or_create_collection(name=collection_name)
    return collection


def insert_chunk(collection, chunk: Chunk):
    metadata = chunk.package_metadata()
    collection.add(
        ids=[chunk.chunk_id],
        documents=[chunk.text],
        metadatas=[metadata],
        embeddings=[chunk.embedding]
    )


def get_record(chunk_id: str, collection):
    record = collection.get(ids=[chunk_id], include=[
                            "embeddings", "metadatas", "documents"])
    return record
