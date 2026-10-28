import shutil
from pathlib import Path

import pytest

from actiontrack.cli import main
from actiontrack.store import Store

FIXTURES = Path(__file__).parent / "fixtures" / "notes"


@pytest.fixture
def base(tmp_path, monkeypatch):
    notes = tmp_path / "notes"
    shutil.copytree(FIXTURES, notes)
    monkeypatch.chdir(tmp_path)
    main(["ingest", str(notes)])
    return tmp_path


def test_done_marks_the_item_and_prints_id_owner_task(base, capsys):
    item = next(i for i in Store(base).all() if i.task == "send the quote")
    capsys.readouterr()
    assert main(["done", str(item.id)]) == 0
    out = capsys.readouterr().out
    assert f"#{item.id}" in out and "Priya Nair" in out and "send the quote" in out
    stored = Store(base).get(item.id)
    assert (stored.status, stored.status_manual) == ("done", True)


def test_done_touches_only_that_item(base):
    before = {i.id: i.status for i in Store(base).all()}
    main(["done", "1"])
    after = {i.id: i.status for i in Store(base).all()}
    assert after.pop(1) == "done"
    before.pop(1)
    assert after == before


def test_done_survives_a_reingest(base):
    main(["done", "1"])
    main(["ingest", str(base / "notes")])
    assert Store(base).get(1).status == "done"
