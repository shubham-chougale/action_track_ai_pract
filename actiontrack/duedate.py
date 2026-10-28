"""Due-date resolution: turn a raw due phrase into an exact date, relative to the meeting date."""

import re
from dataclasses import dataclass
from datetime import date

from actiontrack.metadata import _MONTHS

_LEAD = re.compile(r"^(?:by|due|on|for|until)\s+", re.I)
_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_WEEKDAY_PREFIX = r"(?:[a-z]+\.?,?\s+)?"
_DAY_MONTH = re.compile(rf"^{_WEEKDAY_PREFIX}(\d{{1,2}})(?:st|nd|rd|th)?\s+([a-z]+)(?:\s+(\d{{4}}))?$")
_MONTH_DAY = re.compile(rf"^{_WEEKDAY_PREFIX}([a-z]+)\s+(\d{{1,2}})(?:st|nd|rd|th)?$")


@dataclass
class Due:
    date: str | None  # YYYY-MM-DD, or None when no exact day can be determined
    phrase: str | None  # the raw phrase as written
    flag: str | None = None


def _nearest(day: int, month: int, meeting: date) -> date | None:
    """First day/month on or after the meeting date (looking a few years ahead for 29 Feb)."""
    for year in range(meeting.year, meeting.year + 5):
        try:
            candidate = date(year, month, day)
        except ValueError:
            continue
        if candidate >= meeting:
            return candidate
    return None


def _resolve(text: str, meeting: date) -> date | None:
    if m := _ISO.match(text):
        try:
            return date(*map(int, m.groups()))
        except ValueError:
            return None
    if m := _DAY_MONTH.match(text):
        day, month, year = int(m.group(1)), _MONTHS.get(m.group(2)), m.group(3)
    elif m := _MONTH_DAY.match(text):
        month, day, year = _MONTHS.get(m.group(1)), int(m.group(2)), None
    else:
        return None
    if month is None:
        return None
    if year:
        try:
            return date(int(year), month, day)
        except ValueError:
            return None
    return _nearest(day, month, meeting)


def resolve_due(phrase: str | None, meeting_date: str) -> Due:
    """Resolve a raw due phrase against the meeting date (YYYY-MM-DD)."""
    if not phrase:
        return Due(None, None)
    text = _LEAD.sub("", phrase.strip()).lower()
    resolved = _resolve(text, date.fromisoformat(meeting_date))
    return Due(resolved.isoformat() if resolved else None, phrase)
