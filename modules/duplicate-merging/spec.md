# Module: duplicate-merging

Requirements covered: FR-11 (SC2; acceptance check 8.2).

## Purpose
Recognise the same action item mentioned in several meetings and keep it as one item.

## Inputs
- A newly extracted item (resolved owners, task text, due date, checked state, source).
- Existing items.

## Outputs
- Either a new item, or an update to an existing one (merged).
- Per run counts: new / merged / unchanged (for `ingest-report`).

## Rules
1. Two mentions are the same item when the resolved owner(s) match and the task wording is similar after normalising case, articles, punctuation and the due phrase.
2. Small rewording must still match (a dropped "the", `Priya N.` vs `Priya`).
3. Different owners never merge.
4. A merged item is one row with one ID. All source notes (file, meeting date, meeting title) are kept.
5. Latest meeting wins for status and due date:
   - a later `[x]` marks the item done;
   - a later `[ ]` reopens it;
   - a later due date replaces an earlier one;
   - a later mention with no due date does not erase an existing one.
6. A manual `done` always sticks, whatever a later note shows (see `persistence`, `mark-done`).
7. Flagged items follow the same matching rules.

## Example
"Priya to send the revised quote to Acme" appears in 09-01, 09-08 (as `Priya N.` with an em dash) and 09-15 (`[x]`). Result: one item, done, three sources.

## Depends on
`owner-resolution`, `due-date-resolution`, `action-item-extraction`, `persistence`.
