from acceptance_support import ingest_sample, listed


def owners_of(rows, text):
    return [r["owners"] for r in rows if text in r["task"]]


def test_initials_resolve_to_the_right_priya(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    rows = listed(capsys)
    assert owners_of(rows, "run the invoice rounding tests") == [["Priya Shah"]]
    assert owners_of(rows, "notify customers about the maintenance window") == [["Priya Nair"]]
