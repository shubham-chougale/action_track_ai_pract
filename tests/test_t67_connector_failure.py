import json
import subprocess

import pytest

import actiontrack.cli as cli
import actiontrack.gmail as gmail
from actiontrack.store import Store
from listing_support import seed


def broken(monkeypatch, runner):
    monkeypatch.setattr(gmail, "_run", runner)
    monkeypatch.setattr(gmail.shutil, "which", lambda name: "claude")


def proc(returncode=0, stdout="", stderr=""):
    return lambda cmd, **kw: subprocess.CompletedProcess(cmd, returncode, stdout, stderr)


def result(text, is_error=False):
    return json.dumps({"type": "result", "is_error": is_error, "result": text})


FAILURES = {
    "signed out": proc(1, result("Not logged in", True), "please /login"),
    "tool error": proc(0, result("The Gmail connector is not connected", True)),
    "no id": proc(0, result("I created it")),
    "garbage": proc(0, "not json"),
}


@pytest.mark.parametrize("name", FAILURES)
def test_failures_raise_with_what_failed_and_how_to_retry(monkeypatch, name):
    broken(monkeypatch, FAILURES[name])
    with pytest.raises(gmail.DraftError) as err:
        gmail.create_draft(None, "S", "B")
    assert "retry" in str(err.value).lower()


def test_claude_missing(monkeypatch):
    monkeypatch.setattr(gmail.shutil, "which", lambda name: None)
    with pytest.raises(gmail.DraftError, match="retry"):
        gmail.create_draft(None, "S", "B")


def test_timeout(monkeypatch):
    def slow(cmd, **kw):
        raise subprocess.TimeoutExpired(cmd, 1)
    broken(monkeypatch, slow)
    with pytest.raises(gmail.DraftError, match="retry"):
        gmail.create_draft(None, "S", "B")


def test_no_retry_no_fallback_file_and_data_unchanged(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    Store(tmp_path).learn_people(["Priya Nair"])
    seed(tmp_path, task="quote", due="2026-11-10")
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    calls = []

    def runner(cmd, **kw):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 1, "", "boom")

    broken(monkeypatch, runner)
    assert cli.main(["followup", "Priya Nair", "--today", "2026-10-28"]) != 0
    assert len(calls) == 1
    assert "retry" in capsys.readouterr().err.lower()
    assert {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()} == before
