import subprocess
import sys

import pytest

from actiontrack.cli import main
from actiontrack.scanner import FolderError, scan_folder


def test_missing_path_raises_folder_error(tmp_path):
    with pytest.raises(FolderError, match="not found"):
        scan_folder(tmp_path / "nope")


def test_file_path_raises_folder_error(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("x", encoding="utf-8")
    with pytest.raises(FolderError, match="not a folder"):
        scan_folder(f)


def test_ingest_missing_path_prints_error_and_exits_nonzero(tmp_path, capsys):
    assert main(["ingest", str(tmp_path / "nope")]) != 0
    assert "folder not found" in capsys.readouterr().err


def test_ingest_file_path_prints_error_and_exits_nonzero(tmp_path, capsys):
    f = tmp_path / "a.md"
    f.write_text("x", encoding="utf-8")
    assert main(["ingest", str(f)]) != 0
    assert "not a folder" in capsys.readouterr().err


def test_exit_code_in_a_real_process(tmp_path):
    out = subprocess.run([sys.executable, "-m", "actiontrack.cli", "ingest", str(tmp_path / "nope")],
                         capture_output=True, text=True)
    assert out.returncode != 0 and "folder not found" in out.stderr


def test_valid_folder_exits_zero(tmp_path):
    assert main(["ingest", str(tmp_path)]) == 0
