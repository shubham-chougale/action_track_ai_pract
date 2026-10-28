# Module: item-listing

Requirements covered: FR-14, FR-15, FR-16 (acceptance check 8.8).

## Purpose
`actiontrack list`: show tracked items with filters.

## Inputs
- Stored items.
- Options: `--owner <name>`, `--status open|done|overdue`, `--due-before YYYY-MM-DD`, `--json`, `--today YYYY-MM-DD`.

## Filters (combine with AND)
- `--owner`: full name always works (case-insensitive). A first name works only if exactly one known person has it; otherwise fail with a message listing the matching people (e.g. Priya Nair, Priya Shah). `unassigned` is accepted.
- `--status`: open, done or overdue.
- `--due-before`: strictly before the date. Items with no resolved due date never match. An invalid date gives an error and non-zero exit.

## Status definitions
- done: ticked in the latest note or marked with `done`.
- overdue: open AND due date strictly before today. Due today is open. Done items, items with no due date, and flagged items are never overdue.
- open: anything else not done.
- Today is the computer's date unless `--today` is given.

## Output
- Default: all items, including done, sorted by due date (soonest first, no-due-date last).
- Text table, columns: ID, Owner(s), Task, Due, Status, Source.
  - Due: resolved date; raw phrase marked `?` when unresolved; `-` when none.
  - Status: open / done / overdue, plus a flag marker for flagged items.
  - Source: file and meeting date; merged items show the latest source and the count of other mentions.
  - Co-owned items appear under each owner.
- Ends with a total count. Empty result prints `No items match`.
- `--json` gives machine-readable output.

## Depends on
`persistence`, `people-roster`.
