import shutil
from pathlib import Path

import pytest

from actiontrack.cli import main
from actiontrack.store import Store

FIXTURES = Path(__file__).parent / "fixtures" / "notes"


@pytest.fixture
def ingested(tmp_path, monkeypatch):
    notes = tmp_path / "notes"
    shutil.copytree(FIXTURES, notes)
    monkeypatch.chdir(tmp_path)
    assert main(["ingest", str(notes)]) == 0
    return {i.task: i for i in Store(tmp_path).all()}


def person(name):
    return [{"kind": "person", "name": name}]


def test_stores_one_item_per_real_checkbox_line(ingested):
    assert len(ingested) == 11


def test_owner_date_and_source_come_through(ingested):
    item = ingested["send the quote"]
    assert item.owners == person("Priya Nair")  # that meeting's attendee, not Priya Shah
    assert item.due == "2026-10-09"  # "Friday" after Monday 2026-10-05
    assert item.status == "open" and not item.flagged
    assert item.original_line == "- [ ] Priya to send the quote by Friday"
    assert item.sources == [{"file": "header_style_a.md", "date": "2026-10-05", "title": "Style A"}]


def test_same_first_name_resolved_by_attendees(ingested):
    item = ingested["book the room"]
    assert item.owners == person("Rahul Verma")
    assert item.due == "2026-10-12"
    assert item.sources[0]["file"] == "header_style_b.md"


def test_every_marker_is_stored_with_its_status(ingested):
    markers = {t: i.status for t, i in ingested.items()
               if i.sources[0]["file"] == "markers.md"}
    assert markers == {
        "do dash open": "open", "do dash done": "done", "do dash upper done": "done",
        "do star open": "open", "do plus open": "open",
    }


def test_nested_pair_is_two_items(ingested):
    assert ingested["draft the plan"].owners == person("Meera Rao")
    assert ingested["review the plan"].owners == person("Karan Singh")
    assert ingested["review the plan"].due == "2026-10-12"


def test_decoys_are_kept_and_flagged(ingested):
    code = ingested["do template task by date"]
    comment = ingested["do commented-out task"]
    assert (code.flagged, code.flag_reason) == (True, "code block")
    assert code.owners == [{"kind": "unassigned", "raw": "Owner"}]
    assert (comment.flagged, comment.flag_reason) == (True, "comment")


def test_skipped_notes_store_nothing(ingested):
    files = {s["file"] for i in ingested.values() for s in i.sources}
    assert files == {"header_style_a.md", "header_style_b.md", "markers.md", "nested.md",
                     "code_block_decoy.md", "comment_decoy.md"}
