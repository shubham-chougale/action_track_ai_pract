from actiontrack.followup import select_items
from actiontrack.store import Store
from listing_support import person, seed

TODAY = "2026-10-28"


def tasks(base, owner="Priya Nair"):
    return [i.task for i in select_items(Store(base).all(), owner, TODAY)]


def test_open_and_overdue_items_only(tmp_path):
    seed(tmp_path, task="overdue one", due="2026-10-10")
    seed(tmp_path, task="open one", due="2026-11-10")
    seed(tmp_path, task="no date")
    seed(tmp_path, task="finished", due="2026-10-10", status="done")
    assert sorted(tasks(tmp_path)) == ["no date", "open one", "overdue one"]


def test_unassigned_ambiguous_and_flagged_are_excluded(tmp_path):
    seed(tmp_path, task="mine")
    seed(tmp_path, task="nobody", owners=[{"kind": "unassigned", "raw": "Someone"}])
    seed(tmp_path, task="unsure", owners=[{"kind": "ambiguous", "raw": "Priya"}])
    seed(tmp_path, task="decoy", flagged=True, flag_reason="template")
    assert tasks(tmp_path) == ["mine"]


def test_other_owners_items_are_excluded(tmp_path):
    seed(tmp_path, task="shah's", owners=[person("Priya Shah")])
    seed(tmp_path, task="mine")
    assert tasks(tmp_path) == ["mine"]


def test_co_owned_item_goes_to_each_co_owner(tmp_path):
    seed(tmp_path, task="joint", owners=[person("Anita Desai"), person("Rahul Mehta")])
    assert tasks(tmp_path, "Anita Desai") == ["joint"]
    assert tasks(tmp_path, "Rahul Mehta") == ["joint"]
    assert tasks(tmp_path, "Rahul Verma") == []


def test_merged_item_appears_once(tmp_path):
    seed(tmp_path, task="repeated", sources=[
        {"file": "a.md", "date": "2026-10-01", "title": "A"},
        {"file": "b.md", "date": "2026-10-08", "title": "B"}])
    assert tasks(tmp_path) == ["repeated"]


def test_overdue_sorted_before_later_dates(tmp_path):
    seed(tmp_path, task="later", due="2026-12-01")
    seed(tmp_path, task="sooner", due="2026-10-01")
    assert tasks(tmp_path) == ["sooner", "later"]
