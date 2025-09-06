import subprocess
from timer import Timer


class Benchmarker:
    def __init__(self) -> None:
        # [(chunker, vectorizer)]
        self.worker_counts = [(1, 1), (2, 4)]
        self.file_counts = [1, 5, 25, 50, 100, 200, 400]
        self.output = {}
        self.timer = Timer()
        self.BOOKS_DIRECTORY = "../data/books"
        self.CRHOMA_DIRECTORY = "../data/chromadb"
        self.COLLECTION_NAME = "dev-collection"
        pass

    def generate_times(self):

        # initialize the output
        for pair in self.worker_counts:
            self.output[pair] = []

        # get the times
        for worker_count in self.worker_counts:
            num_chunkers = worker_count[0]
            num_vectorizers = worker_count[1]
            # now get time for each file count for this pair
            for num_files in self.file_counts:
                # start the timer
                self.timer.start()
                subprocess.run(["python3", "main.py", "--input", self.BOOKS_DIRECTORY,
                                "--chroma-db", self.CRHOMA_DIRECTORY, "-cn", self.COLLECTION_NAME, '-n', str(
                                    num_files),
                                "--chunkers", str(num_chunkers), "--vectorizers", str(num_vectorizers)])
                time = self.timer.get_time_elapsed()

                # make a method
                value_array = self.output[worker_count]
                value_array.append(time)
                self.output[worker_count] = value_array

                self.timer.reset()
