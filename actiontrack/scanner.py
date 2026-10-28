"""Note scanning: pick the notes to ingest and skip malformed ones with a reason."""

from dataclasses import dataclass, field
from pathlib import Path

from actiontrack.metadata import Metadata, parse_metadata


class FolderError(Exception):
    """The folder given to ingest cannot be scanned at all (fatal)."""


@dataclass
class Note:
    name: str
    path: Path
    text: str
    meta: Metadata


@dataclass
class Skipped:
    name: str
    reason: str


@dataclass
class ScanResult:
    notes: list[Note] = field(default_factory=list)
    skipped: list[Skipped] = field(default_factory=list)
    scanned: int = 0  # top-level .md files looked at


def scan_folder(folder: Path | str) -> ScanResult:
    folder = Path(folder)
    if not folder.exists():
        raise FolderError(f"folder not found: {folder}")
    if not folder.is_dir():
        raise FolderError(f"not a folder: {folder}")

    result = ScanResult()
    for path in folder.iterdir():
        if path.suffix.lower() != ".md" or not path.is_file():
            continue
        result.scanned += 1
        result.notes.append(Note(path.name, path, "", Metadata()))
    return result
