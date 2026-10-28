import actiontrack.gmail as gmail
from test_t65_gmail_draft import FakeClaude


def test_two_runs_make_two_drafts_and_nothing_else(monkeypatch):
    fake = FakeClaude()
    monkeypatch.setattr(gmail, "_run", fake)
    monkeypatch.setattr(gmail.shutil, "which", lambda name: "claude")
    gmail.create_draft(None, "S", "B")
    gmail.create_draft(None, "S", "B")
    assert len(fake.calls) == 2
    for cmd, kwargs in fake.calls:
        text = " ".join(cmd) + kwargs["input"]
        for tool in ("list_drafts", "get_draft", "update_draft", "delete_draft", "search_threads"):
            assert tool not in text
        assert "create_draft" in text
