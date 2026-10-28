import pytest

from actiontrack.people import UNASSIGNED, LookupFailure, People


@pytest.fixture
def people():
    p = People()
    p.learn([
        "Priya Nair", "Priya Shah", "Rahul Mehta", "Rahul Verma", "Anita Desai",
        "Sam Okafor", "Meera Iyer", "Karan Joshi", "Lena Fischer",
    ])
    return p


def test_full_name_is_case_insensitive(people):
    assert people.find("Priya Nair") == "Priya Nair"
    assert people.find("priya nair") == "Priya Nair"
    assert people.find("  PRIYA   NAIR ") == "Priya Nair"


def test_unique_first_name_finds_the_person(people):
    assert people.find("Anita") == "Anita Desai"
    assert people.find("anita") == "Anita Desai"


@pytest.mark.parametrize("first, who", [("Priya", ["Priya Nair", "Priya Shah"]),
                                        ("Rahul", ["Rahul Mehta", "Rahul Verma"])])
def test_shared_first_name_fails_listing_the_candidates(people, first, who):
    with pytest.raises(LookupFailure) as err:
        people.find(first)
    assert all(name in str(err.value) for name in who)
    assert err.value.matches == who


def test_unknown_name_fails(people):
    with pytest.raises(LookupFailure) as err:
        people.find("Zed")
    assert "Zed" in str(err.value) and err.value.matches == []


def test_unassigned_only_where_allowed(people):
    assert people.find("unassigned", allow_unassigned=True) == UNASSIGNED
    assert people.find("Unassigned", allow_unassigned=True) == UNASSIGNED
    with pytest.raises(LookupFailure):
        people.find("unassigned")
