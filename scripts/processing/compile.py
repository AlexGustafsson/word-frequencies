import logging
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List, Tuple
from os import path, makedirs

from scripts.processing.lib.utils import find_files, chunks, load, store

# Configure the default logging format
logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)-5s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Configure a future executor
executor = None


def compile_bucket(output_directory: str, language: str, bucket: List[Tuple[str, Any]]) -> None:
    """Compile a bucket of sources."""
    logger.info("Compiling bucket size=%d", len(bucket))
    compiled = ""
    for source, parameter in bucket:
        filename = parameter
        input = "clean/{}/{}/{}".format(language, source, parameter)

        try:
            compiled += "\n" + load(output_directory, input)
        except:
            logger.error("Unable to load and compile source=%s filename=%s", source, filename, exc_info=True)
    return compiled


def compile(output_directory: str, language: str) -> None:
    """Compile sources for the language."""
    # Get cleaned files
    files = find_files(path.join(output_directory, "./clean/{}".format(language)))

    buckets = chunks(files, min(10, len(files)))
    logger.info("Cleaning threads=%d", len(buckets))
    futures = {executor.submit(compile_bucket, output_directory, language, bucket) for bucket in buckets}
    compiled = ""
    for future in futures:
        compiled += future.result() + "\n"
    logger.info("Completed all jobs, storing compilation")
    store(output_directory, "./compiled/{}/compiled.txt".format(language), compiled)


def main() -> None:
    """Main entrypoint."""
    global executor

    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="A threaded tool to compile large collections of textual content")
    parser.add_argument("-l", "--language", required=True, type=str, help="The two letter language code for the language to clean")
    parser.add_argument("-c", "--cache", type=str, default="./frequency-data", required=False, help="The cache directory to use")

    # Parse the arguments
    options = parser.parse_args()

    # Create a directory for the language as needed
    output_directory = options.cache
    if not path.exists(output_directory):
        makedirs(output_directory)

    executor = ThreadPoolExecutor(max_workers=5)
    compile(output_directory, options.language)


if __name__ == '__main__':
    main()
