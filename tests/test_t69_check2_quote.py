from acceptance_support import find, ingest_sample, listed


def test_revised_quote_item_appears_once_and_is_done(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    rows = listed(capsys)
    quote = [r for r in rows if "revised quote" in r["task"]]
    assert len(quote) == 1
    assert quote[0]["owners"] == ["Priya Nair"] and quote[0]["status"] == "done"
    assert "Acme" in quote[0]["task"]
    assert len(quote[0]["sources"]) > 1  # merged, every source kept
    assert find(rows, "send the revised quote to Acme") is quote[0]
