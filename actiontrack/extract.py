"""Action-item extraction: find checkbox lines in a note's text."""

import re
from dataclasses import dataclass

CODE_BLOCK = "code block"
COMMENT = "comment"

_CHECKBOX = re.compile(r"^\s*[-*+]\s+\[([ xX])\]\s+(\S.*?)\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")


@dataclass
class Item:
    line: str  # original full line, verbatim
    done: bool
    flag: str | None = None  # CODE_BLOCK or COMMENT for decoys, else None


def extract_items(text: str) -> list[Item]:
    """Every checkbox line; those inside a fenced block or HTML comment are flagged."""
    items = []
    fence: str | None = None  # opening fence marker while inside a code block
    in_comment = False
    for line in text.splitlines():
        flag = None
        candidate = line
        if fence:
            flag = CODE_BLOCK
            if line.strip().startswith(fence):
                fence = None
                continue
        elif in_comment or line.lstrip().startswith("<!--"):
            flag = COMMENT
            candidate = line.lstrip().removeprefix("<!--") if not in_comment else line
            in_comment = "-->" not in candidate
            candidate = candidate.split("-->")[0]
        elif m := _FENCE.match(line):
            fence = m.group(1)
            continue
        if m := _CHECKBOX.match(candidate):
            items.append(Item(line=line, done=m.group(1) != " ", flag=flag))
    return items
