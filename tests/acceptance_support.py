"""Helpers for the Phase 12 acceptance checks on the real sample notes/ folder."""

import json
from pathlib import Path

from actiontrack.cli import main

NOTES = Path(__file__).resolve().parent.parent / "notes"
TODAY = "2026-10-28"


def run(capsys, *args):
    """Run the CLI; returns (exit code, stdout, stderr)."""
    code = main(list(args))
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def ingest_sample(capsys, folder=NOTES):
    return run(capsys, "ingest", str(folder))


def listed(capsys, *extra, today=TODAY):
    code, out, _ = run(capsys, "list", "--json", "--today", today, *extra)
    assert code == 0
    return json.loads(out)


def find(rows, text):
    """The one listed item whose task contains text."""
    hits = [r for r in rows if text in r["task"]]
    assert len(hits) == 1, f"{text!r} matched {len(hits)} items"
    return hits[0]
