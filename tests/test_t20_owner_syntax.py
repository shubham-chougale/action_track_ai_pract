import pytest

from actiontrack.extract import extract_items


def _split(body: str):
    (item,) = extract_items("- [ ] " + body)
    return item.owner_text, item.task, item.due_phrase


@pytest.mark.parametrize(
    "body, owner, task, due",
    [
        ("@anita: audit colour contrast on the dashboard by Mon", "@anita", "audit colour contrast on the dashboard", "by Mon"),
        ("@anita to audit colour contrast", "@anita", "audit colour contrast", None),
        ("Anita & Rahul to agree on the component API by Wednesday", "Anita & Rahul", "agree on the component API", "by Wednesday"),
        ("Anita and Rahul to agree on the API", "Anita and Rahul", "agree on the API", None),
        ("Lena (with Priya) to collect user feedback on the prototype by 2026-09-25", "Lena (with Priya)", "collect user feedback on the prototype", "by 2026-09-25"),
        ("Someone to update the CRM notes", "Someone", "update the CRM notes", None),
        ("TBD to write the design-system changelog", "TBD", "write the design-system changelog", None),
        ("Everyone to submit their Q4 goals by 7 Oct", "Everyone", "submit their Q4 goals", "by 7 Oct"),
        ("Priya N. to notify customers", "Priya N.", "notify customers", None),
        ("Priya Nair to notify customers", "Priya Nair", "notify customers", None),
        ("Book the venue", None, "Book the venue", None),
        ("Book the venue by Friday", None, "Book the venue", "by Friday"),
        ("update the style guide to match the new brand", None, "update the style guide to match the new brand", None),
    ],
)
def test_owner_syntax(body, owner, task, due):
    assert _split(body) == (owner, task, due)
