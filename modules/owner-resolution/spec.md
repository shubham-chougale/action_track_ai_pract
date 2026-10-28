# Module: owner-resolution

Requirements covered: FR-6, FR-7, FR-8 (SC3; acceptance checks 8.3, 8.4, 8.5, 8.6).

## Purpose
Turn the raw owner text of an item into one or more known people, `Unassigned`, or a flagged ambiguous/unknown owner. Never guess.

## Inputs
- Raw owner text of an item.
- Attendees of that meeting.
- Known people (from `people-roster`).

## Outputs
One of:
- owner list (one or more resolved people),
- `Unassigned` (original wording preserved),
- `ambiguous` or `unknown` (raw text kept, item flagged).

## Rules
1. Accepted forms: full name; first name; first name + initial (`Priya N.`); `@handle` (`@anita`).
2. Bare first name:
   - resolve among the meeting's attendees first; exactly one match gives that person;
   - if no attendee matches, resolve to the single person with that first name across all notes;
   - two or more matches, or none: ambiguous/unknown.
3. First name + initial resolves by the surname initial among known people.
4. Non-person owners (`Someone`, `TBD`, `Everyone`, `Team`, `Owner`) and no owner at all give `Unassigned`; the original wording is preserved.
5. Co-owners: `A & B to...` and `A (with B) to...` produce one item with all named people as owners; each name is resolved with the same rules.
6. Ambiguous/unknown owners are shown in `list` and in the ingest report, and are excluded from follow-up emails.
7. Unassigned items are listed (`--owner unassigned`) but never emailed; `followup` reports how many exist.

## Edge cases (sample folder)
- `Priya` / `Rahul` at 2026-09-30 offsite (both Priyas and both Rahuls attend): ambiguous.
- `Priya N.` / `Priya S.` in billing notes: Priya Nair / Priya Shah.
- `Anita & Rahul` in 2026-09-18 (only Rahul Mehta attends): owners Anita Desai and Rahul Mehta.
- `Lena (with Priya)`: Priya resolved by attendees of that meeting.
- `Someone`, `TBD`, `Everyone`, `Team`: Unassigned.

## Depends on
`people-roster`, `meeting-metadata`, `action-item-extraction`.
