import regex  # type: ignore


class Parser:

    header = ""
    body = None

    def __init__(self):
        pass

    def extractAuthor(self, header: str):
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

    def extractHeader(self, text: str):
        match = regex.search(r"\*\*\* START OF THE PROJECT GUTENBERG", text)
        if match:
            header_end = match.start()
            self.header = text[:header_end].strip()

        else:
            raise ValueError("ERROR: Text header is missing.")

    def normalize(self, s: str) -> str:
        return "\n".join(line.strip() for line in s.splitlines())
