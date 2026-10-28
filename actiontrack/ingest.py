"""Ingest pipeline: scan -> metadata -> extract -> owners -> dates -> merge -> store."""

from dataclasses import dataclass, field
from pathlib import Path

from actiontrack.duedate import resolve_due
from actiontrack.extract import extract_items
from actiontrack.merge import Mention, merge_mentions
from actiontrack.owners import RESOLVED, resolve_owner
from actiontrack.people import People
from actiontrack.scanner import Note, Skipped, scan_folder
from actiontrack.store import Store


@dataclass
class IngestResult:
    scanned: int = 0
    ingested: int = 0
    skipped: list[Skipped] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=lambda: {"new": 0, "merged": 0, "unchanged": 0})
    flagged: list[Mention] = field(default_factory=list)  # every flagged mention seen this run


def _owner_entries(resolution) -> list[dict]:
    if resolution.kind == RESOLVED:
        return [{"kind": "person", "name": name} for name in resolution.owners]
    return [{"kind": resolution.kind, "raw": resolution.raw}]


def note_mentions(note: Note, people: People) -> list[Mention]:
    """One mention per checkbox line in the note, owner and due date resolved."""
    source = {"file": note.name, "date": note.meta.date, "title": note.meta.title}
    mentions = []
    for item in extract_items(note.text):
        resolution = resolve_owner(item.owner_text, note.meta.attendees, people)
        due = resolve_due(item.due_phrase, note.meta.date)
        reasons = [r for r in (item.flag, f"{resolution.kind} owner" if resolution.flagged else None,
                               due.flag) if r]
        mentions.append(Mention(
            owners=_owner_entries(resolution), task=item.task, original_line=item.line,
            source=source, done=item.done, due=due.date,
            due_raw=due.phrase if due.flag else None,
            flagged=bool(reasons), flag_reason="; ".join(reasons) or None,
        ))
    return mentions


def ingest_folder(folder: Path | str, base: Path | str | None = None) -> IngestResult:
    """Ingest every usable note in the folder into the store under `base` (default: cwd).

    Raises FolderError when the folder cannot be scanned at all.
    """
    scan = scan_folder(folder)
    people = People.from_notes(scan.notes)
    mentions = [m for note in scan.notes for m in note_mentions(note, people)]
    counts = merge_mentions(Store(base), mentions)
    flagged = [m for m in mentions if m.flagged]
    return IngestResult(scan.scanned, len(scan.notes), scan.skipped, counts, flagged)
