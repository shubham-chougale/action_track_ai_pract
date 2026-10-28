from pathlib import Path

import actiontrack.duedate as duedate
from actiontrack.duedate import resolve_due
from actiontrack.extract import extract_items
from actiontrack.metadata import parse_metadata

NOTES = Path(__file__).parent.parent / "notes"


def _sample_phrases():
    for path in sorted(NOTES.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        meta = parse_metadata(text)
        if meta.date:
            for item in extract_items(text):
                if item.due_phrase:
                    yield item.due_phrase, meta.date


def test_every_sample_phrase_resolves_identically_twice():
    cases = list(_sample_phrases())
    assert len(cases) > 50
    first = [resolve_due(p, d) for p, d in cases]
    second = [resolve_due(p, d) for p, d in cases]
    assert first == second


def test_results_do_not_depend_on_the_system_clock(monkeypatch):
    cases = list(_sample_phrases())
    before = [resolve_due(p, d) for p, d in cases]

    class FrozenElsewhere(duedate.date):
        @classmethod
        def today(cls):
            raise AssertionError("resolve_due must not read the system clock")

    monkeypatch.setattr(duedate, "date", FrozenElsewhere)
    assert [resolve_due(p, d) for p, d in cases] == before


def test_the_module_never_reads_the_clock():
    source = Path(duedate.__file__).read_text(encoding="utf-8")
    assert "today(" not in source and "now(" not in source
