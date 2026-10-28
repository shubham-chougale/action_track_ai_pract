from pathlib import Path

from actiontrack.scanner import scan_folder

ROOT = Path(__file__).parents[1]
FIXTURES = Path(__file__).parent / "fixtures" / "notes"


def test_sample_folder_skips_exactly_four_with_reasons():
    result = scan_folder(ROOT / "notes")
    assert {s.name: s.reason for s in result.skipped} == {
        "2026-09-09-notes-final-v2.md": "empty",
        "scratch.md": "binary",
        "untitled.md": "missing date",
        "2026-10-03-sales-pipeline.md": "invalid date",
    }
    assert len(result.notes) == 31


def test_passed_notes_carry_text_and_metadata():
    result = scan_folder(ROOT / "notes")
    by_name = {n.name: n for n in result.notes}
    standup = by_name["2026-09-16-standup.md"]
    assert standup.meta.date == "2026-09-16" and "Lena to draft" in standup.text


def test_fixture_folder_outcomes():
    result = scan_folder(FIXTURES)
    assert {s.name: s.reason for s in result.skipped} == {
        "empty.md": "empty", "binary.md": "binary", "no_date.md": "missing date", "bad_date.md": "invalid date",
    }
    assert result.scanned == 10  # 11 fixtures minus the .txt


def test_whitespace_only_file_is_empty(tmp_path):
    (tmp_path / "ws.md").write_text("  \n\t\r\n", encoding="utf-8")
    assert [(s.name, s.reason) for s in scan_folder(tmp_path).skipped] == [("ws.md", "empty")]


def test_non_utf8_file_is_skipped_not_crashed(tmp_path):
    (tmp_path / "latin.md").write_bytes("# Meeting: caf\xe9\nDate: 2026-10-05\n".encode("latin-1"))
    (tmp_path / "ok.md").write_text("# Meeting: X\nDate: 2026-10-05\n", encoding="utf-8")
    result = scan_folder(tmp_path)
    assert [n.name for n in result.notes] == ["ok.md"]
    assert result.skipped[0].name == "latin.md" and "UTF-8" in result.skipped[0].reason


def test_utf8_bom_note_is_fine(tmp_path):
    (tmp_path / "bom.md").write_bytes(b"\xef\xbb\xbf# Meeting: X\nDate: 2026-10-05\n")
    assert [n.name for n in scan_folder(tmp_path).notes] == ["bom.md"]


def test_unreadable_file_does_not_stop_the_scan(tmp_path, monkeypatch):
    for name in ("a.md", "b.md", "c.md"):
        (tmp_path / name).write_text("# Meeting: X\nDate: 2026-10-05\n", encoding="utf-8")
    real = Path.read_bytes

    def flaky(self):
        if self.name == "b.md":
            raise PermissionError("denied")
        return real(self)

    monkeypatch.setattr(Path, "read_bytes", flaky)
    result = scan_folder(tmp_path)
    assert [n.name for n in result.notes] == ["a.md", "c.md"]
    assert [(s.name, s.reason.split(":")[0]) for s in result.skipped] == [("b.md", "unreadable")]
