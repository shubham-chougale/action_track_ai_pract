"""Action-item extraction: find checkbox lines in a note's text."""

import re
from dataclasses import dataclass

_CHECKBOX = re.compile(r"^\s*[-*+]\s+\[([ xX])\]\s+(\S.*?)\s*$")


@dataclass
class Item:
    line: str  # original full line, verbatim
    done: bool


def extract_items(text: str) -> list[Item]:
    items = []
    for line in text.splitlines():
        if m := _CHECKBOX.match(line):
            items.append(Item(line=line, done=m.group(1) != " "))
    return items
