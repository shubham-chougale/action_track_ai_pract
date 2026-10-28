import actiontrack.cli as cli
from actiontrack.cli import main
from actiontrack.store import Store
from listing_support import seed

UNASSIGNED = [{"kind": "unassigned", "raw": "Someone"}]


def setup(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Store(tmp_path).learn_people(["Priya Nair", "Rahul Mehta"])
    calls = []
    monkeypatch.setattr(cli, "create_draft", lambda *a, **k: calls.append(a) or "draft-1", raising=False)
    return calls


def test_owner_without_items_gets_no_draft_and_a_message(tmp_path, monkeypatch, capsys):
    calls = setup(tmp_path, monkeypatch)
    seed(tmp_path, task="done already", status="done")
    assert main(["followup", "Priya Nair", "--today", "2026-10-28"]) == 0
    out = capsys.readouterr().out
    assert "No open or overdue items for Priya Nair" in out and "no draft" in out
    assert calls == []


def test_person_with_no_items_at_all(tmp_path, monkeypatch, capsys):
    calls = setup(tmp_path, monkeypatch)
    seed(tmp_path, task="priya's")
    assert main(["followup", "Rahul Mehta", "--today", "2026-10-28"]) == 0
    assert "No open or overdue items for Rahul Mehta" in capsys.readouterr().out
    assert calls == []


def test_unassigned_count_is_printed_when_there_are_no_items(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    seed(tmp_path, task="a", owners=UNASSIGNED)
    seed(tmp_path, task="b", owners=UNASSIGNED)
    main(["followup", "Priya Nair", "--today", "2026-10-28"])
    assert "Unassigned items: 2" in capsys.readouterr().out


def test_unassigned_count_is_printed_when_a_draft_is_made(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    seed(tmp_path, task="mine")
    seed(tmp_path, task="a", owners=UNASSIGNED)
    main(["followup", "Priya Nair", "--today", "2026-10-28"])
    assert "Unassigned items: 1" in capsys.readouterr().out


def test_zero_unassigned_is_reported_too(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    main(["followup", "Priya Nair", "--today", "2026-10-28"])
    assert "Unassigned items: 0" in capsys.readouterr().out
