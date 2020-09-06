import re
from typing import List

# Requires requests:
# python3 -m pip install requests
import requests


book_pattern = re.compile(r'<a ?href="/ebooks/([0-9]+)">([^<]+)</a>')
header_pattern = re.compile(r".*\*\*\* ?START OF.*")
footer_pattern_1 = re.compile(r"\*\*\* ?END OF.*")
footer_pattern_2 = re.compile(r"\*\*\* ?START: FULL LICENSE.*")
newline_pattern = re.compile(r"\n")


def fetch_available_gutenberg_books(language: str) -> List[str]:
    """Fetch available books from Gutenberg for the given two-letter language code."""
    url = "https://www.gutenberg.org/browse/languages/{}".format(language)
    body = {
        "lang": "language",
        "filetype": "txt.utf-8"
    }
    response = requests.post(url, files=body)
    response.raise_for_status()

    # Extract a list of tuples for each book with the id and name
    books = book_pattern.findall(response.text)
    return books


def fetch_gutenberg_book(id: str) -> str:
    """Fetch a book from Gutenberg, given its ebook id."""
    url = "https://www.gutenberg.org/ebooks/{}.txt.utf-8".format(id)
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def clean_gutenberg_book(body: str) -> str:
    """Clean a book from Gutenberg. Removes header and footer."""
    # Remove the Gutenberg header
    body = header_pattern.split(body)[1]

    # Remove the Gutenberg footer
    body = footer_pattern_1.split(body)[0]
    body = footer_pattern_2.split(body)[0]

    # The texts are line broken just like in textbooks
    # Removing all newlines forces most line breaking to be undone
    body = newline_pattern.sub(" ", body)

    return body
