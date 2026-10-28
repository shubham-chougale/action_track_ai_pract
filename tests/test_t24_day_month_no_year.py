import pytest

from actiontrack.duedate import resolve_due

MEETING = "2026-09-08"


@pytest.mark.parametrize("phrase, expected", [
    ("by 10 Sep", "2026-09-10"),
    ("by Oct 3rd", "2026-10-03"),
    ("Oct 3rd", "2026-10-03"),
    ("15 October", "2026-10-15"),
    ("by 7 Oct", "2026-10-07"),
    ("by Oct 5th", "2026-10-05"),
    ("by 2 Oct", "2026-10-02"),
    ("due 15 October", "2026-10-15"),
    ("by 1st Nov", "2026-11-01"),
    ("by 22 Sept", "2026-09-22"),
])
def test_nearest_date_on_or_after_the_meeting(phrase, expected):
    assert resolve_due(phrase, MEETING).date == expected


def test_a_date_on_the_meeting_day_stays_that_day():
    assert resolve_due("8 Sep", MEETING).date == "2026-09-08"


def test_a_date_already_past_this_year_rolls_to_next_year():
    assert resolve_due("by 10 Aug", MEETING).date == "2027-08-10"
    assert resolve_due("7 Sep", MEETING).date == "2027-09-07"


def test_december_meeting_with_january_date_means_next_january():
    assert resolve_due("5 Jan", "2026-12-20").date == "2027-01-05"
    assert resolve_due("by Jan 5th", "2026-12-20").date == "2027-01-05"
    assert resolve_due("by 28 Dec", "2026-12-20").date == "2026-12-28"


def test_leap_day_looks_ahead_to_the_next_leap_year():
    assert resolve_due("29 Feb", "2026-09-08").date == "2028-02-29"


def test_impossible_day_gives_no_date():
    assert resolve_due("by 31 Sep", MEETING).date is None
