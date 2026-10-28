import pytest

from actiontrack.duedate import resolve_due

TUE = "2026-09-01"
MON = "2026-09-07"


@pytest.mark.parametrize("phrase", ["Friday", "by Friday", "by Fri", "FRIDAY", "by fri"])
def test_weekday_after_a_tuesday_meeting(phrase):
    assert resolve_due(phrase, TUE).date == "2026-09-04"


def test_weekday_is_always_strictly_after_the_meeting():
    assert resolve_due("by Mon", MON).date == "2026-09-14"  # same weekday: 7 days later
    assert resolve_due("Tuesday", TUE).date == "2026-09-08"
    assert resolve_due("Wed", TUE).date == "2026-09-02"  # next day
    assert resolve_due("Monday", TUE).date == "2026-09-07"  # wraps into next week


@pytest.mark.parametrize(
    "phrase, expected",
    [("Mon", "2026-09-07"), ("Tue", "2026-09-08"), ("Wed", "2026-09-02"), ("Thu", "2026-09-03"),
     ("Thursday", "2026-09-03"), ("Sat", "2026-09-05"), ("Sunday", "2026-09-06"), ("Wednesday", "2026-09-02")],
)
def test_all_weekday_spellings(phrase, expected):
    assert resolve_due(phrase, TUE).date == expected


def test_next_weekday_is_one_specific_date():
    r = resolve_due("by next Tuesday", TUE)
    assert r.date == "2026-09-08"
    assert resolve_due("by next Tuesday", TUE) == r


def test_next_weekday_means_the_following_calendar_week():
    # Tue 2026-09-01 + "next Friday": Friday of the week after, not this week's Friday.
    assert resolve_due("next Friday", TUE).date == "2026-09-11"
    assert resolve_due("next Monday", TUE).date == "2026-09-07"
    assert resolve_due("next Monday", MON).date == "2026-09-14"
