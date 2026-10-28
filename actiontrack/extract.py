"""Action-item extraction: find checkbox lines in a note's text and split them."""

import re
from dataclasses import dataclass

CODE_BLOCK = "code block"
COMMENT = "comment"

_CHECKBOX = re.compile(r"^\s*[-*+]\s+\[([ xX])\]\s+(\S.*?)\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")

_WEEKDAY = r"(?:mon|tue|tues|wed|thu|thur|thurs|fri|sat|sun)(?:day|sday|nesday|rsday|urday)?"
_MONTH = (r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)"
          r"(?:uary|ruary|ch|il|e|y|ust|tember|ober|ember)?")
_DATE = (
    r"\d{4}-\d{2}-\d{2}"
    rf"|(?:{_WEEKDAY}\.?,?\s+)?\d{{1,2}}(?:st|nd|rd|th)?\s+{_MONTH}(?:\s+\d{{4}})?"
    rf"|(?:{_WEEKDAY}\.?,?\s+)?{_MONTH}\s+\d{{1,2}}(?:st|nd|rd|th)?"
    rf"|(?:next\s+)?{_WEEKDAY}"
    r"|(?:eod|cob)(?:\s+(?:tomorrow|today))?|tomorrow|today"
    r"|end\s+of\s+(?:the\s+)?(?:next\s+)?(?:week|month|quarter|year)"
    rf"|mid-?\s*{_MONTH}"
    rf"|{_MONTH}"
)
# A due phrase is a trailing "by/due/on/for <date>" or "before the next <thing>",
# optionally set off by a dash or comma (hyphen, en dash, em dash).
_DUE_TAIL = re.compile(
    rf"(?:\s*[-–—,;]\s*|\s+)(?P<due>(?:(?:by|due|on|for|until)\s+(?:{_DATE})"
    r"|before\s+the\s+next\s+\w+))\s*$",
    re.I,
)
_NAME = r"[A-Z][\w.'’-]*"
_PERSON = rf"(?:@\w+|{_NAME}(?:\s+{_NAME})*)"
# "Priya", "Priya N.", "@anita", "A & B", "A and B", "A (with B)", then "to <task>" or ": <task>".
_OWNER = re.compile(
    rf"^(?P<owner>{_PERSON}(?:\s*(?:&|and)\s*{_PERSON})*(?:\s*\(with\s+{_PERSON}\))?)"
    r"(?:\s+to\s+|\s*:\s+)(?P<task>.+)$"
)
_TRAIL = " \t-–—,;:"


@dataclass
class Item:
    line: str  # original full line, verbatim
    done: bool
    flag: str | None = None  # CODE_BLOCK or COMMENT for decoys, else None
    owner_text: str | None = None  # raw owner wording, as written
    task: str = ""  # the line without owner and due phrase
    due_phrase: str | None = None  # raw due wording, e.g. "by Friday"


def _split(body: str) -> tuple[str | None, str, str | None]:
    """Split checkbox text into (raw owner, task, raw due phrase)."""
    due = None
    if m := _DUE_TAIL.search(body):
        due, body = m.group("due"), body[: m.start()]
    owner = None
    if m := _OWNER.match(body):
        owner, body = m.group("owner"), m.group("task")
    return owner, body.strip(_TRAIL), due


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
            owner, task, due = _split(m.group(2))
            items.append(Item(line, m.group(1) != " ", flag, owner, task, due))
    return items
