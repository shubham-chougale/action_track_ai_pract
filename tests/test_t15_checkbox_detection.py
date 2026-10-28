from pathlib import Path

from actiontrack.extract import extract_items

FIXTURES = Path(__file__).parent / "fixtures" / "notes"


def test_every_marker_and_state_is_found():
    items = extract_items((FIXTURES / "markers.md").read_text(encoding="utf-8"))
    assert [(i.line, i.done) for i in items] == [
        ("- [ ] Priya to do dash open", False),
        ("- [x] Priya to do dash done", True),
        ("- [X] Priya to do dash upper done", True),
        ("* [ ] Priya to do star open", False),
        ("+ [ ] Priya to do plus open", False),
    ]


def test_any_indentation_is_found():
    text = "- [ ] a\n  - [x] b\n    * [ ] c\n\t+ [X] d\n"
    assert [i.done for i in extract_items(text)] == [False, True, False, True]


def test_plain_bullets_and_malformed_checkboxes_are_not_items():
    text = "- plain bullet\n- [] no space\n- [y] wrong mark\n-[ ] no gap\n- [ ]\n[ ] no bullet\n"
    assert extract_items(text) == []


def test_crlf_lines_are_handled():
    items = extract_items("- [ ] Priya to do it\r\n- [x] Sam to do that\r\n")
    assert [i.line for i in items] == ["- [ ] Priya to do it", "- [x] Sam to do that"]
