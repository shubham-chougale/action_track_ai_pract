from actiontrack.followup import compose, select_items
from actiontrack.store import Store
from listing_support import seed

TODAY = "2026-10-28"


def body_for(base, owner="Priya Nair"):
    return compose(owner, select_items(Store(base).all(), owner, TODAY), TODAY)[1]


def seed_mixed(base):
    seed(base, task="send the quote", due="2026-10-10",
         sources=[{"file": "a.md", "date": "2026-10-01", "title": "Quote Portal Weekly"}])
    seed(base, task="book the room", due="2026-12-01",
         sources=[{"file": "b.md", "date": "2026-10-05", "title": "Standup"}])
    seed(base, task="review the draft", due_raw="end of next sprint",
         sources=[{"file": "c.md", "date": "2026-10-06", "title": "Retro"}])
    seed(base, task="tidy the wiki",
         sources=[{"file": "d.md", "date": "2026-10-07", "title": "Sync"}])


def test_greeting_intro_and_section_order(tmp_path):
    seed_mixed(tmp_path)
    body = body_for(tmp_path)
    lines = body.splitlines()
    assert lines[0] == "Hi Priya,"
    assert lines[1] == "" and lines[2] and not lines[2].startswith("-")
    assert body.index("Overdue") < body.index("Open")


def test_each_item_shows_task_due_source_and_id(tmp_path):
    seed_mixed(tmp_path)
    body = body_for(tmp_path)
    assert "send the quote" in body and "due 2026-10-10" in body
    assert "Quote Portal Weekly (2026-10-01)" in body and "#1" in body
    assert "due 2026-12-01" in body
    assert "due end of next sprint" in body
    assert "no due date" in body and "#4" in body


def test_overdue_item_sits_under_overdue_heading(tmp_path):
    seed_mixed(tmp_path)
    body = body_for(tmp_path)
    overdue_part, open_part = body.split("Open")
    assert "send the quote" in overdue_part
    assert "book the room" in open_part and "tidy the wiki" in open_part


def test_empty_overdue_section_is_omitted(tmp_path):
    seed(tmp_path, task="later", due="2026-12-01")
    body = body_for(tmp_path)
    assert "Overdue" not in body and "Open" in body


def test_plain_text_and_no_sign_off(tmp_path):
    seed_mixed(tmp_path)
    body = body_for(tmp_path)
    assert "<" not in body and "**" not in body
    last = body.rstrip().splitlines()[-1]
    assert last.startswith("-") or last.startswith("  ")
    for word in ("Thanks", "Regards", "Best", "Cheers"):
        assert word not in body


def test_first_name_only_in_greeting(tmp_path):
    seed(tmp_path, task="x", owners=[{"kind": "person", "name": "Rahul Mehta"}])
    assert body_for(tmp_path, "Rahul Mehta").startswith("Hi Rahul,")
