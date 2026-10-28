import shutil
from pathlib import Path

from actiontrack.scanner import scan_folder

ROOT = Path(__file__).parents[1]
SAMPLE = ROOT / "notes"


def test_sample_folder_scans_35_md_files_and_ignores_txt():
    result = scan_folder(SAMPLE)
    assert result.scanned == 35
    seen = {n.name for n in result.notes} | {s.name for s in result.skipped}
    assert len(seen) == 35 and all(name.endswith(".md") for name in seen)
    assert "2026-09-19-offsite-draft.txt" not in seen  # silently ignored, not skipped


def test_subfolder_md_is_not_scanned(tmp_path):
    shutil.copy(SAMPLE / "2026-09-16-standup.md", tmp_path / "top.md")
    sub = tmp_path / "sub"
    sub.mkdir()
    shutil.copy(SAMPLE / "2026-09-16-standup.md", sub / "nested.md")
    result = scan_folder(tmp_path)
    assert result.scanned == 1 and [n.name for n in result.notes] == ["top.md"]


def test_directory_named_like_a_note_is_ignored(tmp_path):
    (tmp_path / "folder.md").mkdir()
    result = scan_folder(tmp_path)
    assert result.scanned == 0 and result.skipped == []


def test_scanning_never_modifies_notes(tmp_path):
    note = tmp_path / "a.md"
    note.write_text("# Meeting: X\nDate: 2026-10-05\n", encoding="utf-8")
    before = (note.read_bytes(), note.stat().st_mtime_ns)
    scan_folder(tmp_path)
    assert (note.read_bytes(), note.stat().st_mtime_ns) == before
