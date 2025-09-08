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

parser = argparse.ArgumentParser(
    description="A CLI tool to vectorize text files.")

parser.add_argument('-i', '--input', required=True,
                    help='The global path to the text file or directory to vectorize.')
parser.add_argument('--chroma-db', required=True,
                    help='The global path pointing to your local persistent ChromaDB instance or the location where you would like one to be created')
parser.add_argument('-cn', '--collection-name', required=True,
                    help='The name of the ChromaDB collection where the records will be stored.')
parser.add_argument('-n', '--num-files')
parser.add_argument('--chunkers')
parser.add_argument('--vectorizers')


args = parser.parse_args()

INPUT_PATH = args.input
CHROMA_PATH = args.chroma_db
COLLECTION_NAME = args.collection_name
NUM_FILES = int(args.num_files) if args.num_files is not None else 100
NUM_CHUNKERS = int(args.chunkers) if args.chunkers is not None else 2
NUM_VECTORIZERS = int(args.vectorizers) if args.vectorizers is not None else 4

# ensure that chroma_path is valid
if not os.path.isdir(CHROMA_PATH):
    sys.exit(
        f"ERROR: The path: {CHROMA_PATH} does not exist or is not a valid directory. Please try again with a valid and existing directory path for ChromaDB")


def cleanup():
    stop_chunkers()
    stop_vectorizers()


def start_chunkers():
    chunkers = [
        Chunker(input_queue=chunking_queue, output_queue=vectorizing_queue, id=f"Chunker-{i}") for i in range(NUM_CHUNKERS)]
    for chunker in chunkers:
        chunker.start()
    return chunkers


def start_vectorizers():
    vectorizers = [Vectorizer(id=f"vectorizer-{i}", pinecone_index_name="my-first-index",
                              input_queue=vectorizing_queue) for i in range(NUM_CHUNKERS)]
    for v in vectorizers:
        v.start()
    return vectorizers


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


if __name__ == "__main__":

    timer = Timer()
    # initialize queues
    chunking_queue = Queue()
    vectorizing_queue = Queue()

    # start workers
    chunkers = start_chunkers()
    vectorizers = start_vectorizers()

    # run pipeline
    try:
        if os.path.isdir(INPUT_PATH):
            directory_path = Path(INPUT_PATH)

            for i, item in enumerate(directory_path.iterdir()):
                if i >= NUM_FILES:
                    break
                if item.is_file():
                    file_path = item
                    path_str = str(file_path)
                    isTextFile(path_str)
                    parseTask = ParseTask(path_str)
                    chunking_queue.put(parseTask)

        elif os.path.isfile(INPUT_PATH):
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
