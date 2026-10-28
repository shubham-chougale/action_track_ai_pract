from pathlib import Path

from actiontrack.extract import extract_items
from actiontrack.owners import AMBIGUOUS, resolve_owner
from actiontrack.people import People
from actiontrack.scanner import scan_folder

SAMPLE = Path(__file__).parents[1] / "notes"


def test_priya_and_rahul_at_the_offsite_are_ambiguous_and_flagged():
    notes = scan_folder(SAMPLE).notes
    people = People.from_notes(notes)
    (offsite,) = [n for n in notes if n.name == "2026-09-30-q4-offsite.md"]
    owners = {i.owner_text: i for i in extract_items(offsite.text) if i.owner_text in ("Priya", "Rahul")}
    assert set(owners) == {"Priya", "Rahul"}
    for raw in owners:
        r = resolve_owner(raw, offsite.meta.attendees, people)
        assert (r.kind, r.owners, r.raw, r.flagged) == (AMBIGUOUS, [], raw, True)
