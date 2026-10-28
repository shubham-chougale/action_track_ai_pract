from acceptance_support import find, ingest_sample, listed


def test_anita_and_rahul_are_both_owners(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ingest_sample(capsys)
    item = find(listed(capsys), "agree on the component API")
    assert item["owners"] == ["Anita Desai", "Rahul Mehta"]
    assert not item["flagged"]
