import re
from typing import List, Set


digit_pattern = re.compile(r"\b\d+\b")
possessive_pattern = re.compile(r"([a-z])'s")
punctuation_pattern = re.compile(r"[!?.]")
special_pattern = re.compile(r"[\\!\"#$%&'()*+,./:;<=>?@[\]^_`{|}~)”»°→©]")
normalize_hyphen_pattern = re.compile(r"[-–]")
hyphen_pattern = re.compile(r"\B-\B|\b-\B|\B-\b")
whitespace_pattern = re.compile(r"\s+")
newline_pattern = re.compile(r"\n+")
padding_pattern = re.compile(r"^\s+|\s+$", flags=re.MULTILINE)
website_pattern = re.compile(r"(https?:\/\/)?([a-z0-9-]+\.)+[a-z]{2,}(\/[a-z0-9%&?=#\.]+)*")
single_character_line_pattern = re.compile(r"^.$", flags=re.MULTILINE)
math_pattern = re.compile(r"\{[A-Za-z0-9\\ _^+\-*\{\}]+\}")

# Note: does not handle etc. i.e.
def clean_text(text: str) -> str:
    """Clean and normalize text into sentences."""
    # Transform all of the text
    text = text.lower()
    # Remove digits
    text = digit_pattern.sub(" ", text)
    # Remove websites
    text = website_pattern.sub(" ", text)
    # Remove math expressions
    text = math_pattern.sub(" ", text)
    # Remove possessives
    text = possessive_pattern.sub(r"\1", text)
    # Normalize hyphens
    text = normalize_hyphen_pattern.sub("-", text)
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
