import itertools

from actiontrack.merge import Mention, merge_mention, merge_mentions
from actiontrack.store import Store


def m(date, done, file=None):
    return Mention(
        owners=[{"kind": "person", "name": "Priya Nair"}], task="send the quote",
        original_line="- [x] send the quote" if done else "- [ ] send the quote",
        source={"file": file or f"{date}.md", "date": date, "title": "T"}, done=done,
    )


def final(tmp_path, mentions):
    tmp_path.mkdir(exist_ok=True)
    store = Store(tmp_path)
    merge_mentions(store, mentions)
    (item,) = store.all()
    return item


def test_later_tick_sets_done(tmp_path):
    assert final(tmp_path, [m("2026-09-01", False), m("2026-09-08", True)]).status == "done"


def test_later_open_after_done_reopens(tmp_path):
    item = final(tmp_path, [m("2026-09-01", False), m("2026-09-08", True), m("2026-09-15", False)])
    assert item.status == "open"


def test_order_of_processing_does_not_matter(tmp_path):
    mentions = [m("2026-09-01", False), m("2026-09-08", True), m("2026-09-15", False)]
    for n, perm in enumerate(itertools.permutations(mentions)):
        assert final(tmp_path / str(n), list(perm)).status == "open"
    mentions = [m("2026-09-01", False), m("2026-09-08", False), m("2026-09-15", True)]
    for n, perm in enumerate(itertools.permutations(mentions)):
        assert final(tmp_path / f"b{n}", list(perm)).status == "done"


def test_file_order_does_not_decide_which_note_is_latest(tmp_path):
    # "z.md" sorts last by file name but is the earlier meeting.
    item = final(tmp_path, [m("2026-09-08", True, "a.md"), m("2026-09-01", False, "z.md")])
    assert item.status == "done"


def test_ids_follow_date_order_not_input_order(tmp_path):
    store = Store(tmp_path)
    late = Mention(owners=[{"kind": "person", "name": "A B"}], task="later thing",
                   original_line="x", source={"file": "a.md", "date": "2026-09-08", "title": "T"})
    early = Mention(owners=[{"kind": "person", "name": "A B"}], task="earlier thing",
                    original_line="y", source={"file": "z.md", "date": "2026-09-01", "title": "T"})
    merge_mentions(store, [late, early])
    assert [i.task for i in store.all()] == ["earlier thing", "later thing"]


def test_late_arriving_older_note_does_not_override_a_newer_one(tmp_path):
    store = Store(tmp_path)
    merge_mention(store, m("2026-09-15", True))
    assert merge_mention(store, m("2026-09-01", False)) == "merged"
    assert store.all()[0].status == "done"
