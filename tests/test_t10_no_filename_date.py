from actiontrack.metadata import parse_metadata


def test_filename_date_is_never_a_fallback(tmp_path):
    note = tmp_path / "2026-09-09-x.md"
    note.write_text("# Meeting: X\nAttendees: Priya Nair\n\n- [ ] Priya to do it\n", encoding="utf-8")
    meta = parse_metadata(note.read_text(encoding="utf-8"))
    assert meta.reason == "missing date" and meta.date is None
