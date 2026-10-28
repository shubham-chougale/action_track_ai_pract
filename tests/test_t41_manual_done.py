from actiontrack.merge import Mention, merge_mention, merge_mentions
from actiontrack.store import Store


def m(date, done=False, due=None):
    return Mention(
        owners=[{"kind": "person", "name": "Priya Nair"}], task="send the quote",
        original_line="- [ ] send the quote", done=done, due=due,
        source={"file": f"{date}.md", "date": date, "title": "T"},
    )


def test_manual_done_survives_a_later_open_mention(tmp_path):
    store = Store(tmp_path)
    merge_mention(store, m("2026-09-01"))
    store.mark_done(1)
    assert merge_mention(store, m("2026-09-08")) == "merged"
    item = Store(tmp_path).get(1)
    assert (item.status, item.status_manual) == ("done", True)
    assert len(item.sources) == 2


def test_manual_done_still_takes_the_later_due_date(tmp_path):
    store = Store(tmp_path)
    merge_mention(store, m("2026-09-01", due="2026-09-04"))
    store.mark_done(1)
    merge_mention(store, m("2026-09-08", due="2026-09-11"))
    assert Store(tmp_path).get(1).due == "2026-09-11"


def test_manual_done_sticks_across_a_whole_reingest(tmp_path):
    store = Store(tmp_path)
    mentions = [m("2026-09-01"), m("2026-09-08")]
    merge_mentions(store, mentions)
    store.mark_done(1)
    counts = merge_mentions(Store(tmp_path), mentions)
    assert counts == {"new": 0, "merged": 0, "unchanged": 2}
    assert Store(tmp_path).get(1).status == "done"
