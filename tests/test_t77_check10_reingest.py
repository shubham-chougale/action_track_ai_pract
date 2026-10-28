from acceptance_support import ingest_sample, listed, run


def snapshot(base):
    return {p.name: p.read_bytes() for p in (base / ".actiontrack").iterdir()}


def test_second_ingest_after_done_adds_nothing_and_changes_nothing(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    open_item = next(r for r in listed(capsys) if r["status"] == "open" and not r["flagged"])
    assert run(capsys, "done", str(open_item["id"]))[0] == 0
    before = snapshot(tmp_path)
    count = len(listed(capsys))
    code, out, _ = ingest_sample(capsys)
    assert code == 0 and "Items new:       0" in out
    assert snapshot(tmp_path) == before
    rows = listed(capsys)
    assert len(rows) == count
    assert next(r for r in rows if r["id"] == open_item["id"])["status"] == "done"
