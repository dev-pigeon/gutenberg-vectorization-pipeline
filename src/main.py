import argparse
import os
import sys
from util import isTextFile
from task import ParseTask
from pathlib import Path
from chunker import Chunker
from vectorizer import Vectorizer
from timer import Timer
from multiprocessing import Queue
from ingestor import Ingestor

parser = argparse.ArgumentParser(
    description="A CLI tool to vectorize text files.")

parser.add_argument('-i', '--input', required=True,
                    help='The global path to the text file or directory to vectorize.')
parser.add_argument('--chroma-db', required=True,
                    help='The global path pointing to your local persistent ChromaDB instance or the location where you would like one to be created')
parser.add_argument('-cn', '--collection-name', required=True,
                    help='The name of the ChromaDB collection where the records will be stored.')
parser.add_argument('-n', '--num-files')

args = parser.parse_args()

INPUT_PATH = args.input
CHROMA_PATH = args.chroma_db
COLLECTION_NAME = args.collection_name
NUM_FILES = int(args.num_files) if args.num_files is not None else 100

# ensure that chroma_path is valid
if not os.path.isdir(CHROMA_PATH):
    sys.exit(
        f"ERROR: The path: {CHROMA_PATH} does not exist or is not a valid directory. Please try again with a valid and existing directory path for ChromaDB")


def cleanup():
    stop_chunkers()
    stop_vectorizers()
    stop_ingestor()


def start_chunkers(num_chunkers):
    chunkers = [
        Chunker(input_queue=chunking_queue, output_queue=vectorizing_queue, id=f"Chunker-{i}") for i in range(num_chunkers)]
    for chunker in chunkers:
        chunker.start()
    return chunkers


def start_vectorizers(num_vectorizers):
    vectorizers = [Vectorizer(id=f"vectorizer-{i}", chroma_path=CHROMA_PATH,
                              collection_name=COLLECTION_NAME, input_queue=vectorizing_queue, output_queue=ingesting_queue) for i in range(num_vectorizers)]
    for v in vectorizers:
        v.start()
    return vectorizers


def start_ingestor():
    ingestor = Ingestor(collection_name=COLLECTION_NAME,
                        chroma_path=CHROMA_PATH, input_queue=ingesting_queue, id="Ingestor")
    ingestor.start()
    return ingestor


def stop_chunkers():
    # stop chunkers
    for _ in chunkers:
        chunking_queue.put(None)

    for c in chunkers:
        c.join()


def stop_vectorizers():
    for _ in vectorizers:
        vectorizing_queue.put(None)

    for v in vectorizers:
        v.join()


def stop_ingestor():
    ingesting_queue.put(None)
    ingestor.join()


if __name__ == "__main__":

    # initialize variables
    chunking_queue = Queue()
    vectorizing_queue = Queue()
    ingesting_queue = Queue()
    timer = Timer()

    # start chunkers
    num_chunkers = 2
    chunkers = start_chunkers(num_chunkers)

    # start vectorizers
    num_vectorizers = 5
    vectorizers = start_vectorizers(num_vectorizers)

    # start ingestor
    ingestor = start_ingestor()

    # run pipeline
    try:
        if os.path.isdir(INPUT_PATH):
            directory_path = Path(INPUT_PATH)
            timer.start()

            for i, item in enumerate(directory_path.iterdir()):
                if i >= NUM_FILES:
                    break
                if item.is_file():
                    file_path = item
                    path_str = str(file_path)
                    isTextFile(path_str)
                    parseTask = ParseTask(path_str)
                    chunking_queue.put(parseTask)
                    # chunkers put in vector queue and vectorizers handle and end

        elif os.path.isfile(INPUT_PATH):
            timer.start()
            isTextFile(INPUT_PATH)
            parseTask = ParseTask(INPUT_PATH)
            chunking_queue.put(parseTask)

        else:
            sys.exit(
                "ERROR: The input path provided does not exist. Please try again and enter a valid path.")
    except ValueError as e:
        print(e)

    # cleanup
    cleanup()
    time_elapsed = timer.get_time_elapsed()
    print(f"Finished processing in {time_elapsed}")
