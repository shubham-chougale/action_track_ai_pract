from actiontrack.merge import Mention, merge_mention
from actiontrack.store import Store


def _mention(owner, task, date="2026-09-01", file="a.md", **kw):
    owners = [{"kind": "person", "name": n} if isinstance(n, str) else n for n in owner]
    return Mention(
        owners=owners, task=task, original_line=f"- [ ] {task}",
        source={"file": file, "date": date, "title": "T"}, **kw,
    )


def test_same_wording_different_owners_stay_two_items(tmp_path):
    store = Store(tmp_path)
    assert merge_mention(store, _mention(["Priya Nair"], "send the quote")) == "new"
    assert merge_mention(store, _mention(["Priya Shah"], "send the quote", "2026-09-08", "b.md")) == "new"
    assert [i.id for i in store.all()] == [1, 2]


def test_same_owners_near_identical_wording_merge(tmp_path):
    store = Store(tmp_path)
    merge_mention(store, _mention(["Priya Nair"], "send the revised quote"))
    result = merge_mention(store, _mention(["Priya Nair"], "send revised quote.", "2026-09-08", "b.md"))
    assert result == "merged"
    (item,) = store.all()
    assert [s["file"] for s in item.sources] == ["a.md", "b.md"]


def test_same_owners_clearly_different_wording_stay_apart(tmp_path):
    store = Store(tmp_path)
    merge_mention(store, _mention(["Priya Nair"], "send the revised quote"))
    assert merge_mention(store, _mention(["Priya Nair"], "book the offsite venue", "2026-09-08", "b.md")) == "new"


def test_co_owner_sets_must_match_in_any_order(tmp_path):
    store = Store(tmp_path)
    merge_mention(store, _mention(["Anita Desai", "Rahul Mehta"], "agree on the API"))
    assert merge_mention(store, _mention(["Rahul Mehta", "Anita Desai"], "agree on API", "2026-09-08", "b.md")) == "merged"
    assert merge_mention(store, _mention(["Anita Desai"], "agree on the API", "2026-09-09", "c.md")) == "new"


def test_unresolved_owners_match_only_on_the_same_raw_text(tmp_path):
    store = Store(tmp_path)
    priya = [{"kind": "ambiguous", "raw": "Priya"}]
    rahul = [{"kind": "ambiguous", "raw": "Rahul"}]
    merge_mention(store, _mention(priya, "own the hiring plan"))
    assert merge_mention(store, _mention(rahul, "own the hiring plan", "2026-09-08", "b.md")) == "new"
    assert merge_mention(store, _mention(priya, "own the hiring plan", "2026-09-09", "c.md")) == "merged"
