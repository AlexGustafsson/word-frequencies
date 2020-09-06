import logging
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List, Tuple
from os import path, makedirs

from scripts.processing.lib.utils import find_files, chunks, exists, load, store
from scripts.processing.lib.clean import clean_text
from scripts.sources.multilingual.gutenberg import clean_gutenberg_book
from scripts.sources.multilingual.wikipedia import clean_wikipedia_article

# Configure the default logging format
logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)-5s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Configure a future executor
executor = None


def clean_bucket(output_directory: str, language: str, bucket: List[Tuple[str, Any]]) -> None:
    """Clean a bucket of sources."""
    logger.info("Cleaning bucket size=%d", len(bucket))
    prepared_content = []
    for source, parameter in bucket:
        filename = parameter
        input = "downloads/{}/{}/{}".format(language, source, parameter)
        output = "clean/{}/{}/{}".format(language, source, parameter)

        if exists(output_directory, output):
            logger.info("Skipping cleaned source=%s filename=%s", source, filename)
        else:
            try:
                content = load(output_directory, input)
                if source == "wikipedia":
                    logger.info("Cleaning with special handler source=Wikipedia filename=%s", filename)
                    content = clean_wikipedia_article(content)
                elif source == "gutenberg":
                    logger.info("Cleaning with special handler source=Gutenberg filename=%s", filename)
                    content = clean_gutenberg_book(content)

                logger.info("Cleaning using generic cleaner filename=%s size=%d", filename, len(content))
                content = clean_text(content)

                logger.info("Storing source=%s filename=%s", source, filename)
                store(output_directory, output, content)
            except:
                logger.error("Unable to load and clean source=%s filename=%s", source, filename, exc_info=True)


def clean(output_directory: str, language: str) -> None:
    """Clean sources for the language."""
    # Get downloaded files
    files = find_files(path.join(output_directory, "./downloads/{}".format(language)))

    buckets = chunks(files, min(10, len(files)))
    logger.info("Cleaning threads=%d", len(buckets))
    futures = {executor.submit(clean_bucket, output_directory, language, bucket) for bucket in buckets}
    for future in futures:
        future.result()
    logger.info("Completed all jobs")


def main() -> None:
    """Main entrypoint."""
    global executor

    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="A threaded tool to clean large collections of textual content")
    parser.add_argument("-l", "--language", required=True, type=str, help="The two letter language code for the language to clean")
    parser.add_argument("-c", "--cache", type=str, default="./frequency-data", required=False, help="The cache directory to use")

    # Parse the arguments
    options = parser.parse_args()

    # Create a directory for the language as needed
    output_directory = options.cache
    if not path.exists(output_directory):
        makedirs(output_directory)

    executor = ThreadPoolExecutor(max_workers=5)
    clean(output_directory, options.language)


if __name__ == '__main__':
    main()
