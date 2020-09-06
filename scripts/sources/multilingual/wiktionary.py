import re
import bz2
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from urllib.parse import urlencode
from typing import List


page_pattern = re.compile(r'<></text>')
heading_pattern = re.compile(r"=+ *[^=]+ *=+")
translation_pattern = re.compile(r"\*[^:]+: ?(\{\{[^}]+}}(, ?)?)+")


def fetch_wiktionary_dump(language: str) -> str:
    """Download a wiktionary dump."""
    url = "https://dumps.wikimedia.org/{0}wiktionary/latest/{0}wiktionary-latest-pages-articles.xml.bz2".format(language)
    file = urlopen(url)
    with bz2.open(file, "rt") as deflated_file:
        return deflated_file.read()


def extract_wiktionary_articles(dump: str) -> List[str]:
    """Extract wiktionary articles."""
    tree = ET.fromstring(dump)
    root = tree.getroot()
    for page in root.findall("page"):
        title = page.find("title")
        if title is None or ":" in title.texr:
            continue
        title = title.text

        article = "{}\n".format(title)
        print(article)


def clean_wiktionary_article(article: str) -> str:
    """Clean a wiktionary article."""
    # Remove headings
    article = heading_pattern.sub("", article)
    # Remove translations
    article = translation_pattern.sub("", article)
    return article
