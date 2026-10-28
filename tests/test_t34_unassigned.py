import pytest

from actiontrack.extract import extract_items
from actiontrack.owners import UNASSIGNED, resolve_owner
from actiontrack.people import People


@pytest.fixture
def people():
    p = People()
    p.learn(["Anita Desai", "Lena Fischer"])
    return p


@pytest.mark.parametrize("raw", ["Someone", "TBD", "Everyone", "Team", "Owner", "someone", "TEAM", "tbd"])
def test_non_person_owner_is_unassigned_with_wording_kept(people, raw):
    r = resolve_owner(raw, ["Anita Desai"], people)
    assert (r.kind, r.owners, r.raw, r.flagged) == (UNASSIGNED, [], raw, False)


@pytest.mark.parametrize("raw", [None, ""])
def test_no_owner_is_unassigned(people, raw):
    r = resolve_owner(raw, ["Anita Desai"], people)
    assert (r.kind, r.owners, r.flagged) == (UNASSIGNED, [], False)


def test_original_wording_survives_on_the_item(people):
    line = "- [ ] Someone to update the CRM notes"
    (item,) = extract_items(line)
    r = resolve_owner(item.owner_text, [], people)
    assert r.kind == UNASSIGNED and r.raw == "Someone"
    assert item.line == line and item.task == "update the CRM notes"


def test_line_with_no_owner(people):
    (item,) = extract_items("- [ ] Book the venue by Friday")
    r = resolve_owner(item.owner_text, [], people)
    assert r.kind == UNASSIGNED and r.raw is None and item.line.endswith("Book the venue by Friday")
