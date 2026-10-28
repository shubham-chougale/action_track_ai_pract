"""Owner resolution: raw owner text -> known people, Unassigned, or a flagged owner."""

from dataclasses import dataclass, field

from actiontrack.people import People

RESOLVED = "resolved"
UNASSIGNED = "unassigned"
AMBIGUOUS = "ambiguous"
UNKNOWN = "unknown"


@dataclass
class Resolution:
    kind: str
    owners: list[str] = field(default_factory=list)  # full names, only when kind is RESOLVED
    raw: str | None = None  # the owner wording as written, always kept

    @property
    def flagged(self) -> bool:
        return self.kind in (AMBIGUOUS, UNKNOWN)


def _first(name: str) -> str:
    return name.split()[0].casefold()


def resolve_owner(raw: str | None, attendees: list[str], people: People) -> Resolution:
    text = " ".join((raw or "").split())
    handle = text.removeprefix("@")
    known = people.names()
    for name in known:
        if name.casefold() == handle.casefold():
            return Resolution(RESOLVED, [name], raw)
    # A bare first name: that meeting's attendees first, then everyone known.
    for pool in ([n for n in attendees if n in known], known):
        matches = [n for n in pool if _first(n) == handle.casefold()]
        if len(matches) == 1:
            return Resolution(RESOLVED, matches, raw)
        if matches:
            return Resolution(AMBIGUOUS, [], raw)
    return Resolution(UNKNOWN, [], raw)
