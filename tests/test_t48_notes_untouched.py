import hashlib
from pathlib import Path

from actiontrack.cli import main

SAMPLE = Path(__file__).parents[1] / "notes"


def hashes(folder):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.iterdir()) if p.is_file()}


def test_sample_notes_are_byte_identical_after_ingest(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    before = hashes(SAMPLE)
    assert len(before) == 36
    main(["ingest", str(SAMPLE)])
    main(["ingest", str(SAMPLE)])
    assert hashes(SAMPLE) == before


def test_no_files_are_added_to_the_notes_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    before = sorted(p.name for p in SAMPLE.iterdir())
    main(["ingest", str(SAMPLE)])
    assert sorted(p.name for p in SAMPLE.iterdir()) == before
    assert not (SAMPLE / ".actiontrack").exists()
