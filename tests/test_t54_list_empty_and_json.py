import json

import pytest

from actiontrack.cli import main
from listing_support import person, seed, table_rows

TODAY = ["--today", "2026-10-28"]


@pytest.fixture(autouse=True)
def cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_empty_store_prints_no_items_match(capsys):
    assert main(["list", *TODAY]) == 0
    assert capsys.readouterr().out.strip() == "No items match"


def test_empty_result_has_no_table_or_total(cwd, capsys):
    seed(cwd, task="x", due="2026-11-01")
    main(["list", *TODAY, "--status", "done"])
    out = capsys.readouterr().out
    assert out.strip() == "No items match" and "Total" not in out


def test_json_parses_and_matches_the_table_items(cwd, capsys):
    seed(cwd, task="late one", due="2026-11-20")
    seed(cwd, task="early one", due="2026-10-02", owners=[person("Anita Desai"), person("Rahul Mehta")])
    seed(cwd, task="undated", due_raw="by end of month", flagged=True, flag_reason="unresolved date")
    main(["list", *TODAY])
    table_ids = [int(r.split()[0]) for r in table_rows(capsys.readouterr().out)]
    assert main(["list", *TODAY, "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert [d["id"] for d in data] == table_ids
    early = next(d for d in data if d["task"] == "early one")
    assert early["owners"] == ["Anita Desai", "Rahul Mehta"]
    assert (early["due"], early["status"]) == ("2026-10-02", "overdue")
    undated = next(d for d in data if d["task"] == "undated")
    assert (undated["due"], undated["due_raw"], undated["flagged"]) == (None, "by end of month", True)
    assert early["sources"] == [{"file": "a.md", "date": "2026-10-01", "title": "A"}]


def test_json_with_no_matches_is_an_empty_list(capsys):
    assert main(["list", *TODAY, "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == []
