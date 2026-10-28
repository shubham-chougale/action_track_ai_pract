import pytest

from actiontrack.cli import main
from listing_support import seed, table_rows

TODAY = ["--today", "2026-10-28"]


@pytest.fixture
def base(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    seed(tmp_path, task="late one", due="2026-11-20")
    seed(tmp_path, task="no date one")
    seed(tmp_path, task="early one", due="2026-10-02")
    seed(tmp_path, task="finished one", due="2026-10-10", status="done")
    return tmp_path


def test_all_items_including_done_sorted_by_due_with_no_date_last(base, capsys):
    assert main(["list", *TODAY]) == 0
    rows = table_rows(capsys.readouterr().out)
    order = ["early one", "finished one", "late one", "no date one"]
    assert [next(t for t in order if t in r) for r in rows] == order


def test_header_has_the_six_columns_in_order(base, capsys):
    main(["list", *TODAY])
    header = capsys.readouterr().out.splitlines()[0].split()
    assert header == ["ID", "Owner(s)", "Task", "Due", "Status", "Source"]


def test_row_shows_id_owner_task_due_status_source(base, capsys):
    main(["list", *TODAY])
    row = next(r for r in table_rows(capsys.readouterr().out) if "early one" in r)
    assert row.split() == ["3", "Priya", "Nair", "early", "one", "2026-10-02", "overdue",
                           "a.md", "(2026-10-01)"]


def test_table_ends_with_a_total_count(base, capsys):
    main(["list", *TODAY])
    assert capsys.readouterr().out.rstrip().splitlines()[-1] == "Total: 4 items"


def test_ties_keep_first_seen_order(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    seed(tmp_path, task="second alphabetically b", due="2026-10-30")
    seed(tmp_path, task="first alphabetically a", due="2026-10-30")
    main(["list", *TODAY])
    rows = table_rows(capsys.readouterr().out)
    assert "second" in rows[0] and "first" in rows[1]
