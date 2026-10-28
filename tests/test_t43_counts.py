import re
import shutil
from pathlib import Path

from actiontrack.cli import main
from actiontrack.store import Store

ROOT = Path(__file__).parents[1]
SAMPLE = ROOT / "notes"
FIXTURES = Path(__file__).parent / "fixtures" / "notes"


def numbers(out):
    return {k: int(v) for k, v in re.findall(r"^(Files \w+|Items \w+):\s+(\d+)$", out, re.M)}


def test_sample_folder_file_counts(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["ingest", str(SAMPLE)]) == 0
    got = numbers(capsys.readouterr().out)
    assert (got["Files scanned"], got["Files ingested"], got["Files skipped"]) == (35, 31, 4)


def test_sample_folder_item_counts_match_the_store(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    main(["ingest", str(SAMPLE)])
    got = numbers(capsys.readouterr().out)
    assert got["Items new"] == len(Store(tmp_path).all()) > 0
    assert got["Items merged"] > 0  # the sample repeats items across meetings
    assert got["Items unchanged"] == 0


def test_txt_files_are_not_counted(tmp_path, monkeypatch, capsys):
    notes = tmp_path / "notes"
    shutil.copytree(FIXTURES, notes)
    monkeypatch.chdir(tmp_path)
    main(["ingest", str(notes)])
    got = numbers(capsys.readouterr().out)
    assert (got["Files scanned"], got["Files ingested"], got["Files skipped"]) == (10, 6, 4)
