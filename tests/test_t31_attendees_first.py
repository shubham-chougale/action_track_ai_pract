import pytest

from actiontrack.owners import RESOLVED, UNKNOWN, resolve_owner
from actiontrack.people import People


@pytest.fixture
def people():
    p = People()
    p.learn(["Priya Nair", "Priya Shah", "Rahul Mehta", "Anita Desai"])
    return p


def test_unique_attendee_wins_over_another_person_with_the_same_first_name(people):
    r = resolve_owner("Priya", ["Priya Shah", "Anita Desai"], people)
    assert (r.kind, r.owners) == (RESOLVED, ["Priya Shah"])
    r = resolve_owner("priya", ["Priya Nair"], people)
    assert r.owners == ["Priya Nair"]


def test_no_attendee_match_falls_back_to_the_single_known_person(people):
    r = resolve_owner("Rahul", ["Anita Desai"], people)
    assert (r.kind, r.owners) == (RESOLVED, ["Rahul Mehta"])


def test_attendees_may_be_empty(people):
    assert resolve_owner("Anita", [], people).owners == ["Anita Desai"]


def test_no_match_anywhere_is_unknown_and_keeps_raw_text(people):
    r = resolve_owner("Zed", ["Anita Desai"], people)
    assert (r.kind, r.owners, r.raw, r.flagged) == (UNKNOWN, [], "Zed", True)
