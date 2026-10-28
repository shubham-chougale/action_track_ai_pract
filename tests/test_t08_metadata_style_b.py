from pathlib import Path

from actiontrack.metadata import Metadata, parse_metadata

ROOT = Path(__file__).parents[1]
FIXTURES = Path(__file__).parent / "fixtures" / "notes"


def test_sample_standup_matches_style_a_shape():
    meta = parse_metadata((ROOT / "notes" / "2026-09-16-standup.md").read_text(encoding="utf-8"))
    assert isinstance(meta, Metadata) and meta.reason is None
    assert meta.title == "Team standup"
    assert meta.date == "2026-09-16"
    assert meta.attendees == ["Anita Desai", "Lena Fischer", "Meera Iyer"]


def test_style_b_fixture():
    meta = parse_metadata((FIXTURES / "header_style_b.md").read_text(encoding="utf-8"))
    assert (meta.title, meta.date) == ("Style B", "2026-10-06")
    assert meta.attendees == ["Priya Shah", "Rahul Verma"]


def test_quoted_front_matter_values():
    meta = parse_metadata('---\ntitle: "Quarterly sync"\ndate: "2026-10-06"\nattendees: ["A B", \'C D\']\n---\n')
    assert (meta.title, meta.date, meta.attendees) == ("Quarterly sync", "2026-10-06", ["A B", "C D"])


def test_front_matter_without_attendees_or_title_is_usable():
    meta = parse_metadata("---\ndate: 2026-10-06\n---\nbody\n")
    assert (meta.title, meta.date, meta.attendees, meta.reason) == (None, "2026-10-06", [], None)
