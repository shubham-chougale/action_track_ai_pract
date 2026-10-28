from actiontrack.people import People


def _people():
    people = People()
    people.learn(["Priya Nair", "Anita Desai"])
    return people


def test_csv_attaches_emails_by_exact_full_name(tmp_path):
    roster = tmp_path / "roster.csv"
    roster.write_text("name,email\nPriya Nair,priya.nair@example.com\n", encoding="utf-8")
    people = _people()
    people.load_roster(roster)
    assert people.email("Priya Nair") == "priya.nair@example.com"
    assert people.email("Anita Desai") is None


def test_missing_roster_file_loads_without_error(tmp_path):
    people = _people()
    people.load_roster(tmp_path / "nope.csv")
    assert people.email("Priya Nair") is None


def test_row_for_unknown_name_adds_no_person(tmp_path):
    roster = tmp_path / "roster.csv"
    roster.write_text("name,email\nZed Nobody,zed@example.com\n", encoding="utf-8")
    people = _people()
    people.load_roster(roster)
    assert people.names() == ["Priya Nair", "Anita Desai"]
    assert people.email("Zed Nobody") is None


def test_name_match_is_exact(tmp_path):
    roster = tmp_path / "roster.csv"
    roster.write_text("name,email\npriya nair,p@example.com\nAnita,a@example.com\n", encoding="utf-8")
    people = _people()
    people.load_roster(roster)
    assert people.email("Priya Nair") is None and people.email("Anita Desai") is None


def test_blank_email_and_blank_lines_are_tolerated(tmp_path):
    roster = tmp_path / "roster.csv"
    roster.write_text("name,email\n\nPriya Nair,\nAnita Desai,a@example.com\n", encoding="utf-8")
    people = _people()
    people.load_roster(roster)
    assert people.email("Priya Nair") is None
    assert people.email("Anita Desai") == "a@example.com"


def test_unreadable_roster_does_not_crash(tmp_path):
    roster = tmp_path / "roster.csv"
    roster.write_bytes(b"\xff\xfe\x00bad")
    people = _people()
    people.load_roster(roster)
    assert people.names() == ["Priya Nair", "Anita Desai"]


def test_roster_is_not_the_sample_source_of_people(tmp_path):
    roster = tmp_path / "roster.csv"
    roster.write_text("name,email\nPriya Nair,a@b.c\n", encoding="utf-8")
    people = People()
    people.load_roster(roster)
    assert people.names() == []
