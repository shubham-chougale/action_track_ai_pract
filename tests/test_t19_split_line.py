from actiontrack.extract import extract_items


def _one(body: str, mark: str = "- [ ] "):
    (item,) = extract_items(mark + body)
    return item


def test_owner_task_and_due_phrase_are_split():
    item = _one("Priya N. to send the slides by Friday")
    assert (item.owner_text, item.task, item.due_phrase) == ("Priya N.", "send the slides", "by Friday")


def test_original_line_is_kept_verbatim():
    line = "  - [x]   Priya N. to send the slides by Friday  "
    (item,) = extract_items(line)
    assert item.line == line and item.done


def test_em_dash_variant_leaves_no_stray_dash():
    item = _one("Priya N. to send revised quote to Acme — by Friday")
    assert item.owner_text == "Priya N."
    assert item.task == "send revised quote to Acme"
    assert item.due_phrase == "by Friday"


def test_other_dash_styles_and_trailing_punctuation():
    for sep in (" - ", " – ", ", ", " — "):
        item = _one(f"Sam to ship it{sep}by 2026-10-09")
        assert (item.task, item.due_phrase) == ("ship it", "by 2026-10-09"), sep


def test_no_due_phrase():
    item = _one("Priya to set up the test data")
    assert (item.owner_text, item.task, item.due_phrase) == ("Priya", "set up the test data", None)


def test_due_phrase_shapes_in_the_sample_notes():
    cases = {
        "Rahul to finish login screen by Wed": "by Wed",
        "Lena to log the three new leads in CRM by EOD": "by EOD",
        "Sam to write the postmortem by EOD tomorrow": "by EOD tomorrow",
        "Karan to send the final contract to legal by tomorrow": "by tomorrow",
        "Anita to finalise the welcome-email copy by Wed 16 Sep": "by Wed 16 Sep",
        "Meera to finalise the Q4 sales targets by Oct 3rd": "by Oct 3rd",
        "Lena to collect 5 customer quotes for the landing page by 2 Oct": "by 2 Oct",
        "Rahul to start SSO spike by next Tuesday": "by next Tuesday",
        "Priya to draft the test plan for invoice rounding by end of next week": "by end of next week",
        "Sam to propose the on-call rotation by mid-October": "by mid-October",
        "Lena to collect 5 customer quotes for the landing page by end of month": "by end of month",
        "Lena to schedule the quarterly business review for November": "for November",
        "Everyone to review the prototype before the next review": "before the next review",
        "Lena to run the customer survey, results due 15 October": "due 15 October",
        "Meera to demo the portal to Acme on 2026-10-14": "on 2026-10-14",
        "Sam to schedule cutover for Saturday 10 Oct": "for Saturday 10 Oct",
    }
    for body, phrase in cases.items():
        assert _one(body).due_phrase == phrase, body


def test_words_that_only_look_like_dates_are_not_due_phrases():
    for body in (
        "Sam to cut cloud costs by 10%",
        "Priya to own the hiring plan for the two QA roles",
        "Sam to snapshot the production DB before cutover",
        "Karan to freeze invoice edits from 9 Oct",
        "Rahul to review Anita's PR on Monday's call",
    ):
        assert _one(body).due_phrase is None, body


def test_task_keeps_inner_by_and_dash_text():
    item = _one("Sam to cut cloud costs by 10% — proposal by 2026-10-09")
    assert item.task == "cut cloud costs by 10% — proposal"
    assert item.due_phrase == "by 2026-10-09"
