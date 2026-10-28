from pathlib import Path

from actiontrack.duedate import resolve_due
from actiontrack.extract import extract_items
from actiontrack.merge import Mention, merge_mention
from actiontrack.owners import RESOLVED, resolve_owner
from actiontrack.people import People
from actiontrack.scanner import scan_folder
from actiontrack.store import Store

SAMPLE = Path(__file__).parents[1] / "notes"


def mentions_for(notes, people, only=None):
    for note in notes:
        for item in extract_items(note.text):
            if only and only not in item.line:
                continue
            r = resolve_owner(item.owner_text, note.meta.attendees, people)
            owners = [{"kind": "person", "name": n} for n in r.owners] or [{"kind": r.kind, "raw": r.raw}]
            due = resolve_due(item.due_phrase, note.meta.date)
            yield Mention(
                owners=owners, task=item.task, original_line=item.line, done=item.done,
                due=due.date, due_raw=None if due.date else due.phrase,
                source={"file": note.name, "date": note.meta.date, "title": note.meta.title},
            )


def test_revised_quote_item_merges_across_three_notes(tmp_path):
    notes = scan_folder(SAMPLE).notes
    people = People.from_notes(notes)
    store = Store(tmp_path)
    for m in mentions_for(notes, people, only="quote to Acme"):
        merge_mention(store, m)

    (item,) = store.all()
    assert item.id == 1
    assert item.owners == [{"kind": "person", "name": "Priya Nair"}]
    assert item.status == "done"
    assert [s["date"] for s in item.sources] == ["2026-09-01", "2026-09-08", "2026-09-15"]
    assert [s["file"][:10] for s in item.sources] == ["2026-09-01", "2026-09-08", "2026-09-15"]
