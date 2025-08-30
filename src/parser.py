import regex


def extractAuthor(header: str):
    match = regex.search(r"Author:", header)
    if match:
        line_end = header.find("\n", match.end())
        author = header[match.end():line_end].strip()
        return author
    return ""
