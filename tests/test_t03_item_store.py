import json
import subprocess
import sys

from actiontrack.store import Store

FIELDS = dict(
    owners=[{"kind": "resolved", "name": "Priya Nair", "raw": "Priya N."}],
    task="send the revised quote to Acme",
    original_line="- [ ] Priya N. to send the revised quote to Acme by Friday",
    due="2026-09-11",
    due_raw="by Friday",
    status="open",
    status_manual=False,
    flagged=True,
    flag_reason="owner ambiguous",
    sources=[{"file": "2026-09-08-quote-portal-weekly.md", "meeting_date": "2026-09-08", "meeting_title": "Weekly"}],
)


def test_item_round_trips_in_same_process(tmp_path):
    item = Store(tmp_path).add(**FIELDS)
    got = Store(tmp_path).get(item.id)
    for key, value in FIELDS.items():
        assert getattr(got, key) == value
    assert got.first_seen_order == 1


def test_item_round_trips_in_a_fresh_process(tmp_path):
    item = Store(tmp_path).add(**FIELDS)
    code = (
        "import json, sys; from dataclasses import asdict; from actiontrack.store import Store; "
        f"print(json.dumps(asdict(Store(sys.argv[1]).get({item.id}))))"
    )
    out = subprocess.run([sys.executable, "-c", code, str(tmp_path)], capture_output=True, text=True, check=True)
    got = json.loads(out.stdout)
    for key, value in FIELDS.items():
        assert got[key] == value
    assert got["id"] == item.id


def test_defaults_for_unset_fields(tmp_path):
    item = Store(tmp_path).add(task="bare item")
    got = Store(tmp_path).get(item.id)
    assert got.owners == [] and got.due is None and got.due_raw is None
    assert got.status == "open" and got.status_manual is False
    assert got.flagged is False and got.flag_reason is None and got.sources == []


def test_get_unknown_id_returns_none(tmp_path):
    assert Store(tmp_path).get(99) is None
