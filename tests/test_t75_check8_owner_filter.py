from acceptance_support import ingest_sample, listed, run


def test_shared_first_name_fails_listing_both_priyas(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    code, out, err = run(capsys, "list", "--owner", "Priya")
    assert code != 0 and out == ""
    assert "Priya Nair" in err and "Priya Shah" in err


def test_full_name_works(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    rows = listed(capsys, "--owner", "Priya Nair")
    assert rows and all("Priya Nair" in r["owners"] for r in rows)
    code, out, _ = run(capsys, "list", "--owner", "Priya Nair")
    assert code == 0 and "Total:" in out
