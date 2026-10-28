from pathlib import Path

import pytest

from actiontrack.extract import extract_items
from actiontrack.owners import AMBIGUOUS, RESOLVED, UNKNOWN, resolve_owner
from actiontrack.people import People
from actiontrack.scanner import scan_folder

SAMPLE = Path(__file__).parents[1] / "notes"


@pytest.fixture(scope="module")
def sample():
    notes = scan_folder(SAMPLE).notes
    return {n.name: n for n in notes}, People.from_notes(notes)


def _owner_of(note, prefix):
    (item,) = [i for i in extract_items(note.text) if i.owner_text and i.owner_text.startswith(prefix)]
    return item.owner_text


def test_anita_and_rahul_resolve_by_that_meetings_attendees(sample):
    notes, people = sample
    note = notes["2026-09-18-design-review.md"]
    raw = _owner_of(note, "Anita &")
    r = resolve_owner(raw, note.meta.attendees, people)
    assert (r.kind, r.owners, r.raw) == (RESOLVED, ["Anita Desai", "Rahul Mehta"], raw)


def test_lena_with_priya_gives_two_owners(sample):
    notes, people = sample
    note = notes["2026-09-18-design-review.md"]
    raw = _owner_of(note, "Lena (with")
    r = resolve_owner(raw, note.meta.attendees, people)
    assert (r.kind, r.owners) == (RESOLVED, ["Lena Fischer", "Priya Nair"])


def test_and_form_and_duplicate_names():
    people = People()
    people.learn(["Anita Desai", "Rahul Mehta"])
    assert resolve_owner("Anita and Rahul", [], people).owners == ["Anita Desai", "Rahul Mehta"]
    assert resolve_owner("Anita & Anita", [], people).owners == ["Anita Desai"]


def test_an_unresolvable_co_owner_flags_the_whole_item_and_guesses_nothing():
    people = People()
    people.learn(["Anita Desai", "Priya Nair", "Priya Shah"])
    both = ["Anita Desai", "Priya Nair", "Priya Shah"]
    r = resolve_owner("Anita & Priya", both, people)
    assert (r.kind, r.owners, r.raw, r.flagged) == (AMBIGUOUS, [], "Anita & Priya", True)
    r = resolve_owner("Anita (with Zed)", both, people)
    assert (r.kind, r.owners, r.flagged) == (UNKNOWN, [], True)
