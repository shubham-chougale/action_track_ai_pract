import shutil
from pathlib import Path

import pytest

from actiontrack.cli import main
from actiontrack.store import Store

SAMPLE = Path(__file__).parents[1] / "notes"


@pytest.fixture
def folder(tmp_path, monkeypatch):
    notes = tmp_path / "notes"
    shutil.copytree(SAMPLE, notes)
    monkeypatch.chdir(tmp_path)
    main(["ingest", str(notes)])
    return notes


def snapshot(base):
    return {i.id: (i.task, i.first_seen_order, list(i.sources)) for i in Store(base).all()}


def test_done_survives_reingest_even_when_a_note_says_open(folder, tmp_path):
    open_item = next(i for i in Store(tmp_path).all() if i.status == "open" and not i.flagged)
    Store(tmp_path).mark_done(open_item.id)
    main(["ingest", str(folder)])
    kept = Store(tmp_path).get(open_item.id)
    assert (kept.status, kept.status_manual) == ("done", True)


def test_new_note_adds_only_its_own_items_and_sources(folder, tmp_path, capsys):
    before = snapshot(tmp_path)
    existing = next(i for i in Store(tmp_path).all()
                    if i.owners and i.owners[0]["kind"] == "person" and not i.flagged and len(i.sources) == 1)
    name = existing.owners[0]["name"]
    (folder / "2027-01-04-new.md").write_text(
        f"# Meeting: New\nDate: 2027-01-04\nAttendees: {name}\n\n"
        f"- [ ] {name} to {existing.task}\n- [ ] {name} to order the brand new banner\n",
        encoding="utf-8")
    capsys.readouterr()
    main(["ingest", str(folder)])
    out = capsys.readouterr().out

    after = snapshot(tmp_path)
    assert set(before) < set(after) and len(after) == len(before) + 1
    for item_id, (task, order, sources) in before.items():
        assert after[item_id][:2] == (task, order)  # IDs and order unchanged
        extra = after[item_id][2][len(sources):]
        assert after[item_id][2][:len(sources)] == sources  # old sources all kept
        assert [s["file"] for s in extra] == (["2027-01-04-new.md"] if item_id == existing.id else [])
    assert "Items new:       1" in out and "Items merged:    1" in out
