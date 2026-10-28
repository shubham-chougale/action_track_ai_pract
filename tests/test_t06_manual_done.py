from actiontrack.store import Store


def test_manual_done_survives_note_update_setting_open(tmp_path):
    store = Store(tmp_path)
    item = store.add(task="x")
    store.mark_done(item.id)
    store.update(item.id, status="open")

    got = Store(tmp_path).get(item.id)
    assert got.status == "done" and got.status_manual is True


def test_note_set_done_is_not_manual_and_can_reopen(tmp_path):
    store = Store(tmp_path)
    item = store.add(task="x")
    store.update(item.id, status="done")
    assert Store(tmp_path).get(item.id).status_manual is False
    store.update(item.id, status="open")
    assert Store(tmp_path).get(item.id).status == "open"


def test_manual_done_still_accepts_other_updates(tmp_path):
    store = Store(tmp_path)
    item = store.add(task="x", due="2026-09-11")
    store.mark_done(item.id)
    store.update(item.id, status="open", due="2026-09-18")
    got = Store(tmp_path).get(item.id)
    assert (got.status, got.due) == ("done", "2026-09-18")
