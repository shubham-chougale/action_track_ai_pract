# Module: people-roster

Requirements covered: FR-6 (names learned from attendees), FR-19 (roster CSV), section 6 (per-person data).

## Purpose
Keep the set of known people and their optional email addresses.

## Inputs
- Attendee names from every ingested note.
- Roster file: CSV in `.actiontrack/` with header `name,email`.

## Outputs
- Known people: full name and optional email.
- Lookups used by `owner-resolution`, `item-listing` (`--owner`) and `followup-email`.

## Rules
1. People (names) are learned only from Attendees lines. The roster supplies emails only; it never adds people.
2. Roster rows match a person by full name, exactly as written in Attendees (e.g. `Priya Nair,priya.nair@example.com`).
3. A missing roster file, or a person missing from it, is not an error here; the person simply has no email. `followup-email` warns when this affects a draft.
4. Owner filter lookup (`list --owner`, `followup`):
   - full name always works, case-insensitive;
   - a first name works only if exactly one known person has it; otherwise the lookup fails with the list of matching people (e.g. Priya Nair, Priya Shah);
   - `unassigned` is accepted by `list`.

## Known people in the sample folder
Priya Nair, Priya Shah, Rahul Mehta, Rahul Verma, Anita Desai, Sam Okafor, Meera Iyer, Karan Joshi, Lena Fischer.

## Depends on
`meeting-metadata`, `persistence`.
