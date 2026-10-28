from actiontrack.store import Store

SRC1 = {"file": "a.md", "meeting_date": "2026-09-01", "meeting_title": "A"}
SRC2 = {"file": "b.md", "meeting_date": "2026-09-08", "meeting_title": "B"}


def test_add_source_keeps_id_order_and_earlier_sources(tmp_path):
    store = Store(tmp_path)
    store.add(task="x", sources=[SRC1])
    item = store.add(task="y", sources=[SRC1])
    store.add_source(item.id, SRC2)

    got = Store(tmp_path).get(item.id)
    assert got.id == item.id and got.first_seen_order == 2
    assert got.sources == [SRC1, SRC2]


def test_add_source_does_not_duplicate_an_existing_source(tmp_path):
    store = Store(tmp_path)
    item = store.add(task="x", sources=[SRC1])
    store.add_source(item.id, SRC1)
    assert Store(tmp_path).get(item.id).sources == [SRC1]


def test_update_changes_status_and_due_only(tmp_path):
    store = Store(tmp_path)
    item = store.add(task="x", sources=[SRC1], due="2026-09-11", flag_reason="r")
    store.update(item.id, status="done", due="2026-09-18")

    got = Store(tmp_path).get(item.id)
    assert (got.status, got.due) == ("done", "2026-09-18")
    assert got.task == "x" and got.sources == [SRC1] and got.flag_reason == "r"
    assert (got.id, got.first_seen_order) == (item.id, item.first_seen_order)
