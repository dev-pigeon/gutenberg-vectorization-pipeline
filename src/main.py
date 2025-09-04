import argparse
import os
import sys
from util import isTextFile
from task import ParseTask
from pathlib import Path
from chunker import Chunker
from vectorizer import Vectorizer
from timer import Timer
from multiprocessing import Queue, Process

parser = argparse.ArgumentParser(
    description="A CLI tool to vectorize text files.")

parser.add_argument('-i', '--input', required=True,
                    help='The global path to the text file or directory to vectorize.')
parser.add_argument('--chroma-db', required=True,
                    help='The global path pointing to your local persistent ChromaDB instance or the location where you would like one to be created')
parser.add_argument('-cn', '--collection-name', required=True,
                    help='The name of the ChromaDB collection where the records will be stored.')

args = parser.parse_args()

INPUT_PATH = args.input
CHROMA_PATH = args.chroma_db
COLLECTION_NAME = args.collection_name

# ensure that chroma_path is valid
if not os.path.isdir(CHROMA_PATH):
    sys.exit(
        f"ERROR: The path: {CHROMA_PATH} does not exist or is not a valid directory. Please try again with a valid and existing directory path for ChromaDB")


def cleanup():
    chunking_queue.put(None)
    chunker.join()


if __name__ == "__main__":

    # initialize variables
    chunking_queue = Queue()
    chunker = Chunker(chunking_queue)
    chunker.start()
    vectorizer = Vectorizer(chroma_path=CHROMA_PATH,
                            collection_name=COLLECTION_NAME)
    timer = Timer()

    # run pipeline
    try:
        if os.path.isdir(INPUT_PATH):
            directory_path = Path(INPUT_PATH)
            timer.start()

            for item in directory_path.iterdir():
                if item.is_file():
                    file_path = item
                    path_str = str(file_path)
                    isTextFile(path_str)
                    parseTask = ParseTask(path_str)
                    chunking_queue.put(parseTask)
                    # vectorizer.embed_and_insert_chunks(chunker.chunks)

        elif os.path.isfile(INPUT_PATH):
            timer.start()
            isTextFile(INPUT_PATH)
            parseTask = ParseTask(INPUT_PATH)
            chunking_queue.put(parseTask)
            # print("embedding file chunks...")
            # vectorizer.embed_and_insert_chunks(chunker.chunks)

        else:
            sys.exit(
                "ERROR: The input path provided does not exist. Please try again and enter a valid path.")
    except ValueError as e:
        print(e)

    # cleanup
    cleanup()
    time_elapsed = timer.get_time_elapsed()
    print(f"Finished processing in {time_elapsed}")
