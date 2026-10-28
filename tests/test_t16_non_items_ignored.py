from pathlib import Path

from actiontrack.extract import extract_items

OFFSITE = Path(__file__).parent.parent / "notes" / "2026-09-30-q4-offsite.md"


def test_table_row_and_action_line_produce_no_items():
    lines = [i.line for i in extract_items(OFFSITE.read_text(encoding="utf-8"))]
    assert not any("Refresh the brand kit" in line for line in lines)
    assert not any("circulate the offsite summary" in line for line in lines)
    assert all(line.lstrip()[0] in "-*+" for line in lines)


def test_offsite_has_exactly_its_seven_checkbox_items():
    assert len(extract_items(OFFSITE.read_text(encoding="utf-8"))) == 7


def test_table_row_with_checkbox_text_and_action_prefix_are_ignored():
    text = "| Owner | - [ ] x |\nACTION: - [ ] Karan to do y\nACTION: Karan to do z\n"
    assert extract_items(text) == []
