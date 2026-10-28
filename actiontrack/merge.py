"""Duplicate merging: recognise the same action item across meetings."""

import re
from difflib import SequenceMatcher

from actiontrack.extract import _DUE_TAIL

SIMILARITY = 0.85  # normalised wording at least this alike is "the same task"

_ARTICLES = {"a", "an", "the"}


def normalize_task(task: str) -> str:
    """Lower-case the task and drop its due phrase, punctuation and articles."""
    if m := _DUE_TAIL.search(task):
        task = task[: m.start()]
    words = re.sub(r"[^\w\s]", "", task.lower().replace("-", " ")).split()
    return " ".join(w for w in words if w not in _ARTICLES)


def same_task(a: str, b: str) -> bool:
    return SequenceMatcher(None, normalize_task(a), normalize_task(b)).ratio() >= SIMILARITY
