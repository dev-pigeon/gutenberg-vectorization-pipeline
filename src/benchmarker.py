import subprocess
from timer import Timer
from datetime import datetime
import matplotlib.pyplot as plt
import time


class Benchmarker:
    def __init__(self) -> None:
        # [(chunker, vectorizer)]
        self.worker_counts = [(1, 1), (2, 4), (3, 3), (4, 4)]
        self.file_counts = [1, 5, 10, 20, 50]
        self.output = {}
        self.timer = Timer()
        self.BOOKS_DIRECTORY = "../data/books"
        self.CRHOMA_DIRECTORY = "../data/chromadb"
        self.COLLECTION_NAME = "dev-collection"
        self.TIMER_OVERHEAD = 3  # seconds - temp fix will be better in future

    def generate_plots(self):
        self.generate_times()

        for worker_pair, time_pairs in self.output.items():
            # now times is a list of tuples (time, file count)
            x_axis = []
            y_axis = []
            for pair in time_pairs:
                y_axis.append(pair[0])
                x_axis.append(pair[1])

            plt.plot(x_axis, y_axis, marker="o")
            plt.xlabel("Number of Files")
            plt.ylabel("Runtime (seconds)")
            plt.title(f"Runtime Distribution for Worker Pair {worker_pair}")
            print(f"Saving Plot for worker pair {worker_pair}")
            save_path = "../data/output/pinecone/" + \
                str(worker_pair) + "plot.png"
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

    def generate_times(self):

        self.output = self.initialize_output()

        for pair in self.worker_counts:
            num_chunkers = pair[0]
            num_vectorizers = pair[1]
            # now get time for each file count for this pair
            for num_files in self.file_counts:
                print(
                    f"******************** \nFiles: {num_files} ---- Chunkers: {num_chunkers} ---- Vectorizers: {num_vectorizers} \nStarted at: {datetime.now().strftime("%H:%M:%S")}")
                self.timer.start()
                subprocess.run(["python3", "main.py", "--input", self.BOOKS_DIRECTORY,
                                "--chroma-db", self.CRHOMA_DIRECTORY, "-cn", self.COLLECTION_NAME, '-n', str(
                                    num_files),
                                "--chunkers", str(num_chunkers), "--vectorizers", str(num_vectorizers)])
                runtime = self.timer.get_time_elapsed()
                self.update_output(
                    pair, runtime - self.TIMER_OVERHEAD, num_files)
                self.timer.reset()

                # clean pinecone to prevent going over free tier storage
                print("Execution finished - cleaning pinecone instance...")
                subprocess.run(["python3", "clean_pinecone.py"])
                print("********************")

    def initialize_output(self):
        for pair in self.worker_counts:
            self.output[pair] = []
        return self.output

    def update_output(self, pair, runtime, num_files):
        times = self.output[pair]
        print(f"finished in {runtime} seconds")
        times.append((runtime, num_files))
        self.output[pair] = times


if __name__ == "__main__":
    benchmarker = Benchmarker()
    benchmarker.generate_plots()
