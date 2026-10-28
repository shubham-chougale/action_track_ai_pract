import re

import pytest

from actiontrack.cli import main
from listing_support import seed, table_rows

TODAY = ["--today", "2026-10-28"]


@pytest.fixture
def base(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    seed(tmp_path, task="overdue one", due="2026-09-15")
    seed(tmp_path, task="due on cutoff", due="2026-10-01")
    seed(tmp_path, task="due today", due="2026-10-28")
    seed(tmp_path, task="done old", due="2026-09-01", status="done")
    seed(tmp_path, task="no date")
    seed(tmp_path, task="raw date", due_raw="by end of month", flagged=True)
    return tmp_path


def tasks(capsys):
    return [re.split(r"\s{2,}", r.strip())[2] for r in table_rows(capsys.readouterr().out)]


def test_status_open_excludes_overdue_and_done(base, capsys):
    assert main(["list", *TODAY, "--status", "open"]) == 0
    assert tasks(capsys) == ["due today", "no date", "raw date"]


def test_status_done(base, capsys):
    main(["list", *TODAY, "--status", "done"])
    assert tasks(capsys) == ["done old"]


def test_status_overdue(base, capsys):
    main(["list", *TODAY, "--status", "overdue"])
    assert tasks(capsys) == ["overdue one", "due on cutoff"]


def test_invalid_status_is_rejected(base, capsys):
    with pytest.raises(SystemExit) as err:
        main(["list", "--status", "late"])
    assert err.value.code != 0


def test_due_before_is_strict_and_skips_undated_items(base, capsys):
    assert main(["list", *TODAY, "--due-before", "2026-10-01"]) == 0
    # the item due exactly on the cutoff is not before it; no-date and raw-date items never match
    assert tasks(capsys) == ["done old", "overdue one"]


def test_due_before_includes_done_items(base, capsys):
    main(["list", *TODAY, "--due-before", "2026-12-31"])
    out = tasks(capsys)
    assert "done old" in out and "no date" not in out and "raw date" not in out


@pytest.mark.parametrize("bad", ["10/01/2026", "2026-13-01", "2026-02-30", "20261001", "soon", ""])
def test_due_before_with_an_invalid_date_errors(base, capsys, bad):
    assert main(["list", *TODAY, "--due-before", bad]) != 0
    captured = capsys.readouterr()
    assert captured.out == "" and captured.err.startswith("error:") and "--due-before" in captured.err
