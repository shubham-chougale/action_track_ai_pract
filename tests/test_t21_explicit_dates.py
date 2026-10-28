from actiontrack.duedate import resolve_due

MEETING = "2026-09-01"


def test_iso_date_is_used_as_is():
    assert resolve_due("by 2026-09-08", MEETING).date == "2026-09-08"
    assert resolve_due("2026-09-08", MEETING).date == "2026-09-08"
    assert resolve_due("on 2026-10-14", MEETING).date == "2026-10-14"


def test_iso_date_before_the_meeting_is_kept():
    assert resolve_due("by 2026-08-20", MEETING).date == "2026-08-20"


def test_weekday_day_month_uses_the_explicit_date():
    assert resolve_due("Wed 16 Sep", MEETING).date == "2026-09-16"
    assert resolve_due("by Wed 16 Sep", MEETING).date == "2026-09-16"
    assert resolve_due("for Saturday 10 Oct", MEETING).date == "2026-10-10"


def test_explicit_year_is_honoured():
    assert resolve_due("by 5 Jan 2027", MEETING).date == "2027-01-05"


def test_result_keeps_the_phrase():
    assert resolve_due("by 2026-09-08", MEETING).phrase == "by 2026-09-08"


def test_no_phrase_means_no_date():
    r = resolve_due(None, MEETING)
    assert (r.date, r.phrase, r.flag) == (None, None, None)
