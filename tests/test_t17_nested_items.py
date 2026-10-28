from dataclasses import fields
from pathlib import Path

from actiontrack.extract import extract_items

FIXTURES = Path(__file__).parent / "fixtures" / "notes"
OFFSITE = Path(__file__).parent.parent / "notes" / "2026-09-30-q4-offsite.md"


def _lines(path):
    return [i.line for i in extract_items(path.read_text(encoding="utf-8"))]


def test_nested_item_is_a_separate_item_in_the_offsite_note():
    lines = _lines(OFFSITE)
    meera = [x for x in lines if "Meera to finalise" in x]
    karan = [x for x in lines if "Karan to validate" in x]
    assert len(meera) == 1 and len(karan) == 1
    assert karan[0].startswith("  - [ ]")  # indentation kept, but only as part of the line


def test_nested_fixture_yields_two_items_with_no_link():
    items = extract_items((FIXTURES / "nested.md").read_text(encoding="utf-8"))
    assert len(items) == 2
    names = {f.name for f in fields(items[0])}
    assert not names & {"parent", "children", "parent_id", "depth", "indent"}
    assert items[0] is not items[1] and items[0].line != items[1].line
