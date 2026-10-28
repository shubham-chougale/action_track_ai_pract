import re

import pytest

from actiontrack.cli import main
from actiontrack.store import Store
from listing_support import person, seed, table_rows

TODAY = ["--today", "2026-10-28"]


@pytest.fixture
def base(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Store(tmp_path).learn_people(["Priya Nair", "Priya Shah"])
    seed(tmp_path, task="match", due="2026-09-10")  # Priya Nair, overdue, before
    seed(tmp_path, task="wrong owner", due="2026-09-10", owners=[person("Priya Shah")])
    seed(tmp_path, task="wrong status", due="2026-09-10", status="done")
    seed(tmp_path, task="too late", due="2026-10-20")  # overdue, but not before the cutoff
    seed(tmp_path, task="no date")
    return tmp_path


def tasks(capsys):
    return [re.split(r"\s{2,}", r.strip())[2] for r in table_rows(capsys.readouterr().out)]


def test_owner_status_and_due_before_all_apply(base, capsys):
    args = ["list", *TODAY, "--owner", "Priya Nair", "--status", "overdue", "--due-before", "2026-10-01"]
    assert main(args) == 0
    assert tasks(capsys) == ["match"]


def test_each_filter_alone_returns_a_superset(base, capsys):
    main(["list", *TODAY, "--owner", "Priya Nair"])
    owner_only = set(tasks(capsys))
    main(["list", *TODAY, "--owner", "Priya Nair", "--status", "overdue"])
    with_status = set(tasks(capsys))
    assert with_status < owner_only and "match" in with_status


def test_filters_that_cannot_all_hold_give_no_items_match(base, capsys):
    main(["list", *TODAY, "--owner", "Priya Shah", "--status", "done"])
    assert capsys.readouterr().out.strip() == "No items match"


def test_total_counts_only_the_filtered_items(base, capsys):
    main(["list", *TODAY, "--owner", "Priya Nair", "--status", "overdue"])
    assert capsys.readouterr().out.rstrip().endswith("Total: 2 items")
