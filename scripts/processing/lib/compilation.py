from typing import List, Dict

# Ugly, but mulitudes faster than
# return {word: words.count(word) for word in set(words)}
def count(words: List[str]) -> Dict[str, int]:
    """Count words."""
    counted_words = {}
    for word in words:
        if word not in counted_words:
            counted_words[word] = 0
        counted_words[word] = counted_words[word] + 1
    return counted_words
