import argparse
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

# Begin vectorization pipeline
print(isTextFile(INPUT_PATH))
