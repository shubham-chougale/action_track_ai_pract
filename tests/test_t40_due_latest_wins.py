from actiontrack.merge import Mention, merge_mentions
from actiontrack.store import Store


def m(date, due=None, due_raw=None):
    return Mention(
        owners=[{"kind": "person", "name": "Priya Nair"}], task="send the quote",
        original_line="- [ ] send the quote", due=due, due_raw=due_raw,
        source={"file": f"{date}.md", "date": date, "title": "T"},
    )


def final(tmp_path, mentions):
    store = Store(tmp_path)
    merge_mentions(store, mentions)
    (item,) = store.all()
    return item


def test_later_due_date_replaces_earlier(tmp_path):
    item = final(tmp_path, [m("2026-09-01", "2026-09-04"), m("2026-09-08", "2026-09-11")])
    assert item.due == "2026-09-11"


def test_earlier_note_never_overrides_a_later_due_date(tmp_path):
    item = final(tmp_path, [m("2026-09-08", "2026-09-11"), m("2026-09-01", "2026-09-04")])
    assert item.due == "2026-09-11"


def test_later_mention_without_due_keeps_existing(tmp_path):
    item = final(tmp_path, [m("2026-09-01", "2026-09-04"), m("2026-09-08")])
    assert (item.due, item.due_raw) == ("2026-09-04", None)


def test_unresolved_phrase_is_a_due_mention_and_clears_the_old_date(tmp_path):
    item = final(tmp_path, [m("2026-09-01", "2026-09-04"), m("2026-09-08", due_raw="end of month")])
    assert (item.due, item.due_raw) == (None, "end of month")


def test_later_resolved_date_clears_an_old_raw_phrase(tmp_path):
    item = final(tmp_path, [m("2026-09-01", due_raw="mid-October"), m("2026-09-08", "2026-10-15")])
    assert (item.due, item.due_raw) == ("2026-10-15", None)
