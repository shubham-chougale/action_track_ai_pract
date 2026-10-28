import re
import subprocess
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"
ROOT = Path(__file__).parents[1]


def test_every_fixture_is_listed_with_a_comment():
    rows = re.findall(r"^\| `notes/([^`]+)` \| (.+) \|$", (FIXTURES / "README.md").read_text(), re.M)
    listed = {name for name, comment in rows if comment.strip()}
    on_disk = {p.name for p in (FIXTURES / "notes").iterdir()}
    assert listed == on_disk


def test_sample_notes_untouched():
    out = subprocess.run(["git", "status", "--porcelain", "notes"], cwd=ROOT, capture_output=True, text=True)
    assert out.stdout == ""
