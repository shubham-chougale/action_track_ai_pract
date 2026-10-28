"""Duplicate merging: recognise the same action item across meetings."""

import re
from dataclasses import dataclass
from difflib import SequenceMatcher

from actiontrack.extract import _DUE_TAIL
from actiontrack.store import Store

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


@dataclass
class Mention:
    """One extracted item from one note, with its owner already resolved.

    owners: [{"kind": "person", "name": ...}] per person, or one
    {"kind": "unassigned" | "ambiguous" | "unknown", "raw": ...} entry.
    """

    owners: list[dict]
    task: str
    original_line: str
    source: dict  # {"file", "date", "title"}
    done: bool = False
    due: str | None = None  # resolved YYYY-MM-DD
    due_raw: str | None = None  # raw phrase when it could not be resolved
    flagged: bool = False
    flag_reason: str | None = None


def owner_key(owners: list[dict]) -> tuple:
    """Order-free identity of an owner set; unassigned items share one key."""
    key = set()
    for o in owners:
        if o["kind"] == "person":
            key.add(("person", o["name"]))
        elif o["kind"] == "unassigned":
            key.add(("unassigned", ""))
        else:
            key.add((o["kind"], (o.get("raw") or "").casefold()))
    return tuple(sorted(key))


def merge_mention(store: Store, m: Mention) -> str:
    """Add the mention to the store: returns "new", "merged" or "unchanged"."""
    key = owner_key(m.owners)
    for item in store.all():
        if owner_key(item.owners) == key and same_task(item.task, m.task):
            if m.source in item.sources:
                return "unchanged"
            latest = max(src["date"] for src in item.sources)
            store.add_source(item.id, m.source)
            if m.source["date"] >= latest:  # the latest meeting wins
                store.update(item.id, status="done" if m.done else "open")
            return "merged"
    item = store.add(
        task=m.task, owners=m.owners, original_line=m.original_line, due=m.due,
        due_raw=m.due_raw, status="done" if m.done else "open", flagged=m.flagged,
        flag_reason=m.flag_reason,
    )
    store.add_source(item.id, m.source)
    return "new"
