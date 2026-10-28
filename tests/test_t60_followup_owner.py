from actiontrack.cli import main
from actiontrack.store import Store
from listing_support import person, seed


def setup(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Store(tmp_path).learn_people(["Priya Nair", "Priya Shah", "Rahul Mehta"])
    seed(tmp_path, task="quote", due="2026-11-10")


def test_first_name_shared_by_two_people_fails_with_candidates(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    assert main(["followup", "Priya", "--today", "2026-10-28"]) != 0
    captured = capsys.readouterr()
    assert "Priya Nair" in captured.err and "Priya Shah" in captured.err
    assert captured.out == ""


def test_full_name_proceeds(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    assert main(["followup", "Priya Nair", "--today", "2026-10-28"]) == 0
    assert "Priya Nair" in capsys.readouterr().out


def test_unknown_person_fails(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    assert main(["followup", "Zed", "--today", "2026-10-28"]) != 0
    assert "Zed" in capsys.readouterr().err


def test_unassigned_is_not_a_followup_owner(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    assert main(["followup", "unassigned"]) != 0


def test_bad_today_is_an_error(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    assert main(["followup", "Priya Nair", "--today", "soon"]) != 0
    assert "--today" in capsys.readouterr().err
