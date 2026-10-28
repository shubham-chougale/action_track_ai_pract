from pathlib import Path

from actiontrack.metadata import parse_metadata

FIXTURES = Path(__file__).parent / "fixtures" / "notes"


def test_style_a_returns_title_date_and_attendees():
    meta = parse_metadata((FIXTURES / "header_style_a.md").read_text(encoding="utf-8"))
    assert meta.reason is None
    assert meta.title == "Style A"
    assert meta.date == "2026-10-05"
    assert meta.attendees == ["Priya Nair", "Rahul Mehta"]


def test_style_a_with_bracketed_attendees():
    meta = parse_metadata("# Meeting: X\nDate: 2026-10-05\nAttendees: [Anita Desai, Sam Okafor]\n")
    assert meta.attendees == ["Anita Desai", "Sam Okafor"]


def test_crlf_and_bom_are_tolerated():
    meta = parse_metadata("﻿# Meeting: X\r\nDate: 2026-10-05\r\nAttendees: A B, C D\r\n")
    assert (meta.title, meta.date, meta.attendees) == ("X", "2026-10-05", ["A B", "C D"])


def test_header_fields_after_the_body_starts_are_ignored():
    meta = parse_metadata("# Meeting: X\nDate: 2026-10-05\n\n## Notes\nDate: 2030-01-01\nAttendees: Nobody\n")
    assert meta.date == "2026-10-05" and meta.attendees == []
