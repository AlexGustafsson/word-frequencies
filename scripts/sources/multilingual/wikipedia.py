import json
import re
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime

heading_pattern = re.compile(r"=+ *[^=]+ *=+")
newline_pattern = re.compile(r"\n")

def fetch_wikipedia_article(query: str, language: str) -> str:
    """Fetch a plain-text article from Wikipedia."""
    url = "https://{}.wikipedia.org/w/api.php?{}".format(language, urlencode({
        "action": "query",
        "prop": "extracts",
        "rvprop": "content",
        "explaintext": True,
        "format": "json",
        "titles": query}))
    file = urlopen(url)
    body = json.loads(file.read())
    return list(body["query"]["pages"].values())[0]["extract"]

def fetch_top_wikipedia_articles(language: str) -> str:
    """Fetch the top viewed articles for a language."""
    now = datetime.now()
    month = 12 if now.month == 1 else now.month - 1
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{0}.wikipedia.org/all-access/{1}/{2:02}/all-days".format(language, now.year, month)
    file = urlopen(url)
    body = json.loads(file.read())
    return [article["article"] for article in body["items"][0]["articles"] if not ":" in article["article"]]

def clean_wikipedia_article(body: str) -> str:
    """Clean a Wikipedia article. Removes headings."""
    body = heading_pattern.sub("", body)
    # Lists do not end with a period, but a newline. By doing this
    # we force list items to be treated as sentences
    body = newline_pattern.sub("\n.", body)
    return body
