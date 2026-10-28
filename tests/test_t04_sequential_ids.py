from actiontrack.store import Store


def test_ids_are_sequential_and_survive_reopen(tmp_path):
    store = Store(tmp_path)
    assert [store.add(task=t).id for t in ("a", "b", "c")] == [1, 2, 3]
    reopened = Store(tmp_path)
    assert [i.id for i in reopened.all()] == [1, 2, 3]
    assert reopened.add(task="d").id == 4


def test_first_seen_order_follows_creation(tmp_path):
    store = Store(tmp_path)
    for t in ("a", "b", "c"):
        store.add(task=t)
    assert [i.first_seen_order for i in Store(tmp_path).all()] == [1, 2, 3]
