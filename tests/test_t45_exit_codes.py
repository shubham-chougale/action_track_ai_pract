import subprocess
import sys
from pathlib import Path

from actiontrack.cli import main

SAMPLE = Path(__file__).parents[1] / "notes"


def test_exit_zero_with_skipped_notes(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["ingest", str(SAMPLE)]) == 0
    assert "Skipped files:" in capsys.readouterr().out


def test_exit_zero_for_an_empty_folder(tmp_path, monkeypatch):
    (tmp_path / "empty").mkdir()
    monkeypatch.chdir(tmp_path)
    assert main(["ingest", str(tmp_path / "empty")]) == 0


def test_exit_nonzero_only_for_fatal_folder_errors(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["ingest", str(tmp_path / "nope")]) != 0
    captured = capsys.readouterr()
    assert "folder not found" in captured.err and "Files scanned" not in captured.out


def test_real_process_exit_codes(tmp_path):
    run = lambda folder: subprocess.run(
        [sys.executable, "-m", "actiontrack.cli", "ingest", str(folder)],
        capture_output=True, text=True, cwd=tmp_path)
    assert run(SAMPLE).returncode == 0
    assert run(tmp_path / "nope").returncode != 0
