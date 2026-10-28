import actiontrack.cli as cli
from actiontrack.cli import main
from actiontrack.store import Store, data_dir
from listing_support import seed


def setup(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Store(tmp_path).learn_people(["Priya Nair", "Priya Shah"])
    seed(tmp_path, task="quote", due="2026-11-10")
    calls = []

    def fake(recipient, subject, body):
        calls.append((recipient, subject, body))
        return "draft-1"

    monkeypatch.setattr(cli, "create_draft", fake)
    return calls


def write_roster(tmp_path, text):
    (data_dir(tmp_path) / "roster.csv").write_text(text, encoding="utf-8")


def run(capsys):
    code = main(["followup", "Priya Nair", "--today", "2026-10-28"])
    return code, capsys.readouterr()


def test_roster_row_gives_the_recipient(tmp_path, monkeypatch, capsys):
    calls = setup(tmp_path, monkeypatch)
    write_roster(tmp_path, "name,email\nPriya Nair,priya.nair@example.com\nPriya Shah,priya.shah@example.com\n")
    code, captured = run(capsys)
    assert code == 0 and calls[0][0] == "priya.nair@example.com"
    assert "warning" not in captured.err


def test_no_roster_file_still_makes_the_draft_with_a_warning(tmp_path, monkeypatch, capsys):
    calls = setup(tmp_path, monkeypatch)
    code, captured = run(capsys)
    assert code == 0 and len(calls) == 1 and calls[0][0] is None
    assert "warning" in captured.err and "Priya Nair" in captured.err
    assert calls[0][1].startswith("Action items follow-up: Priya Nair")


def test_person_missing_from_roster_warns(tmp_path, monkeypatch, capsys):
    calls = setup(tmp_path, monkeypatch)
    write_roster(tmp_path, "name,email\nPriya Shah,priya.shah@example.com\n")
    code, captured = run(capsys)
    assert code == 0 and calls[0][0] is None and "warning" in captured.err


def test_draft_id_is_printed(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    _, captured = run(capsys)
    assert "draft-1" in captured.out
