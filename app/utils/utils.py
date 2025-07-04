import re


def pluralize(word: str) -> str:
    if re.search(r"[^aeiou]y$", word):
        return re.sub(r"y$", "ies", word)
    return word + "s"
