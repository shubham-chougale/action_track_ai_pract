from acceptance_support import NOTES, ingest_sample

SKIPPED = {
    "2026-09-09-notes-final-v2.md": "empty",
    "scratch.md": "binary",
    "untitled.md": "missing date",
    "2026-10-03-sales-pipeline.md": "invalid date",
}


def test_ingest_skips_exactly_the_four_malformed_notes(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    code, out, _ = ingest_sample(capsys)
    assert code == 0
    skipped = out.split("Skipped files:")[1].split("Flagged")[0]
    lines = [line.strip() for line in skipped.strip().splitlines()]
    assert len(lines) == 4
    for name, reason in SKIPPED.items():
        assert f"{name}: {reason}" in lines
    assert "Files ingested:  31" in out and "Files skipped:   4" in out


def test_the_txt_file_is_ignored_silently(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert list(NOTES.glob("*.txt"))
    _, out, err = ingest_sample(capsys)
    assert ".txt" not in out + err and "Files scanned:   35" in out
