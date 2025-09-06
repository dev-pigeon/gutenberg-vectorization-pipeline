import subprocess
from timer import Timer


class Benchmarker:
    def __init__(self) -> None:
        # [(chunker, vectorizer)]
        self.worker_counts = [(1, 1), (2, 4)]
        self.file_counts = [1, 5, 25, 50, 100, 200, 400]
        self.output = self.initialize_output()
        self.timer = Timer()
        self.BOOKS_DIRECTORY = "../data/books"
        self.CRHOMA_DIRECTORY = "../data/chromadb"
        self.COLLECTION_NAME = "dev-collection"

    def generate_times(self):

        for pair in self.worker_counts:
            num_chunkers = pair[0]
            num_vectorizers = pair[1]
            # now get time for each file count for this pair
            for num_files in self.file_counts:
                self.timer.start()
                subprocess.run(["python3", "main.py", "--input", self.BOOKS_DIRECTORY,
                                "--chroma-db", self.CRHOMA_DIRECTORY, "-cn", self.COLLECTION_NAME, '-n', str(
                                    num_files),
                                "--chunkers", str(num_chunkers), "--vectorizers", str(num_vectorizers)])
                runtime = self.timer.get_time_elapsed()
                self.update_output(pair, runtime)
                self.timer.reset()

    def initialize_output(self):
        for pair in self.worker_counts:
            self.output[pair] = []
        return self.output

    def update_output(self, pair, runtime):
        times = self.output[pair]
        times.append(runtime)
        self.output[pair] = times
