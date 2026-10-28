import hashlib
import os
from pathlib import Path

import pytest

import actiontrack.cli as cli
from acceptance_support import NOTES, run

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "notes"


def digest(folder):
    return {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob("*")) if p.is_file()}


def make_garbage(root):
    root.mkdir()
    (root / "empty.md").write_bytes(b"")
    (root / "binary.md").write_bytes(os.urandom(4096))
    (root / "nul.md").write_bytes(b"Date: 2026-10-01\n\x00\x00- [ ] Priya to x\n")
    (root / "latin1.md").write_bytes("Date: 2026-10-01\n- [ ] Zo\xe9 to do it\n".encode("latin-1"))
    (root / "huge.md").write_text("# T\nDate: 2026-10-01\n" + "- [ ] A to b by Friday\n" * 20000, encoding="utf-8")
    (root / "longline.md").write_text("Date: 2026-10-01\n- [ ] " + "x" * 500000, encoding="utf-8")
    (root / "markers.md").write_text("- [ ]\n- [x]\n- [ ] \n- [ ] to\n- [ ] by Friday\n", encoding="utf-8")
    (root / "dir.md").mkdir()
    (root / "noext").write_text("Date: 2026-10-01", encoding="utf-8")
    (root / "emoji.md").write_text("Date: 2026-10-01\nAttendees: \U0001f600\n- [ ] \U0001f600 to ‮ rtl\n",
                                   encoding="utf-8")


COMMANDS = [
    ["list"], ["list", "--json"], ["list", "--status", "overdue"], ["list", "--owner", "Priya"],
    ["list", "--owner", "unassigned"], ["list", "--due-before", "2026-11-01"], ["list", "--today", "nope"],
    ["done", "1"], ["done", "999999"], ["done", "abc"], ["done", "-1"],
    ["followup", "Priya Nair", "--today", "2026-10-28"], ["followup", "Nobody"], ["followup", "Priya"],
]


@pytest.mark.parametrize("name", ["sample", "fixtures", "garbage", "missing", "a_file"])
def test_every_command_ends_with_a_message_not_a_crash(name, tmp_path, monkeypatch, capsys):
    garbage = tmp_path / "garbage"
    make_garbage(garbage)
    target = {"sample": NOTES, "fixtures": FIXTURES, "garbage": garbage,
              "missing": tmp_path / "nope", "a_file": garbage / "noext"}[name]
    before = digest(target) if target.is_dir() else None
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    monkeypatch.setattr(cli, "create_draft", lambda *a: "draft-1")
    code, out, err = run(capsys, "ingest", str(target))
    assert isinstance(code, int) and (out or err)
    for args in COMMANDS * 2:
        code, out, err = run(capsys, *args)
        assert isinstance(code, int)
        assert out or err or code == 0
        assert "Traceback" not in out + err
    if before is not None:
        assert digest(target) == before  # notes/ stays read-only


def test_commands_before_any_ingest_do_not_crash(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    for args in COMMANDS:
        assert isinstance(run(capsys, *args)[0], int)


@pytest.mark.parametrize("filename,content", [("items.json", "{bad"), ("items.json", "[]"),
                                              ("items.json", '{"next_id": 1}'), ("people.json", "[1")])
def test_damaged_data_files_give_a_message_and_stay_untouched(filename, content, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".actiontrack").mkdir()
    damaged = tmp_path / ".actiontrack" / filename
    damaged.write_text(content, encoding="utf-8")
    monkeypatch.setattr(cli, "create_draft", lambda *a: "draft-1")
    for args in (["ingest", str(FIXTURES)], ["list"], ["done", "1"], ["followup", "Priya"]):
        code, out, err = run(capsys, *args)
        assert code != 0 and "Traceback" not in err
        if not (args[0] == "done" and filename == "people.json"):  # done never reads the people file
            assert filename in err
    assert damaged.read_text(encoding="utf-8") == content
