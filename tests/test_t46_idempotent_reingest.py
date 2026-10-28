import re
from pathlib import Path

from actiontrack.cli import main
from actiontrack.store import ITEMS_FILE, Store, data_dir

SAMPLE = Path(__file__).parents[1] / "notes"


def new_items(out):
    return int(re.search(r"^Items new:\s+(\d+)$", out, re.M).group(1))


def test_second_ingest_reports_zero_new(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    main(["ingest", str(SAMPLE)])
    first = capsys.readouterr().out
    main(["ingest", str(SAMPLE)])
    second = capsys.readouterr().out
    assert new_items(first) > 0
    assert new_items(second) == 0
    assert re.search(r"^Items merged:\s+0$", second, re.M)


def test_stored_data_is_byte_for_byte_unchanged(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    main(["ingest", str(SAMPLE)])
    path = data_dir(tmp_path) / ITEMS_FILE
    before = path.read_bytes()
    count = len(Store(tmp_path).all())
    main(["ingest", str(SAMPLE)])
    assert path.read_bytes() == before
    assert len(Store(tmp_path).all()) == count


def test_unchanged_count_equals_every_mention(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    main(["ingest", str(SAMPLE)])
    first = capsys.readouterr().out
    main(["ingest", str(SAMPLE)])
    second = capsys.readouterr().out
    total = sum(int(n) for n in re.findall(r"^Items (?:new|merged|unchanged):\s+(\d+)$", first, re.M))
    assert int(re.search(r"^Items unchanged:\s+(\d+)$", second, re.M).group(1)) == total
