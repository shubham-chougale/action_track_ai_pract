from pathlib import Path

import pytest

from actiontrack.duedate import UNRESOLVED_DATE, resolve_due
from actiontrack.extract import extract_items
from actiontrack.metadata import parse_metadata

NOTES = Path(__file__).parent.parent / "notes"


@pytest.mark.parametrize("phrase", [
    "by mid-October", "mid-October", "by end of month", "by end of next week",
    "for November", "before the next review",
])
def test_unresolvable_phrase_is_empty_kept_and_flagged(phrase):
    r = resolve_due(phrase, "2026-09-08")
    assert r.date is None
    assert r.phrase == phrase
    assert r.flag == UNRESOLVED_DATE == "unresolved date"


def test_impossible_or_unknown_wording_is_flagged_too():
    for phrase in ("by 31 Sep", "by whenever", "by 2026-02-30", "by Octember 3"):
        r = resolve_due(phrase, "2026-09-08")
        assert (r.date, r.phrase, r.flag) == (None, phrase, UNRESOLVED_DATE)


def test_resolved_phrases_are_not_flagged():
    assert resolve_due("by Friday", "2026-09-08").flag is None


def test_missing_phrase_is_not_flagged():
    assert resolve_due(None, "2026-09-08").flag is None
    assert resolve_due("", "2026-09-08").flag is None


def test_no_sample_phrase_gives_empty_date_without_a_flag():
    seen = 0
    for path in sorted(NOTES.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        meta = parse_metadata(text)
        if not meta.date:
            continue
        for item in extract_items(text):
            r = resolve_due(item.due_phrase, meta.date)
            seen += item.due_phrase is not None
            if item.due_phrase:
                assert r.date or r.flag == UNRESOLVED_DATE, (path.name, item.due_phrase)
                assert r.phrase == item.due_phrase
    assert seen > 50
