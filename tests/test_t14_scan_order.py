from pathlib import Path

from actiontrack.scanner import scan_folder

SAMPLE = Path(__file__).parents[1] / "notes"


def order(result):
    return [n.name for n in result.notes], [s.name for s in result.skipped]


def test_two_scans_return_the_same_order():
    assert order(scan_folder(SAMPLE)) == order(scan_folder(SAMPLE))


def test_order_is_by_file_name_regardless_of_listing_order(monkeypatch):
    expected = order(scan_folder(SAMPLE))
    notes, skipped = expected
    assert notes == sorted(notes) and skipped == sorted(skipped)

    real = Path.iterdir
    monkeypatch.setattr(Path, "iterdir", lambda self: iter(sorted(real(self), reverse=True)))
    assert order(scan_folder(SAMPLE)) == expected
