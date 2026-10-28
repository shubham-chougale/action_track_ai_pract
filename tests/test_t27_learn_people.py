from pathlib import Path

from actiontrack.people import People
from actiontrack.scanner import scan_folder

SAMPLE = Path(__file__).parents[1] / "notes"

KNOWN = {
    "Priya Nair", "Priya Shah", "Rahul Mehta", "Rahul Verma", "Anita Desai",
    "Sam Okafor", "Meera Iyer", "Karan Joshi", "Lena Fischer",
}


def test_sample_folder_gives_exactly_the_nine_known_people():
    people = People.from_notes(scan_folder(SAMPLE).notes)
    assert set(people.names()) == KNOWN
    assert len(people.names()) == 9


def test_people_come_only_from_attendees(tmp_path):
    (tmp_path / "a.md").write_text(
        "# Meeting: A\nDate: 2026-09-01\nAttendees: Ann Lee, Bo Chan\n\n- [ ] Cy Dow to ship it\n",
        encoding="utf-8",
    )
    people = People.from_notes(scan_folder(tmp_path).notes)
    assert people.names() == ["Ann Lee", "Bo Chan"]


def test_repeated_attendees_are_one_person():
    people = People()
    people.learn(["Ann Lee", "Bo Chan"])
    people.learn(["Ann Lee"])
    assert people.names() == ["Ann Lee", "Bo Chan"]
