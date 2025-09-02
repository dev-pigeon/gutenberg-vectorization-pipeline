import regex  # type: ignore


class Parser:

    header = ""
    header_end_index = -1
    body = None
    release_date = ""

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
            self.header_end_index = match.start()
            self.header = text[:self.header_end_index].strip()

        else:
            raise ValueError("ERROR: Text header is missing.")

    def extract_body(self, text: str):
        # header_end_index has either been set or extractHeader raised an error
        # in the second case, the parser will have moved on to the next file
        # therefor, header_end_index should always be valid at this point
        line_end = text.find("\n", self.header_end_index)
        self.body = text[line_end:].strip()

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
        match = regex.search(pattern, header)
        if match:
            end_of_line = header.find("\n", match.start())
            print(match.group())
            if end_of_line != -1:
                title = header[match.end():end_of_line].strip()
                return title
            else:
                title = header[match.end():].strip()
                return title

        return ""

    def normalize(self, s: str) -> str:
        return "\n".join(line.strip() for line in s.splitlines())
