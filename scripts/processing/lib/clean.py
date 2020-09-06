import re
from typing import List, Set



digit_pattern = re.compile(r"\b\d+\b")
possessive_pattern = re.compile(r"([a-z])'s")
punctuation_pattern = re.compile(r"[!?.]")
special_pattern = re.compile(r"[\\!\"#$%&'()*+,./:;<=>?@[\]^_{|}~)°→©²§½×ʃ•¾⊙°\u2020\u2030\u00b3\u00b9‿✯¼√═\u0333º⎫⎬⎭|\u2460-\u325aᚠ™]")
hyphen_pattern = re.compile(r"\B-\B|\b-\B|\B-\b")
whitespace_pattern = re.compile(r"\s+")
newline_pattern = re.compile(r"\n+")
padding_pattern = re.compile(r"^\s+|\s+$", flags=re.MULTILINE)
website_pattern = re.compile(r"(https?:\/\/)?([a-z0-9-]+\.)+[a-z]{2,}(\/[a-z0-9%&?=#\.-]+)*")
single_character_line_pattern = re.compile(r"^.$", flags=re.MULTILINE)
math_pattern = re.compile(r"\{[A-Za-z0-9\\ _^+\-*\{\}]+\}")

unicode_hyphen_pattern = re.compile(r"[\u2014\u2013\u2012\u2010\u2043\ufe63\uff0d\u058a\u1806\u2014\u2010\u00ad\u2010\u2013\u2014\u2043\u2212]")
unicode_single_quote_pattern = re.compile(r"[\u2039\u203a\u2019\u276e\u276f\u201a\u2018\u201b\u275b\u275c\u275f\u00b4\u02c8\u02cc\u02bb`\u2032]")
unicode_double_quote_pattern = re.compile(r"[\u00ab\u00ab\u201e\u201c\u201f\u201d\u0022\u275d\u275e\u2e42\u301d\u301e\u301f\uff02\u00bb\u2033]")
unicode_period_pattern = re.compile(r"[\u002e\u0589\u3002\u06d4\u2cf9\u0701\u1362\u166e\u1803\u2cfe\ua4ff\ua60e\ua6f3\u002e\u002e]")
unicode_exclamation_pattern = re.compile(r"[\u2048\u2757\u203c\u0021\u00a1\u07f9\u1944\u0021\u0021\u00a1]")
unicode_comma_pattern = re.compile(r"[\u002c\u060c\u3001\u055d\u07f8\u1363\u1808\ua4fe\ua60d\ua6f5\u002c\u002c]")
unicode_question_pattern = re.compile(r"[\u2047\u2049\u003f\u037e\u00bf\u061f\u055e\u1367\u2cfa\u2cfb\ua60f\ua6f7\ud804\u003f\u003f\u00bf]")
unicode_colon_pattern = re.compile(r"[\u0706\u003a\u1365\ua6f4\u003a\u003a\u02d0]")
unicode_ellipsis_pattern = re.compile(r"[\u2026\ufe19\u0eaf\u2026\u2026]")


def normalize_unicode(text: str) -> str:
    """Normalize unicode to their ASCII counterpart."""
    # The following are your friend:
    # https://unicode-table.com/en/sets
    # Array.from(document.querySelectorAll('[data-template]')).map(x => x.getAttribute("data-template")).filter(x => x.includes("{")).map(x => JSON.parse(x)).filter(x => x.title.includes("Stop")).map(x => "\\u" + "0000".substring(0, 4 - x.symbol.charCodeAt(0).toString(16).length) + x.symbol.charCodeAt(0).toString(16)).join("")
    text = unicode_hyphen_pattern.sub("-", text)
    text = unicode_single_quote_pattern.sub("'", text)
    text = unicode_double_quote_pattern.sub('"', text)
    text = unicode_period_pattern.sub(".", text)
    text = unicode_comma_pattern.sub(",", text)
    text = unicode_exclamation_pattern.sub("!", text)
    text = unicode_question_pattern.sub("?", text)
    text = unicode_colon_pattern.sub(":", text)
    text = unicode_ellipsis_pattern.sub("...", text)

    # TODO: \u2460-\u325a 0-30, currently in special characters instead

    return text


def normalize_abbreviations(text: str) -> str:
    # Note: does not handle etc. i.e.
    return text


def clean_text(text: str) -> str:
    """Clean and normalize text into sentences."""
    # Transform all of the text to lowercase
    text = text.lower()
    # Normalize unicode
    text = normalize_unicode(text)
    # Normalize abbreviations
    text = normalize_abbreviations(text)
    # Remove digits
    text = digit_pattern.sub(" ", text)
    # Remove websites
    text = website_pattern.sub(" ", text)
    # Remove math expressions
    text = math_pattern.sub(" ", text)
    # Remove possessives
    text = possessive_pattern.sub(r"\1", text)
    # Remove hyphens not between words
    text = hyphen_pattern.sub(" ", text)
    # Normalize whitespace
    text = whitespace_pattern.sub(" ", text)
    # Split sentences to newlines
    text = punctuation_pattern.sub("\n", text)
    # Remove special characters
    text = special_pattern.sub("", text)
    # Remove padding
    text = padding_pattern.sub("", text)
    # Remove single characters on a line
    text = single_character_line_pattern.sub("", text)
    # Normalize newlines
    text = newline_pattern.sub("\n", text)
    return text


def extract_words(text: str) -> List[str]:
    """Extract words from a text."""
    # Remove newlines
    text = newline_pattern.sub("", text)
    # Split words
    return [word for word in text.split(" ") if len(word) > 0]
