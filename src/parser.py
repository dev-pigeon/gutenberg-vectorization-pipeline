import regex  # type: ignore


class Parser:

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
