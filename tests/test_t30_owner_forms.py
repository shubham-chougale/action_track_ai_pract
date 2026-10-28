import pytest

from actiontrack.owners import RESOLVED, resolve_owner
from actiontrack.people import People

ATTENDEES = ["Anita Desai", "Rahul Mehta", "Lena Fischer"]


@pytest.fixture
def people():
    p = People()
    p.learn(ATTENDEES)
    return p


@pytest.mark.parametrize("raw", ["Anita Desai", "Anita", "@anita", "anita desai", "@Anita"])
def test_forms_resolve_to_anita_desai(people, raw):
    r = resolve_owner(raw, ATTENDEES, people)
    assert (r.kind, r.owners, r.raw) == (RESOLVED, ["Anita Desai"], raw)
    assert not r.flagged
