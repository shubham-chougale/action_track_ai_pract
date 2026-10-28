import shutil
from pathlib import Path

from actiontrack.cli import main

ROOT = Path(__file__).parents[1]
SAMPLE = ROOT / "notes"
FIXTURES = Path(__file__).parent / "fixtures" / "notes"


def report(tmp_path, monkeypatch, capsys, folder=SAMPLE):
    monkeypatch.chdir(tmp_path)
    assert main(["ingest", str(folder)]) == 0
    return capsys.readouterr().out


def section(out, heading):
    """Lines under a heading, up to the next unindented line."""
    lines = out.splitlines()
    start = lines.index(heading) + 1
    body = []
    for line in lines[start:]:
        if line and not line.startswith(" "):
            break
        body.append(line.strip())
    return [b for b in body if b]


def test_each_skipped_file_is_listed_with_its_reason(tmp_path, monkeypatch, capsys):
    out = report(tmp_path, monkeypatch, capsys)
    assert section(out, "Skipped files:") == [
        "2026-09-09-notes-final-v2.md: empty",
        "2026-10-03-sales-pipeline.md: invalid date",
        "scratch.md: binary",
        "untitled.md: missing date",
    ]


def test_ambiguous_owners_show_the_raw_text(tmp_path, monkeypatch, capsys):
    out = report(tmp_path, monkeypatch, capsys)
    owners = section(out, "Flagged - ambiguous or unknown owner:")
    assert len(owners) == 6
    assert ("2026-09-17-billing-migration-sync.md: owner 'Priya' (ambiguous) - "
            "- [ ] Priya to sign off the cutover checklist by Monday") in owners


def test_unresolved_due_phrases_show_the_raw_phrase(tmp_path, monkeypatch, capsys):
    out = report(tmp_path, monkeypatch, capsys)
    dues = section(out, "Flagged - unresolved due phrase:")
    assert len(dues) == 5
    assert any("by end of next week" in d and d.startswith("2026-09-03-billing") for d in dues)
    assert any("for November" in d for d in dues)


def test_decoys_are_grouped_with_their_kind(tmp_path, monkeypatch, capsys):
    out = report(tmp_path, monkeypatch, capsys)
    decoys = section(out, "Flagged - found in a code block or comment:")
    assert len(decoys) == 2
    assert decoys[0].startswith("2026-10-09-security-review.md: code block - ")
    assert decoys[1].startswith("2026-10-09-security-review.md: comment - ")


def test_clean_run_has_no_empty_sections(tmp_path, monkeypatch, capsys):
    notes = tmp_path / "notes"
    notes.mkdir()
    shutil.copy(FIXTURES / "header_style_a.md", notes)
    out = report(tmp_path, monkeypatch, capsys, notes)
    assert "Skipped files" not in out and "Flagged" not in out
