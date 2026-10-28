from pathlib import Path

import pytest

from actiontrack.metadata import parse_metadata

ROOT = Path(__file__).parents[1]


def sample(name):
    return parse_metadata((ROOT / "notes" / name).read_text(encoding="utf-8"))


def test_untitled_is_missing_date():
    meta = sample("untitled.md")
    assert meta.reason == "missing date" and meta.date is None


def test_sales_pipeline_is_invalid_date():
    meta = sample("2026-10-03-sales-pipeline.md")
    assert meta.reason == "invalid date" and meta.date is None


def test_impossible_calendar_date_is_invalid():
    assert parse_metadata("# Meeting: X\nDate: 2026-02-30\n").reason == "invalid date"


@pytest.mark.parametrize("value", ["2026-13-01", "26-09-01", "31 June 2026", "Someday 5 Foo 2026", "2026/09/01"])
def test_other_unusable_dates_are_invalid(value):
    assert parse_metadata(f"# Meeting: X\nDate: {value}\n").reason == "invalid date"


def test_empty_date_value_is_missing():
    assert parse_metadata("# Meeting: X\nDate:\n").reason == "missing date"


def test_no_attendees_and_no_title_still_valid():
    meta = parse_metadata("Date: 2026-09-23\n\nsome text\n")
    assert (meta.title, meta.attendees, meta.date, meta.reason) == (None, [], "2026-09-23", None)


def test_sample_note_without_attendees_line_is_usable():
    assert sample("2026-09-23-standup.md").date == "2026-09-23"


def test_long_form_sample_dates_are_valid():
    assert sample("2026-09-09-qa-standup.md").date == "2026-09-09"
    assert sample("2026-09-14-onboarding-flow-design.md").date == "2026-09-14"
