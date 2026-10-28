import actiontrack.cli as cli
from acceptance_support import find, ingest_sample, listed, run
from actiontrack.store import Store

DECOYS = ("remediate finding", "hardware tokens")


def test_decoys_are_flagged_and_never_overdue(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    for today in ("2026-10-28", "2099-01-01"):
        rows = listed(capsys, today=today)
        template = find(rows, "remediate finding")
        commented = find(rows, "hardware tokens")
        for item, reason in ((template, "code block"), (commented, "comment")):
            assert item["flagged"] and reason in item["flag_reason"]
            assert item["status"] == "open"
        assert not [r for r in listed(capsys, "--status", "overdue", today=today)
                    if any(d in r["task"] for d in DECOYS)]


def test_decoys_are_in_no_followup_draft(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    drafts = []
    monkeypatch.setattr(cli, "create_draft", lambda to, subject, body: drafts.append(body) or "d")
    people = Store(tmp_path).people_names()
    assert people
    for name in people:
        assert run(capsys, "followup", name, "--today", "2099-01-01")[0] == 0
    assert drafts
    for body in drafts:
        assert not any(d in body for d in DECOYS)
