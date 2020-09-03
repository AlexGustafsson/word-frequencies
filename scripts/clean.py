import re
from typing import List, Set

def clean(text: str) -> str:
    """Clean and normalize text."""
    # Transform all of the text
    text = text.lower()
    # Remove digits
    digit_pattern = r"\b\d+\b"
    text = re.sub(digit_pattern, " ", text)
    # Remove possessives
    possessive_pattern = r"([a-z])'s"
    text = re.sub(possessive_pattern, r"\1", text)
    # Remove punctuation
    punctuation_pattern = r"[\\!\"#$%&'()*+,./:;<=>?@[\]^_`{|}~)]"
    text = re.sub(punctuation_pattern, " ", text)
    # Remove hyphens not between words
    hyphen_pattern = r"\B-\B|\b-\B|\B-\b"
    text = re.sub(hyphen_pattern, " ", text)
    # Normalize whitespace
    whitespace_pattern = r"\s+"
    text = re.sub(whitespace_pattern, " ", text)
    return text

def extract_words(text: str) -> List[str]:
    """Extract words from a text."""
    # Split words
    return [word for word in text.split(" ") if len(word) > 0]
