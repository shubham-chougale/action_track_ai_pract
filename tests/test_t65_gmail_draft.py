import json
import subprocess

import pytest

import actiontrack.gmail as gmail

CREATE = "mcp__claude_ai_Gmail__create_draft"
SENDERS = ["mcp__claude_ai_Gmail__send_message", "mcp__claude_ai_Gmail__reply",
           "mcp__claude_ai_Gmail__forward"]


class FakeClaude:
    def __init__(self, result=None, **proc):
        self.calls = []
        self.result = result or json.dumps({"draft_id": "r123", "url": "https://mail.google.com/d/r123"})
        self.proc = proc

    def __call__(self, cmd, **kwargs):
        self.calls.append((cmd, kwargs))
        out = json.dumps({"type": "result", "is_error": False, "result": self.result})
        return subprocess.CompletedProcess(cmd, self.proc.get("returncode", 0),
                                           self.proc.get("stdout", out), "")


@pytest.fixture
def fake(monkeypatch):
    f = FakeClaude()
    monkeypatch.setattr(gmail, "_run", f)
    monkeypatch.setattr(gmail.shutil, "which", lambda name: "claude")
    return f


def test_creates_exactly_one_draft_and_returns_its_id_and_link(fake):
    out = gmail.create_draft("p@example.com", "Subj", "Hi Priya,\nbody")
    assert len(fake.calls) == 1
    assert "r123" in out and "https://mail.google.com/d/r123" in out


def test_prompt_carries_recipient_subject_and_body(fake):
    gmail.create_draft("p@example.com", "Subj line", "Hi Priya,\nbody text")
    prompt = fake.calls[0][1]["input"]
    for part in ("p@example.com", "Subj line", "Hi Priya,\nbody text"):
        assert part in prompt


def test_no_recipient_is_allowed(fake):
    gmail.create_draft(None, "S", "B")
    assert "p@example.com" not in fake.calls[0][1]["input"]


def test_only_create_draft_is_allowed_and_every_sender_is_blocked(fake):
    gmail.create_draft(None, "S", "B")
    cmd = fake.calls[0][0]
    allowed = cmd[cmd.index("--allowedTools") + 1:]
    allowed = allowed[:next((i for i, a in enumerate(allowed) if a.startswith("--")), len(allowed))]
    assert allowed == [CREATE]
    blocked = cmd[cmd.index("--disallowedTools") + 1:]
    for tool in SENDERS:
        assert tool in blocked
    assert "--tools" in cmd and cmd[cmd.index("--tools") + 1] == ""


def test_the_module_never_names_a_send_tool_outside_the_block_list():
    import inspect
    src = inspect.getsource(gmail)
    for tool in SENDERS:
        assert src.count(tool) == 1  # only in the disallowed list


def test_list_form_output_is_read_and_a_double_create_is_an_error(monkeypatch):
    def use():
        return {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": CREATE}]}}

    def run(events):
        out = json.dumps(events)
        monkeypatch.setattr(gmail, "_run", lambda cmd, **kw: subprocess.CompletedProcess(cmd, 0, out, ""))
        monkeypatch.setattr(gmail.shutil, "which", lambda name: "claude")
        return gmail.create_draft(None, "S", "B")

    final = {"type": "result", "is_error": False, "result": '{"draft_id": "d9"}'}
    assert run([{"type": "system"}, use(), final]) == "d9"
    with pytest.raises(gmail.DraftError, match="2 Gmail drafts"):
        run([use(), use(), final])
