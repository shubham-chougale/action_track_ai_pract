"""People roster: known people, learned from Attendees lines only."""

import csv
from pathlib import Path

UNASSIGNED = "unassigned"


class LookupFailure(Exception):
    """A name given to --owner / followup matches nobody, or more than one person."""

    def __init__(self, message: str, matches: list[str]):
        super().__init__(message)
        self.matches = matches


def _key(text: str) -> str:
    return " ".join(text.split()).casefold()


class People:
    """Known people in first-seen order, each with an optional email."""

    def __init__(self):
        self._emails: dict[str, str | None] = {}

    @classmethod
    def from_notes(cls, notes) -> "People":
        people = cls()
        for note in notes:
            people.learn(note.meta.attendees)
        return people

    def learn(self, attendees: list[str]) -> None:
        for name in attendees:
            self._emails.setdefault(name, None)

    def names(self) -> list[str]:
        return list(self._emails)

    def email(self, name: str) -> str | None:
        return self._emails.get(name)

    def load_roster(self, path: Path | str) -> None:
        """Attach emails from a `name,email` CSV by exact full name. Never raises.

        A missing or unreadable file, a missing person, and a row for an unknown
        name are all fine: the roster supplies emails only and adds no people.
        """
        try:
            with open(path, newline="", encoding="utf-8-sig") as handle:
                for row in csv.DictReader(handle):
                    name = (row.get("name") or "").strip()
                    email = (row.get("email") or "").strip()
                    if name in self._emails and email:
                        self._emails[name] = email
        except (OSError, UnicodeDecodeError, csv.Error):
            return

    def find(self, text: str, allow_unassigned: bool = False) -> str:
        """Full name of the one person `text` names: a full name, or a unique first name.

        Raises LookupFailure listing the candidates when a first name is shared.
        """
        key = _key(text)
        if allow_unassigned and key == UNASSIGNED:
            return UNASSIGNED
        for name in self._emails:
            if _key(name) == key:
                return name
        matches = [n for n in self._emails if _key(n).split()[0] == key]
        if len(matches) == 1:
            return matches[0]
        if matches:
            raise LookupFailure(
                f"'{text}' matches more than one person: {', '.join(matches)}. Use the full name.",
                matches,
            )
        raise LookupFailure(f"no known person matches '{text}'", [])
