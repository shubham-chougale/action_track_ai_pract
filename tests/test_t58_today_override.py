import re
from datetime import date

import pytest

import actiontrack.cli as cli
from actiontrack.cli import main
from listing_support import seed, table_rows


@pytest.fixture
def base(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    seed(tmp_path, task="soon", due="2026-10-10")
    seed(tmp_path, task="later", due="2026-11-10")
    return tmp_path


def overdue(capsys, *args):
    assert main(["list", "--status", "overdue", "--json", *args]) == 0
    out = capsys.readouterr().out
    return re.findall(r'"task": "(\w+)"', out)


def test_two_today_values_give_different_overdue_sets(base, capsys):
    assert overdue(capsys, "--today", "2026-10-01") == []
    assert overdue(capsys, "--today", "2026-10-28") == ["soon"]
    assert overdue(capsys, "--today", "2026-12-01") == ["soon", "later"]


def test_without_today_the_computers_date_is_used(base, capsys, monkeypatch):
    class FakeDate(date):
        @classmethod
        def today(cls):
            return cls(2026, 11, 1)

    monkeypatch.setattr(cli, "date", FakeDate)
    assert overdue(capsys) == ["soon"]
    monkeypatch.setattr(cli, "date", type("D2", (FakeDate,), {"today": classmethod(lambda c: date(2027, 1, 1))}))
    assert overdue(capsys) == ["soon", "later"]


def test_table_status_column_follows_today(base, capsys):
    main(["list", "--today", "2026-10-28"])
    rows = table_rows(capsys.readouterr().out)
    assert "overdue" in next(r for r in rows if "soon" in r)
    assert "open" in next(r for r in rows if "later" in r)


@pytest.mark.parametrize("bad", ["10/28/2026", "2026-02-30", "tomorrow"])
def test_invalid_today_is_an_error(base, capsys, bad):
    assert main(["list", "--today", bad]) != 0
    captured = capsys.readouterr()
    assert captured.out == "" and "--today" in captured.err
