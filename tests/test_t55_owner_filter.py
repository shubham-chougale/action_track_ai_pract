import re
import shutil
from pathlib import Path

import pytest

from actiontrack.cli import main
from actiontrack.store import Store
from listing_support import person, seed, table_rows

TODAY = ["--today", "2026-10-28"]
FIXTURES = Path(__file__).parent / "fixtures" / "notes"
PEOPLE = ["Priya Nair", "Priya Shah", "Anita Desai", "Rahul Mehta"]


@pytest.fixture
def base(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Store(tmp_path).learn_people(PEOPLE)
    seed(tmp_path, task="nair task", owners=[person("Priya Nair")])
    seed(tmp_path, task="shah task", owners=[person("Priya Shah")])
    seed(tmp_path, task="shared task", owners=[person("Anita Desai"), person("Rahul Mehta")])
    seed(tmp_path, task="nobody task", owners=[{"kind": "unassigned", "raw": None}])
    seed(tmp_path, task="vague task", owners=[{"kind": "ambiguous", "raw": "Priya"}], flagged=True)
    return tmp_path


def tasks(capsys):
    return [re.split(r"\s{2,}", r.strip())[2] for r in table_rows(capsys.readouterr().out)]


def test_full_name_filters_case_insensitively(base, capsys):
    assert main(["list", *TODAY, "--owner", "priya NAIR"]) == 0
    assert tasks(capsys) == ["nair task"]


def test_unique_first_name_works(base, capsys):
    assert main(["list", *TODAY, "--owner", "anita"]) == 0
    assert tasks(capsys) == ["shared task"]


def test_shared_first_name_fails_listing_both_people(base, capsys):
    assert main(["list", *TODAY, "--owner", "Priya"]) != 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Priya Nair" in captured.err and "Priya Shah" in captured.err


def test_co_owned_item_matches_each_owner(base, capsys):
    for name in ("Anita Desai", "Rahul Mehta"):
        main(["list", *TODAY, "--owner", name])
        assert tasks(capsys) == ["shared task"]


def test_unassigned_shows_only_unassigned_items(base, capsys):
    assert main(["list", *TODAY, "--owner", "unassigned"]) == 0
    assert tasks(capsys) == ["nobody task"]


def test_ambiguous_owner_item_is_never_given_to_a_named_person(base, capsys):
    main(["list", *TODAY, "--owner", "Priya Shah"])
    assert "vague task" not in capsys.readouterr().out


def test_unknown_name_is_an_error(base, capsys):
    assert main(["list", *TODAY, "--owner", "Zed"]) != 0
    assert "no known person" in capsys.readouterr().err


def test_ingest_remembers_attendees_for_the_lookup(tmp_path, monkeypatch, capsys):
    notes = tmp_path / "notes"
    shutil.copytree(FIXTURES, notes)
    monkeypatch.chdir(tmp_path)
    main(["ingest", str(notes)])
    capsys.readouterr()
    assert main(["list", *TODAY, "--owner", "Priya"]) != 0
    assert "Priya Nair" in capsys.readouterr().err
    assert main(["list", *TODAY, "--owner", "Priya Nair"]) == 0
