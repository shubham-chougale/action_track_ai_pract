# Module: persistence

Requirements covered: FR-12, section 6 (data kept), NFR (deterministic, notes never modified); SC5; acceptance check 8.10.

## Purpose
Keep items, sources and people between runs so re-ingesting is safe and IDs stay stable.

## Data kept
Per item: ID; owner(s) (resolved person, or Unassigned / ambiguous / unknown with raw text); task; original line; due date or raw unresolved phrase; status (open/done) and whether set manually; flagged marker and reason; all source mentions (file, meeting date, meeting title); first-seen order.
Per person: full name, optional email.

## Rules
1. Data and the roster live in a hidden `.actiontrack/` folder in the directory where the user runs the tool. Separate directories keep separate data.
2. IDs are short sequential numbers assigned at first ingestion; never reused; stable across re-ingests and merges.
3. Re-running ingest on the same folder, or adding new notes, never creates duplicates and never resets status. It adds only new items and sources.
4. A manual `done` always sticks, regardless of any later note.
5. A second `ingest` on the same folder reports 0 new items and changes nothing, even after `done` was used.
6. Notes are never modified; done status lives only in actiontrack's own data.
7. Results are deterministic for the same notes and `--today` date.
8. A failed command (e.g. Gmail failure in `followup`) changes no data.

## Depends on
None. Used by every other module that reads or writes items.
