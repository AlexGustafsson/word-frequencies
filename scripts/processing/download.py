import logging
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List, Tuple
from os import path

from scripts.sources.multilingual.wikipedia import fetch_top_wikipedia_articles, fetch_wikipedia_article
from scripts.sources.multilingual.gutenberg import fetch_available_gutenberg_books, fetch_gutenberg_book
from scripts.sources.multilingual.wiktionary import fetch_wiktionary_dump
from scripts.processing.lib.utils import chunks, store, exists

# Configure the default logging format
logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)-5s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Configure a future executor
executor = None


def download_bucket(output_directory: str, language: str, bucket: List[Tuple[str, Any]]) -> None:
    """Download a bucket of sources."""
    logger.info("Downloading bucket size=%d", len(bucket))
    for source, parameter in bucket:
        filename = ""
        if source == "wikipedia":
            filename = "wikipedia/{}.txt".format(parameter.replace("/", "_"))
        elif source == "gutenberg":
            filename = "gutenberg/{}.txt".format(parameter[0].replace("/", "_"))
        elif source == "wiktionary":
            filename = "wiktionary/dump.xml"

        if exists(output_directory, "downloads/{}/{}".format(language, filename)):
            logger.info("Skipping download source=%s filename=%s", source, filename)
        else:
            content = ""
            try:
                if source == "wikipedia":
                    logger.info("Downloading source=Wikipedia article=%s", parameter)
                    content = fetch_wikipedia_article(parameter, language)
                elif source == "gutenberg":
                    logger.info("Fetching source=Gutenberg book='%s' id=%s", parameter[1], parameter[0])
                    content = fetch_gutenberg_book(parameter[0])
                elif source == "wiktionary":
                    logger.info("Fetching dump source=Wiktionary")
                    content = fetch_wiktionary_dump(language)
                logger.info("Storing source=%s filename=%s", source, filename)
                store(output_directory, "downloads/{}/{}".format(language, filename), content)
            except:
                logger.error("Unable to download source=%s filename=%s", source, filename, exc_info=True)


def download(output_directory: str, language: str) -> None:
    """Download sources for the language."""
    logger.info("Fetching top Wikipedia articles language=%s", language)
    top_articles = [("wikipedia", x) for x in fetch_top_wikipedia_articles(language)]
    logger.info("Fetching available Gutenberg books language=%s", language)
    gutenberg_books = [("gutenberg", x) for x in fetch_available_gutenberg_books(language)]

    fetches = top_articles + [("wiktionary", None)]

    buckets = chunks(fetches, min(10, len(fetches)))
    logger.info("Downloading threads=%d", len(buckets))
    futures = {executor.submit(download_bucket, output_directory, language, bucket) for bucket in buckets}
    for future in futures:
        future.result()
    logger.info("Completed all jobs")


def main() -> None:
    """Main entrypoint."""
    global executor

    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="A threaded tool to download large collections of textual content")
    parser.add_argument("-l", "--language", required=True, type=str, help="The two letter language code for which to download data")
    parser.add_argument("-c", "--cache", type=str, default="./frequency-data", required=False, help="The cache directory to use")

    # Parse the arguments
    options = parser.parse_args()

    # Create a directory for the language as needed
    output_directory = options.cache
    if not path.exists(output_directory):
        makedirs(output_directory)

    executor = ThreadPoolExecutor(max_workers=5)
    download(output_directory, options.language)


if __name__ == '__main__':
    main()
