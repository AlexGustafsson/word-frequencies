import logging
import json
from argparse import ArgumentParser
from typing import Any, List, Tuple
from os import path, makedirs

from scripts.processing.lib.utils import load, store

# Configure the default logging format
logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)-5s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


def create_ngrams(output_directory: str, language: str, n: int) -> None:
    """Count words in sources for the language."""
    # Get cleaned files
    compiled = load(output_directory, "compiled/{}/compiled.txt".format(language))
    sentences = compiled.split("\n")

    logger.info("Creating %d-grams of  %d sentences", n, len(sentences))

    compiled_grams = set()
    for sentence in sentences:
        sentence = sentence.split(" ")
        grams = [sentence[i:i + n] for i in range(0, len(sentence), n)]
        for gram in grams:
            compiled_grams.add(" ".join(gram))

    logger.info("Completed all jobs, storing compiled %d-grams", n)
    store(output_directory, "compiled/{}/{}-grams.txt".format(language, n), "\n".join(compiled_grams))


def main() -> None:
    """Main entrypoint."""
    global executor

    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="A threaded tool to create n-grams of words in large collections of textual content")
    parser.add_argument("-l", "--language", required=True, type=str, help="The two letter language code for the language to clean")
    parser.add_argument("-c", "--cache", type=str, default="./frequency-data", required=False, help="The cache directory to use")
    parser.add_argument("-n", type=int, default=3, required=False, help="The number of words to use for each sequence")

    # Parse the arguments
    options = parser.parse_args()

    # Create a directory for the language as needed
    output_directory = options.cache
    if not path.exists(output_directory):
        makedirs(output_directory)

    create_ngrams(output_directory, options.language, options.n)


if __name__ == '__main__':
    main()
