class ParseTask:
    def __init__(self, input: str):
        self.input_path = input

    def process(self):
        """Processes the file at input_path by cleaning it, lementing it, chunking it, and storing it in output_path"""
        pass


class VectorizeTask:
    def __init__(self, input: str, output: str):
        self.input_path = input
        self.chroma_path = output

    def process(self):
        """Vectorizes the chunk at input path and stores in chroma_path"""
        pass
