from acceptance_support import find, ingest_sample, listed


def test_offsite_items_are_flagged_ambiguous(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    rows = listed(capsys)
    for text, raw in (("own the hiring plan", "Priya"), ("prepare the architecture overview", "Rahul")):
        item = find(rows, text)
        assert item["owners"] == [f"{raw} (ambiguous)"]
        assert item["flagged"] and "ambiguous owner" in item["flag_reason"]
        assert item["sources"][0]["file"] == "2026-09-30-q4-offsite.md"
