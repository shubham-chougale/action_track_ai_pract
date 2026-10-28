import pytest

from actiontrack.owners import RESOLVED, UNKNOWN, resolve_owner
from actiontrack.people import People


@pytest.fixture
def people():
    p = People()
    p.learn(["Priya Nair", "Priya Shah", "Rahul Mehta", "Rahul Verma"])
    return p


@pytest.mark.parametrize("raw, who", [
    ("Priya N.", "Priya Nair"), ("Priya S.", "Priya Shah"),
    ("priya n.", "Priya Nair"), ("Priya N", "Priya Nair"), ("Rahul V.", "Rahul Verma"),
])
def test_first_name_and_initial(people, raw, who):
    # Both Priyas attend, so only the initial can tell them apart.
    r = resolve_owner(raw, ["Priya Nair", "Priya Shah"], people)
    assert (r.kind, r.owners, r.raw) == (RESOLVED, [who], raw)


def test_initial_matching_nobody_is_unknown(people):
    r = resolve_owner("Priya X.", ["Priya Nair", "Priya Shah"], people)
    assert (r.kind, r.owners, r.raw, r.flagged) == (UNKNOWN, [], "Priya X.", True)


def test_initial_with_unknown_first_name_is_unknown(people):
    assert resolve_owner("Zed N.", [], people).kind == UNKNOWN
