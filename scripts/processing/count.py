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


def count(output_directory: str, language: str) -> None:
    """Count words in sources for the language."""
    # Get cleaned files
    compiled = load(output_directory, "compiled/{}/compiled.txt".format(language))
    words = " ".join(compiled.split("\n")).split(" ")

    logger.info("Counting %d words", len(words))

    word_count = {}
    character_count = {}
    for word in words:
        for character in word:
            if character not in character_count:
                character_count[character] = 0
            character_count[character] += 1
        if word not in word_count:
            word_count[word] = 0
        word_count[word] += 1
    sorted_word_count = {k: v for k, v in sorted(word_count.items(), key=lambda item: item[1], reverse=True)}
    sorted_character_count = {k: v for k, v in sorted(character_count.items(), key=lambda item: item[1], reverse=True)}

    logger.info("Completed all jobs, storing compilation")
    store(output_directory, "./compiled/{}/word-frequencies.json".format(language), json.dumps(sorted_word_count, indent=2))
    store(output_directory, "./compiled/{}/character-frequencies.json".format(language), json.dumps(sorted_character_count, indent=2))


def main() -> None:
    """Main entrypoint."""
    global executor

    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="A tool to count the frequency of words and characters in large collections of textual content")
    parser.add_argument("-l", "--language", required=True, type=str, help="The two letter language code for the language to clean")
    parser.add_argument("-c", "--cache", type=str, default="./frequency-data", required=False, help="The cache directory to use")

    # Parse the arguments
    options = parser.parse_args()

    # Create a directory for the language as needed
    output_directory = options.cache
    if not path.exists(output_directory):
        makedirs(output_directory)

    count(output_directory, options.language)


if __name__ == '__main__':
    main()
