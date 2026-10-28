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


@pytest.mark.parametrize("bad", ["999", "abc", "0", "-1", "1.5"])
def test_unknown_or_non_numeric_id_is_an_error(base, capsys, bad):
    capsys.readouterr()
    assert main(["done", bad]) != 0
    captured = capsys.readouterr()
    assert captured.err.startswith("error:") and captured.out == ""
    assert all(i.status != "done" or i.status_manual is False for i in Store(base).all())


def test_second_done_says_already_done_and_exits_zero(base, capsys):
    main(["done", "3"])
    capsys.readouterr()
    assert main(["done", "3"]) == 0
    assert "already done" in capsys.readouterr().out


def test_item_done_in_a_note_is_already_done_and_becomes_sticky(base, capsys):
    done_item = next(i for i in Store(base).all() if i.status == "done")
    assert not done_item.status_manual
    capsys.readouterr()
    assert main(["done", str(done_item.id)]) == 0
    assert "already done" in capsys.readouterr().out
    assert Store(base).get(done_item.id).status_manual


def test_co_owned_item_is_closed_for_both_owners(tmp_path, monkeypatch, capsys):
    notes = tmp_path / "notes"
    notes.mkdir()
    (notes / "a.md").write_text(
        "# Meeting: A\nDate: 2026-10-05\nAttendees: Anita Desai, Rahul Mehta\n\n"
        "- [ ] Anita & Rahul to demo the build by Friday\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    main(["ingest", str(notes)])
    capsys.readouterr()
    assert main(["done", "1"]) == 0
    out = capsys.readouterr().out
    assert "Anita Desai" in out and "Rahul Mehta" in out
    (item,) = Store(tmp_path).all()
    assert item.status == "done" and len(item.owners) == 2


def test_flagged_item_can_be_dismissed(base, capsys):
    flagged = next(i for i in Store(base).all() if i.flagged)
    capsys.readouterr()
    assert main(["done", str(flagged.id)]) == 0
    assert str(flagged.id) in capsys.readouterr().out
    assert Store(base).get(flagged.id).status == "done"


def test_done_in_an_empty_directory_is_an_error(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["done", "1"]) != 0
    assert "no item" in capsys.readouterr().err
