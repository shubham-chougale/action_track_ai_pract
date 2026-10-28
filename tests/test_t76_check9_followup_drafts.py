"""Acceptance 9 with the connector replaced by a recorder.

The real-connector half (a draft really appears in Gmail, Sent unchanged) is
blocked by X-001 in blockers.md, so T76 stays unticked.
"""

import actiontrack.cli as cli
from acceptance_support import ingest_sample, run


def test_followup_creates_one_draft_per_run_and_sends_nothing(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    drafts = []
    monkeypatch.setattr(cli, "create_draft",
                        lambda to, subject, body: drafts.append((to, subject, body)) or f"draft-{len(drafts)}")
    code, out, _ = run(capsys, "followup", "Priya Nair", "--today", "2026-10-28")
    assert code == 0 and len(drafts) == 1 and "draft-1" in out
    assert drafts[0][1].startswith("Action items follow-up: Priya Nair (")
    code, out, _ = run(capsys, "followup", "Priya Nair", "--today", "2026-10-28")
    assert code == 0 and len(drafts) == 2 and "draft-2" in out
