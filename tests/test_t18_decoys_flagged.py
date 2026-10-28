from pathlib import Path

from actiontrack.extract import extract_items

FIXTURES = Path(__file__).parent / "fixtures" / "notes"
SECURITY = Path(__file__).parent.parent / "notes" / "2026-10-09-security-review.md"


def _items(path):
    return extract_items(path.read_text(encoding="utf-8"))


def test_security_review_decoys_are_extracted_and_flagged():
    items = _items(SECURITY)
    flags = {i.line: i.flag for i in items if i.flag}
    assert flags == {
        "- [ ] Owner to remediate finding by <date>": "code block",
        "<!-- - [ ] Sam to buy hardware tokens for everyone by Friday  (cut from the agenda, not agreed) -->": "comment",
    }


def test_real_security_review_items_are_not_flagged():
    real = [i.line for i in _items(SECURITY) if not i.flag]
    assert real == [
        "- [ ] Sam to enable MFA on all admin accounts by 2026-10-16",
        "- [ ] Rahul to patch the outdated express dependency by Monday",
        "- [ ] Priya to document the incident response steps by 23 Oct",
        "- [x] Karan to revoke access for the two ex-contractors",
    ]


def test_fixtures():
    assert [i.flag for i in _items(FIXTURES / "code_block_decoy.md")] == ["code block"]
    assert [i.flag for i in _items(FIXTURES / "comment_decoy.md")] == ["comment"]


def test_multiline_comment_and_tilde_fence_and_state_resets():
    text = (
        "<!--\n- [ ] A in comment\n- [x] B in comment\n-->\n- [ ] C real\n"
        "~~~\n- [ ] D in tilde fence\n~~~\n- [ ] E real\n"
        "```md\n- [ ] F fenced\n```\n"
    )
    assert [(i.line[6:7], i.flag) for i in extract_items(text)] == [
        ("A", "comment"), ("B", "comment"), ("C", None),
        ("D", "code block"), ("E", None), ("F", "code block"),
    ]


def test_single_line_comment_closing_before_a_real_item():
    text = "<!-- - [ ] gone -->\n- [ ] real one\n"
    assert [i.flag for i in extract_items(text)] == ["comment", None]
