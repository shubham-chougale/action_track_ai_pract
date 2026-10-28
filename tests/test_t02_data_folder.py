import subprocess
import sys
from pathlib import Path

from actiontrack.store import data_dir


def test_separate_dirs_get_separate_data_folders(tmp_path):
    a, b = tmp_path / "A", tmp_path / "B"
    a.mkdir()
    b.mkdir()
    assert data_dir(a) == a / ".actiontrack"
    assert data_dir(b) == b / ".actiontrack"
    assert (a / ".actiontrack").is_dir() and (b / ".actiontrack").is_dir()


def test_data_written_in_a_is_invisible_from_b(tmp_path):
    a, b = tmp_path / "A", tmp_path / "B"
    a.mkdir()
    b.mkdir()
    (data_dir(a) / "marker.txt").write_text("A")
    assert [p.name for p in data_dir(a).iterdir()] == ["marker.txt"]
    assert list(data_dir(b).iterdir()) == []


def test_defaults_to_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert data_dir() == Path.cwd() / ".actiontrack"
