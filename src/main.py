import argparse
import os
import sys
from util import isTextFile
from task import ParseTask
from pathlib import Path

parser = argparse.ArgumentParser(
    description="A CLI tool to vectorize text files.")

parser.add_argument('-i', '--input', required=True,
                    help='The global path to the text file or directory to vectorize.')
parser.add_argument('-o', '--output', required=True,
                    help='The global path where the intermediary cleaned data will be stored for fast future vectorizations. Must either point to a an existing directory or a .json file.')
parser.add_argument('--chroma-db', required=True,
                    help='The global path pointing to your local persistent ChromaDB instance or the location where you would like one to be created')

args = parser.parse_args()

INPUT_PATH = args.input
OUTPUT_PATH = args.output
CHROMA_PATH = args.chroma_db

# Check if input path is a directory

try:
    if os.path.isdir(INPUT_PATH):
        print("Directory")
        directory_path = Path(INPUT_PATH)
        for item in directory_path.iterdir():
            if item.is_file():
                file_path = item
                print(f"Verifying that {file_path} is a text file")
                isTextFile(str(file_path))
                parseTask = ParseTask(INPUT_PATH, OUTPUT_PATH)
                # push the parseTask into Redis

        pass
    elif os.path.isfile(INPUT_PATH):
        print("File")
        isTextFile(INPUT_PATH)
        parseTask = ParseTask(INPUT_PATH, OUTPUT_PATH)
        # push the parseTask into Redis

        pass
    else:
        sys.exit(
            "ERROR: The input path provided does not exist. Please try again and enter a valid path.")
except ValueError as e:
    sys.exit(str(e))
