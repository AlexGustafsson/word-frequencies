import re
import json
from typing import List, Tuple

# Requires requests:
# python3 -m pip install requests
import requests

# å
accent_pattern_1 = re.compile(r"ã¥")
# ä
accent_pattern_2 = re.compile(r"ã¤")
# ö
accent_pattern_3 = re.compile(r"ã¶")

# ß -> s
germanization_pattern_1 = re.compile(r"ß")

# Characters from the Ancient Greek unicode block
ancient_greek_pattern = re.compile(r"[\u0370\u0371\u0372\u0373\u0374\u0375\u0376\u0377\u037a\u037b\u037c\u037d\u037e\u037f\u0384\u0385\u0386\u0387\u0388\u0389\u038a\u038c\u038e\u038f\u0390\u0391\u0392\u0393\u0394\u0395\u0396\u0397\u0398\u0399\u039a\u039b\u039c\u039d\u039e\u039f\u03a0\u03a1\u03a3\u03a4\u03a5\u03a6\u03a7\u03a8\u03a9\u03aa\u03ab\u03ac\u03ad\u03ae\u03af\u03b0\u03b1\u03b2\u03b3\u03b4\u03b5\u03b6\u03b7\u03b8\u03b9\u03ba\u03bb\u03bc\u03bd\u03be\u03bf\u03c0\u03c1\u03c2\u03c3\u03c4\u03c5\u03c6\u03c7\u03c8\u03c9\u03ca\u03cb\u03cc\u03cd\u03ce\u03cf\u03d0\u03d1\u03d2\u03d3\u03d4\u03d5\u03d6\u03d7\u03d8\u03d9\u03da\u03db\u03dc\u03dd\u03de\u03df\u03e0\u03e1\u03e2\u03e3\u03e4\u03e5\u03e6\u03e7\u03e8\u03e9\u03ea\u03eb\u03ec\u03ed\u03ee\u03ef\u03f0\u03f1\u03f2\u03f3\u03f4\u03f5\u03f6\u03f7\u03f8\u03f9\u03fa\u03fb\u03fc\u03fd\u03fe\u03ff]")

# Characters from the Cyrillic unicode block
cyrillic_pattern = re.compile(r"[\u0400\u0401\u0402\u0403\u0404\u0405\u0406\u0407\u0408\u0409\u040a\u040b\u040c\u040d\u040e\u040f\u0410\u0411\u0412\u0413\u0414\u0415\u0416\u0417\u0418\u0419\u041a\u041b\u041c\u041d\u041e\u041f\u0420\u0421\u0422\u0423\u0424\u0425\u0426\u0427\u0428\u0429\u042a\u042b\u042c\u042d\u042e\u042f\u0430\u0431\u0432\u0433\u0434\u0435\u0436\u0437\u0438\u0439\u043a\u043b\u043c\u043d\u043e\u043f\u0440\u0441\u0442\u0443\u0444\u0445\u0446\u0447\u0448\u0449\u044a\u044b\u044c\u044d\u044e\u044f\u0450\u0451\u0452\u0453\u0454\u0455\u0456\u0457\u0458\u0459\u045a\u045b\u045c\u045d\u045e\u045f\u0460\u0461\u0462\u0463\u0464\u0465\u0466\u0467\u0468\u0469\u046a\u046b\u046c\u046d\u046e\u046f\u0470\u0471\u0472\u0473\u0474\u0475\u0476\u0477\u0478\u0479\u047a\u047b\u047c\u047d\u047e\u047f\u0480\u0481\u0482\u0483\u0484\u0485\u0486\u0487\u0488\u0489\u048a\u048b\u048c\u048d\u048e\u048f\u0490\u0491\u0492\u0493\u0494\u0495\u0496\u0497\u0498\u0499\u049a\u049b\u049c\u049d\u049e\u049f\u04a0\u04a1\u04a2\u04a3\u04a4\u04a5\u04a6\u04a7\u04a8\u04a9\u04aa\u04ab\u04ac\u04ad\u04ae\u04af\u04b0\u04b1\u04b2\u04b3\u04b4\u04b5\u04b6\u04b7\u04b8\u04b9\u04ba\u04bb\u04bc\u04bd\u04be\u04bf\u04c0\u04c1\u04c2\u04c3\u04c4\u04c5\u04c6\u04c7\u04c8\u04c9\u04ca\u04cb\u04cc\u04cd\u04ce\u04cf\u04d0\u04d1\u04d2\u04d3\u04d4\u04d5\u04d6\u04d7\u04d8\u04d9\u04da\u04db\u04dc\u04dd\u04de\u04df\u04e0\u04e1\u04e2\u04e3\u04e4\u04e5\u04e6\u04e7\u04e8\u04e9\u04ea\u04eb\u04ec\u04ed\u04ee\u04ef\u04f0\u04f1\u04f2\u04f3\u04f4\u04f5\u04f6\u04f7\u04f8\u04f9\u04fa\u04fb\u04fc\u04fd\u04fe\u04ff]")

# Blacklisted books that are incorrectly reported as being Swedish
blacklist = [
    "LB_StrindbergA_LegenderSvenskText_2001_etext.txt",
    "LB_StrindbergA_EnDåresFörsvarstalSv_1999_etext.txt",
    "LB_BrennerSE_PoetiskeDikter1_1713_etext.txt"
]


def fetch_available_litteraturbanken_books() -> List[Tuple[str, str]]:
    """Fetch available books from Litteraturbanken."""
    url = "https://litteraturbanken.se/api/list_all/etext?exclude=text,parts,sourcedesc,pages,errata&filter_and=%7B%22sort_date_imprint.date:range%22:%221248,2020%22,%22export%3Etype%22:%5B%22xml%22,%22txt%22,%22workdb%22%5D%7D&filter_or=%7B%7D&filter_string=&from=0&include=lbworkid,titlepath,title,titleid,work_titleid,shorttitle,mediatype,searchable,imported,sortfield,sort_date_imprint.plain,main_author.authorid,main_author.surname,main_author.type,work_authors.authorid,work_authors.surname,startpagename,has_epub,sort_date.plain,export&partial_string=true&sort_field=popularity%7Cdesc&suggest=true&to=1000"
    response = requests.get(url)
    response.raise_for_status()

    response = json.loads(response.text)

    books = []
    for book in response["data"]:
        has_text = False
        for export in book["export"]:
            if export["type"] == "txt":
                has_text = True
                break
        if not has_text:
            continue

        filename = "LB_{}_{}_{}_etext.txt".format(book["main_author"]["authorid"], book["titleid"], book["sort_date_imprint"]["plain"])
        if filename in blacklist:
            continue
        books.append((filename, book["lbworkid"]))

    return books


def fetch_litteraturbanken_books(books: List[Tuple[str, str]]) -> str:
    """Fetch books from Litteraturbanken given their ids."""
    url = "https://litteraturbanken.se/api/download"
    body = {
        "files": ["{}-etext-txt".format(id) for filename, id in books]
    }
    response = requests.post(url, data=body)
    response.raise_for_status()
    return response.text


def clean_litteraturbanken_book(book: str) -> str:
    """Clean a book fetched from Litteraturbanken."""
    # Remove the header
    book = book.split("--------------------------------------------------------------------------------")[1]

    book = accent_pattern_1.sub("å", book)
    book = accent_pattern_2.sub("ä", book)
    book = accent_pattern_3.sub("ö", book)
    book = germanization_pattern_1.sub("ss", book)
    book = ancient_greek_pattern.sub("", book)
    book = cyrillic_pattern.sub("", book)

    return book
