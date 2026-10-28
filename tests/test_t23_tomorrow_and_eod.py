import pytest

from actiontrack.duedate import resolve_due


@pytest.mark.parametrize("meeting, tomorrow", [
    ("2026-09-01", "2026-09-02"), ("2026-09-30", "2026-10-01"), ("2026-12-31", "2027-01-01"),
    ("2028-02-28", "2028-02-29"),
])
def test_tomorrow_is_meeting_plus_one(meeting, tomorrow):
    assert resolve_due("tomorrow", meeting).date == tomorrow
    assert resolve_due("by tomorrow", meeting).date == tomorrow


def test_eod_is_the_meeting_date():
    assert resolve_due("EOD", "2026-09-01").date == "2026-09-01"
    assert resolve_due("by EOD", "2026-09-01").date == "2026-09-01"
    assert resolve_due("by eod", "2026-09-01").date == "2026-09-01"


def test_eod_tomorrow_is_meeting_plus_one():
    assert resolve_due("by EOD tomorrow", "2026-09-01").date == "2026-09-02"
    assert resolve_due("EOD tomorrow", "2026-09-30").date == "2026-10-01"


def test_today_is_the_meeting_date():
    assert resolve_due("by today", "2026-09-01").date == "2026-09-01"
