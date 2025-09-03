import argparse
import os
import sys
from util import isTextFile
from task import ParseTask
from pathlib import Path
from chunker import Chunker
from vectorizer import Vectorizer

parser = argparse.ArgumentParser(
    description="A CLI tool to vectorize text files.")

parser.add_argument('-i', '--input', required=True,
                    help='The global path to the text file or directory to vectorize.')
parser.add_argument('--chroma-db', required=True,
                    help='The global path pointing to your local persistent ChromaDB instance or the location where you would like one to be created')

args = parser.parse_args()

INPUT_PATH = args.input
CHROMA_PATH = args.chroma_db
chunker = Chunker()

# ensure that chroma_path is valid
if not os.path.isdir(CHROMA_PATH):
    sys.exit(
        f"ERROR: The path: {CHROMA_PATH} does not exist or is not a valid directory. Please try again with a valid and existing directory path for ChromaDB")


# Check if input path is a directory
try:
    if os.path.isdir(INPUT_PATH):
        print("Directory")
        directory_path = Path(INPUT_PATH)
        for item in directory_path.iterdir():
            if item.is_file():
                file_path = item
                path_str = str(file_path)
                isTextFile(path_str)
                parseTask = ParseTask(path_str)
                chunker.chunk_file(parseTask)

    elif os.path.isfile(INPUT_PATH):
        isTextFile(INPUT_PATH)
        parseTask = ParseTask(INPUT_PATH)
        chunker.chunk_file(parseTask)

    else:
        sys.exit(
            "ERROR: The input path provided does not exist. Please try again and enter a valid path.")
except ValueError as e:
    print(e)
