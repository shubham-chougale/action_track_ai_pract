import re

from actiontrack.followup import compose
from actiontrack.store import Store
from listing_support import seed

TODAY = "2026-10-28"


def build(base, owner="Priya Nair"):
    from actiontrack.followup import select_items
    return compose(owner, select_items(Store(base).all(), owner, TODAY), TODAY)


def test_subject_has_overdue_and_open_counts(tmp_path):
    seed(tmp_path, task="a", due="2026-10-01")
    seed(tmp_path, task="b", due="2026-10-10")
    seed(tmp_path, task="c", due="2026-12-01")
    seed(tmp_path, task="d")
    subject, _ = build(tmp_path)
    assert subject == "Action items follow-up: Priya Nair (2 overdue, 2 open)"


def test_subject_counts_equal_the_body_counts(tmp_path):
    seed(tmp_path, task="a", due="2026-10-01")
    seed(tmp_path, task="b", due="2026-12-01")
    seed(tmp_path, task="c")
    subject, body = build(tmp_path)
    n, m = map(int, re.search(r"\((\d+) overdue, (\d+) open\)", subject).groups())
    overdue_part, open_part = body.split("Open")
    assert n == overdue_part.count("\n- ") and m == open_part.count("\n- ")


def test_zero_overdue_still_in_subject(tmp_path):
    seed(tmp_path, task="c", due="2026-12-01")
    subject, _ = build(tmp_path)
    assert subject == "Action items follow-up: Priya Nair (0 overdue, 1 open)"
