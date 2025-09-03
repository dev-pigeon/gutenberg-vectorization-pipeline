import regex  # type: ignore
from chunk import Chunk
from task import ParseTask


class Chunker:

    header = ""
    header_end_index = -1
    body = ""
    release_date = ""
    title = ""
    author = ""
    chunks = []

    def __init__(self):
        pass

    def chunk_file(self, task: ParseTask):
        try:
            with open(task.input_path, "r") as file:
                text = file.read()
                self.header = self.extract_header(text)
                self.body = self.extract_body(text)
                self.title = self.get_title(self.header)
                self.author = self.extract_author(self.header)
                self.release_date = self.get_release_date(self.header)
                self.chunks = self.chunk_text(self.body)

        except FileNotFoundError:
            raise FileNotFoundError(f"File {task.input_path} does not exist.")

        except ValueError as e:
            raise ValueError(e)

    def extract_author(self, header: str):
        match = regex.search(r"Author:", header)

        if match:
            author = ""
            line_end = header.find("\n", match.end())
            if line_end == -1:
                author = header[match.end():].strip()
            else:
                author = header[match.end():line_end].strip()
            return author

        return "Unknown"

    def extract_header(self, text: str):
        self.extract_body(text)
        match = regex.search(r"\*\*\* START OF THE PROJECT GUTENBERG", text)
        if match:
            self.header_end_index = match.start()
            header = text[:self.header_end_index].strip()
            return header

        else:
            raise ValueError("ERROR: Text header is missing.")

    def extract_body(self, text: str):
        # header_end_index has either been set or extract_header raised an error
        # in the second case, the parser will have moved on to the next file
        # so header_end_index should always be valid at this point
        line_end = text.find("\n", self.header_end_index)
        # body = text[line_end:].strip()
        end_pattern = r"\*{3}\s*END OF THE PROJECT"
        match = regex.search(end_pattern, text)
        if match:
            file_end = match.start()
            body = text[line_end:file_end]
            return body
        # no end signature detected, get the entire thing

        return text[line_end:]

    def get_release_date(self, header: str):
        pattern = r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}"
        match = regex.search(pattern, header, regex.IGNORECASE)
        if match:
            release_date = match.group()
            return release_date
        else:
            return "Unknown"

    def get_title(self, header: str):
        pattern = r"Title:\s?"
        match = regex.search(pattern, header, regex.IGNORECASE)
        if match:
            end_of_line = header.find("\n", match.start())
            if end_of_line != -1:
                title = header[match.end():end_of_line].strip()
                return title
            else:
                title = header[match.end():].strip()
                return title

        else:
            raise ValueError(
                "WARNING: File does not contain valid book title - skipping.")

    def chunk_text(self, body: str, min_tokens=250):

        paragraphs = [para.strip()
                      for para in body.split("\n\n") if para.strip()]
        current_chunk = ""
        chunks = []
        chunk_count = 0

        for para in paragraphs:
            current_chunk += para

            if len(current_chunk) >= min_tokens:
                # make a chunk
                chunk = Chunk(title=self.title, author=self.author, text=current_chunk.strip(
                ), release_date=self.release_date, chunk_id=chunk_count)
                chunks.append(chunk)
                # gets the last seventy five characters as overlap
                current_chunk = current_chunk[-75:]
                chunk_count += 1
        for chunk in chunks:
            print(chunk.to_json())
        return chunks

    def normalize(self, s: str) -> str:
        return "\n".join(line.strip() for line in s.splitlines())
