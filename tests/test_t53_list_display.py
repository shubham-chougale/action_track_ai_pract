import pytest

from actiontrack.cli import main
from listing_support import person, seed, table_rows

TODAY = ["--today", "2026-10-28"]


def row_for(capsys, task):
    main(["list", *TODAY])
    return next(r for r in table_rows(capsys.readouterr().out) if task in r)


@pytest.fixture(autouse=True)
def cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_unresolved_date_shows_raw_phrase_marked_with_question_mark(cwd, capsys):
    seed(cwd, task="plan the offsite", due_raw="by end of month", flagged=True,
         flag_reason="unresolved date")
    assert "by end of month ?" in row_for(capsys, "plan the offsite")


def test_no_date_shows_a_dash(cwd, capsys):
    seed(cwd, task="no date task")
    assert "  -  " in row_for(capsys, "no date task")


def test_flagged_item_shows_a_flag_marker(cwd, capsys):
    seed(cwd, task="flagged task", due="2026-11-01", flagged=True, flag_reason="ambiguous owner",
         owners=[{"kind": "ambiguous", "raw": "Priya"}])
    row = row_for(capsys, "flagged task")
    assert "open [!]" in row and "Priya (ambiguous)" in row


def test_unflagged_item_has_no_marker(cwd, capsys):
    seed(cwd, task="plain task", due="2026-11-01")
    assert "[!]" not in row_for(capsys, "plain task")


def test_unassigned_item_is_labelled(cwd, capsys):
    seed(cwd, task="nobody task", owners=[{"kind": "unassigned", "raw": None}])
    assert "unassigned" in row_for(capsys, "nobody task")


def test_merged_item_shows_latest_source_and_count_of_other_mentions(cwd, capsys):
    seed(cwd, task="merged task", due="2026-11-01", sources=[
        {"file": "b.md", "date": "2026-10-08", "title": "B"},
        {"file": "c.md", "date": "2026-10-15", "title": "C"},
        {"file": "a.md", "date": "2026-10-01", "title": "A"},
    ])
    row = row_for(capsys, "merged task")
    assert "c.md (2026-10-15) +2 more" in row


def test_single_source_has_no_count(cwd, capsys):
    seed(cwd, task="single task", due="2026-11-01")
    assert "more" not in row_for(capsys, "single task")


def test_co_owned_item_lists_both_owners(cwd, capsys):
    seed(cwd, task="shared task", owners=[person("Anita Desai"), person("Rahul Mehta")])
    row = row_for(capsys, "shared task")
    assert "Anita Desai, Rahul Mehta" in row
