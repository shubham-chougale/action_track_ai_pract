"""Run the real CLI as a separate process, with spaces in every path."""

import json
import shutil
import subprocess
import sys

from acceptance_support import NOTES


def cli(cwd, *args):
    return subprocess.run([sys.executable, "-m", "actiontrack.cli", *args], cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8")


def test_paths_with_spaces_work_end_to_end(tmp_path):
    notes = tmp_path / "my meeting notes" / "sample notes"
    shutil.copytree(NOTES, notes)
    work = tmp_path / "work dir with spaces"
    work.mkdir()
    done = cli(work, "ingest", str(notes))
    assert done.returncode == 0 and "Files ingested:  31" in done.stdout and "Files skipped:   4" in done.stdout
    rows = json.loads(cli(work, "list", "--json", "--today", "2026-10-28").stdout)
    assert len(rows) == 92
    bad = cli(work, "list", "--owner", "Priya")
    assert bad.returncode != 0 and "Priya Nair" in bad.stderr and "Traceback" not in bad.stderr
    assert cli(work, "list", "--owner", "Priya Nair").returncode == 0
    marked = cli(work, "done", str(rows[0]["id"]))
    assert marked.returncode == 0
    again = cli(work, "ingest", str(notes))
    assert "Items new:       0" in again.stdout
    assert (work / ".actiontrack").is_dir() and not (notes / ".actiontrack").exists()


def test_a_missing_folder_with_spaces_is_a_message(tmp_path):
    work = tmp_path / "w d"
    work.mkdir()
    out = cli(work, "ingest", str(tmp_path / "no such folder"))
    assert out.returncode != 0 and "Traceback" not in out.stderr and out.stderr.strip()
