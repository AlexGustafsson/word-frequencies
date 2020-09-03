import logging
import json
from argparse import ArgumentParser
from os import makedirs, path, listdir
from typing import List, Any, Dict
from sys import stdout
from multiprocessing.pool import ThreadPool
from itertools import chain

from scripts.wikipedia import fetch_from_wikipedia, fetch_top_viewed_articles
from scripts.clean import clean, extract_words
from scripts.compilation import count

# TODO: handle t.ex, etc. o.s.v.

# Configure the default logging format
logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)-5s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Configure a thread pool
pool = ThreadPool(processes=4)

def store(output_directory: str, filename: str, content: str) -> None:
    """Store a file in the output directory."""
    with open(path.join(output_directory, filename), "w") as file:
        file.write(content)

def load(output_directory: str, filename: str) -> str:
    """Load a file from the output directory."""
    with open(path.join(output_directory, filename), "r") as file:
        return file.read()

def load_bucket(output_directory: str, bucket: List[str]) -> List[str]:
    """Load a bucket of files."""
    files = []
    for filename in bucket:
        files.append(load(output_directory, filename))
    return files

def load_all(output_directory) -> List[str]:
    """Load all files from an output directory."""
    filenames = listdir(output_directory)

    buckets = chunks(filenames, 10)
    logger.info("Loading files in %d threads", len(buckets))
    futures = [pool.apply_async(load_bucket, (output_directory, bucket)) for bucket in buckets]
    results = [future.get() for future in futures]

    return list(chain.from_iterable(results))


def exists(output_directory: str, filename: str) -> bool:
    """Whether or not a file exists in the output directory."""
    return path.exists(path.join(output_directory, filename))


def chunks(items: Any, chunk_size: int) -> List[List[Any]]:
    """Format a list to evenly sized chunks"""
    size = round(len(items) / chunk_size)
    return [items[i:i + size] for i in range(0, len(items), size)]


def download_bucket(output_directory: str, language: str, bucket: List[str]) -> None:
    """Download a bucket of articles."""
    for article in bucket:
        filename = "{}.txt".format(article.replace("/", "_"))
        if exists(output_directory, filename):
            logger.info("Article %s is already downloaded", article)
        else:
            logger.info("Fetching article %s", article)
            content = fetch_from_wikipedia(article, language)
            logger.info("Caching article %s", article)
            store(output_directory, filename, content)


def download(output_directory: str, language: str) -> None:
    """Download articles for the language."""
    logger.info("Fetching top articles for language %s", language)
    top_articles = fetch_top_viewed_articles(language)

    buckets = chunks(top_articles, 10)
    logger.info("Downloading in %d threads", len(buckets))
    futures = [pool.apply_async(download_bucket, (output_directory, language, bucket)) for bucket in buckets]
    [future.wait() for future in futures]


def compile_frequency_bucket(bucket: List[str]) -> Dict[str, int]:
    """Compile a bucket."""
    logger.info("Compiling %d articles in bucket", len(bucket))
    compiled = "\n".join(bucket)
    logger.info("Cleaning bucket")
    compiled = clean(compiled)
    logger.info("Extracting words from bucket")
    words = extract_words(compiled)
    logger.info("Counting %d words in bucket", len(words))
    counted_words = count(words)
    return counted_words

def compile_frequency(output_directory: str, language: str) -> None:
    """Compile a frequency list for the language."""
    # Download all articles if they don't exist
    download(output_directory, language)

    logger.info("Loading all articles")
    articles = load_all(output_directory)

    buckets = chunks(articles, 10)
    logger.info("Performing cleaning and counting in %d threads", len(buckets))
    futures = [pool.apply_async(compile_bucket, (bucket,)) for bucket in buckets]
    results = [future.get() for future in futures]

    logger.info("Summing results")
    counted_words = {}
    for result in results:
        for word, count in result.items():
            if word not in counted_words:
                counted_words[word] = 0
            counted_words[word] = counted_words[word] + count

    logger.info("Sorting results")
    counted_words = {word: count for word, count in sorted(counted_words.items(), key=lambda item: item[1], reverse=True)}

    logger.info("Processed %d articles with %d words", len(articles), len(counted_words))

    # Print it as JSON to stdout
    json.dump(counted_words, stdout)


def compile_text(output_directory: str, language: str) -> None:
    """Compile a large text file for the language."""
    # Download all articles if they don't exist
    download(output_directory, language)

    logger.info("Loading all articles")
    articles = load_all(output_directory)

    compiled = "\n".join(articles)

    print(compiled)

def main() -> None:
    """Main entrypoint."""
    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="A tool to compile a collection of words and frequencies")

    # Add parameters for the server connection
    parser.add_argument("-l", "--language", required=True, type=str, help="The two letter language code for which to compile")
    # Add optional parameters for the server connection
    parser.add_argument("-c", "--cache", type=str, default="./frequency-data", required=False, help="The cache directory to use")
    # Add a command parameter
    parser.add_argument("command", type=str, choices=["download", "compile-frequency", "compile-text"], help="Command to execute")

    # Parse the arguments
    options = parser.parse_args()

    # Create a directory for the language as needed
    output_directory = path.join(options.cache, options.language)
    if not path.exists(output_directory):
        makedirs(output_directory)

    if options.command == "download":
        download(output_directory, options.language)
    elif options.command == "compile-frequency":
        compile_frequency(output_directory, options.language)
    elif options.command == "compile-text":
        compile_text(output_directory, options.language)

if __name__ == '__main__':
    main()
