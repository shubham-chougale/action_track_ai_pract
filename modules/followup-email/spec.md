# Module: followup-email

Requirements covered: FR-18, FR-19 (recipient use), FR-20 (acceptance check 8.9).

## Purpose
Decide which items go to one owner and compose the follow-up email (subject and plain-text body) for `actiontrack followup <owner>`.

## Inputs
- Owner argument; `--today YYYY-MM-DD`.
- Stored items, known people, roster emails.

## Item selection
1. One owner per run, matched with the same rules as `list --owner` (an ambiguous first name fails with the list of candidates).
2. Include the owner's open and overdue items.
3. Exclude done, unassigned, ambiguous and flagged items.
4. Co-owned items are included for each owner.
5. Merged duplicates appear once.
6. If the owner has no such items: no draft is created and a message says so.
7. Report how many unassigned items exist.

## Recipient
- From the roster CSV (`name,email`). If the roster file or the person is missing, the draft is still created with no recipient and a warning is printed.

## Content
- Subject: `Action items follow-up: <Full Name> (<n> overdue, <m> open)`; counts match the email.
- Body, plain text: greeting `Hi <first name>,`; short intro line; section **Overdue** first, then **Open**.
- Each item shows: task, due date (or raw phrase for unresolved dates, or "no due date"), source meeting name and date, item ID.
- The user's Gmail signature is appended by Gmail. The tool adds no sign-off.

## Depends on
`persistence`, `people-roster`, `item-listing` (status rules), `gmail-draft`.
