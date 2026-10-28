"""People roster: known people, learned from Attendees lines only."""


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
