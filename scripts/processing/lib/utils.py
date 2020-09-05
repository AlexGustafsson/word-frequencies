import logging
from typing import Any, List, Tuple
from multiprocessing.pool import ThreadPool
from os import makedirs, path, listdir

logger = logging.getLogger(__name__)


def assert_file(output_directory: str, filename: str) -> None:
    """Create the path to a file if it does not exist."""
    parent_directory = path.join(output_directory, path.dirname(filename))
    if not path.exists(parent_directory):
        makedirs(parent_directory)


def store(output_directory: str, filename: str, content: str) -> None:
    """Store a file in the output directory. Creates the path as needed."""
    assert_file(output_directory, filename)
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


def find_files(output_directory: str) -> List[Tuple[str, str]]:
    """Find files from the output directory by sub directory."""
    directories = listdir(output_directory)
    return [(directory, x) for directory in directories for x in listdir(path.join(output_directory, directory))]


def exists(output_directory: str, filename: str) -> bool:
    """Whether or not a file exists in the output directory."""
    return path.exists(path.join(output_directory, filename))


def chunks(items: Any, chunk_size: int) -> List[List[Any]]:
    """Format a list to evenly sized chunks"""
    size = round(len(items) / chunk_size)
    return [items[i:i + size] for i in range(0, len(items), size)]
