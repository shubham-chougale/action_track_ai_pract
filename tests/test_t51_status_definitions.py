from actiontrack.listing import item_status
from actiontrack.store import Item

TODAY = "2026-10-28"


def item(**kw):
    return Item(id=1, first_seen_order=1, task="t", **kw)


def test_open_and_past_due_is_overdue():
    assert item_status(item(due="2026-10-27"), TODAY) == "overdue"


def test_due_today_is_still_open():
    assert item_status(item(due="2026-10-28"), TODAY) == "open"


def test_future_due_is_open():
    assert item_status(item(due="2026-10-29"), TODAY) == "open"


def test_done_with_a_past_date_is_done():
    assert item_status(item(due="2026-10-01", status="done"), TODAY) == "done"


def test_no_due_date_is_open():
    assert item_status(item(), TODAY) == "open"


def test_flagged_with_a_past_date_is_never_overdue():
    flagged = item(due="2026-10-01", flagged=True, flag_reason="ambiguous owner")
    assert item_status(flagged, TODAY) == "open"


def test_unresolved_date_is_never_overdue():
    unresolved = item(due_raw="by end of month", flagged=True, flag_reason="unresolved date")
    assert item_status(unresolved, TODAY) == "open"


def test_flagged_done_item_is_done():
    assert item_status(item(status="done", flagged=True), TODAY) == "done"
