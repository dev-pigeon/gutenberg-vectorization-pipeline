import json


class Chunk:

    def __init__(self, title: str, author: str | None, text: str, release_date: str | None, chunk_id: str) -> None:
        self.title = title
        self.author = author
        self.text = text
        self.release_date = release_date
        self.chunk_id = chunk_id
        self.embedding = []

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(**data)

    def package_metadata(self):
        # author, title, release date
        metadata = {
            "author": self.author,
            "title": self.title,
            "release_date": self.release_date
        }
        return metadata
