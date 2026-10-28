from acceptance_support import ingest_sample, listed


def test_no_owner_items_are_unassigned(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    tasks = [r["task"] for r in listed(capsys, "--owner", "unassigned")]
    for text in ("update the CRM notes", "write the design-system changelog", "submit", "decide"):
        assert any(text in t for t in tasks), text
    everyone = listed(capsys)
    for row in everyone:
        if row["owners"] == ["unassigned"]:
            assert row["task"] in tasks
