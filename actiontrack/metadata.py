"""Meeting metadata: title, date and attendees read from the note body only."""

import re
from dataclasses import dataclass, field
from datetime import date

MISSING_DATE = "missing date"
INVALID_DATE = "invalid date"

_MONTHS = {
    name: number
    for number, names in enumerate(
        ("january jan", "february feb", "march mar", "april apr", "may", "june jun",
         "july jul", "august aug", "september sep sept", "october oct", "november nov",
         "december dec"),
        start=1,
    )
    for name in names.split()
}
_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_LONG = re.compile(r"^(?:[A-Za-z]+,?\s+)?(\d{1,2})\s+([A-Za-z]+),?\s+(\d{4})$")
_HEADER_FIELD = re.compile(r"^\s*(date|attendees)\s*:\s*(.*?)\s*$", re.I)
_TITLE = re.compile(r"^#\s*meeting\s*:\s*(.*?)\s*$", re.I)
_LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s")


@dataclass
class Metadata:
    title: str | None = None
    date: str | None = None  # YYYY-MM-DD
    attendees: list[str] = field(default_factory=list)
    reason: str | None = None  # set when the note has no usable date


def _parse_date(value: str) -> str | None:
    """Return YYYY-MM-DD for a real calendar date, else None."""
    parts = None
    if m := _ISO.match(value):
        parts = tuple(int(g) for g in m.groups())
    elif (m := _LONG.match(value)) and m.group(2).lower() in _MONTHS:
        parts = (int(m.group(3)), _MONTHS[m.group(2).lower()], int(m.group(1)))
    try:
        return date(*parts).isoformat() if parts else None
    except ValueError:
        return None


def _split_attendees(value: str) -> list[str]:
    value = value.strip().removeprefix("[").removesuffix("]")
    names = (n.strip().strip("'\"").strip() for n in value.split(","))
    return [n for n in names if n]


def _front_matter(lines: list[str]) -> tuple[dict[str, str], int] | None:
    """Return (key/value pairs, index of first body line) for a leading YAML block."""
    if not lines or lines[0].strip() != "---":
        return None
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            pairs = {}
            for line in lines[1:end]:
                key, sep, value = line.partition(":")
                if sep:
                    pairs[key.strip().lower()] = value.strip()
            return pairs, end + 1
    return None


def _header_fields(lines: list[str]) -> dict[str, str]:
    """Style A: first Title/Date/Attendees lines, before the body (a ## heading or list) starts."""
    fields: dict[str, str] = {}
    for line in lines:
        if line.startswith("##") or _LIST_ITEM.match(line):
            break
        if (m := _TITLE.match(line)) and "title" not in fields:
            fields["title"] = m.group(1)
        elif (m := _HEADER_FIELD.match(line)) and m.group(1).lower() not in fields:
            fields[m.group(1).lower()] = m.group(2)
    return fields


def parse_metadata(text: str) -> Metadata:
    """Read metadata from note text. The filename is never consulted."""
    lines = text.lstrip("﻿").splitlines()
    front = _front_matter(lines)
    fields = front[0] if front else _header_fields(lines)

    meta = Metadata(
        title=fields.get("title", "").strip("'\"").strip() or None,
        attendees=_split_attendees(fields.get("attendees", "")),
    )
    raw_date = fields.get("date", "").strip().strip("'\"")
    if not raw_date:
        meta.reason = MISSING_DATE
    elif (iso := _parse_date(raw_date)) is None:
        meta.reason = INVALID_DATE
    else:
        meta.date = iso
    return meta
