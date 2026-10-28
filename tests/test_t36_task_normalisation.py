import pytest

from actiontrack.merge import normalize_task, same_task


@pytest.mark.parametrize("a, b", [
    ("send the revised quote to Acme", "Send the Revised Quote to ACME"),
    ("send the revised quote to Acme", "send revised quote to Acme"),
    ("send a revised quote to Acme", "send an revised quote to Acme"),
    ("send the revised quote to Acme", "send the revised quote, to Acme."),
    ("send the revised quote to Acme", "send the revised quote to Acme — by Friday"),
    ("send the revised quote to Acme", "send the revised quote to Acme by 2026-09-08"),
    ("deploy the beta to staging", "deploy the beta to staging by tomorrow"),
    ("update the CRM notes", "update   the CRM notes!"),
    ("estimate the SSO work", "estimate SSO work"),
])
def test_wording_differing_only_in_case_articles_punctuation_or_due_is_equal(a, b):
    assert same_task(a, b)


@pytest.mark.parametrize("a, b", [
    ("send the revised quote to Acme", "send the invoice to Globex"),
    ("fix the pagination bug", "fix the login redirect"),
    ("review the schema mapping doc", "write the beta test checklist"),
    ("deploy the beta to staging", "rotate the production keys"),
    ("start SSO spike", "estimate SSO work"),
])
def test_clearly_different_tasks_are_not_equal(a, b):
    assert not same_task(a, b)


def test_normalize_strips_case_articles_punctuation_and_due():
    assert normalize_task("Send the Revised quote, to Acme — by Friday") == "send revised quote to acme"
