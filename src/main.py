import argparse
import os
from util import isTextFile

parser = argparse.ArgumentParser(
    description="A CLI tool to vectorize text files.")

parser.add_argument('-i', '--input', required=True,
                    help='The global path to the text file or directory to vectorize.')
parser.add_argument('-o', '--output', required=True,
                    help='The global path where the intermediary cleaned data will be stored for fast future vectorizations.')
parser.add_argument('--chroma-db', required=True,
                    help='The global path pointing to your local persistent ChromaDB instance or the location where you would like one to be created')

args = parser.parse_args()

INPUT_PATH = args.input
OUTPUT_PATH = args.output
CHROMA_PATH = args.chroma_db


# Check if input path is a directory
if os.path.isdir(INPUT_PATH):
    # go to the directory
    # loop each file
    # check is text
    # pass to the parser
    # parser will put the vectorization tasks into a queue
    # while that isn't empty -> vectorize and store the intermediary chunks
    pass
else:
    # pass into parser as a task
    # parser will put the vectorization tasks into a queue
    # while that isn't empty -> vectorize and store the intermediary chunks
    pass

# Begin vectorization pipeline
print(isTextFile(INPUT_PATH))
