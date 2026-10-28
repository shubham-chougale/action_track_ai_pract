# Module: note-scanning

Requirements covered: FR-1, FR-5 (and acceptance check 8.1).

## Purpose
Decide which files in the given folder are notes to ingest, and skip malformed notes with a reason, without ever stopping the run.

## Inputs
- `<folder>` path given to `actiontrack ingest`.

## Outputs
- Ordered list of candidate notes (readable, non-empty, with a valid meeting date).
- List of skipped notes, each with file name and reason.
- Count of files scanned.

## Rules
1. Scan only top-level `.md` files. No recursion into subfolders.
2. Other files (e.g. `.txt`) are ignored silently: not counted as skipped, not reported.
3. A missing folder, or a path that is not a folder, is a fatal error: message and non-zero exit.
4. A `.md` note is skipped, with a reason, if it is:
   - unreadable or binary,
   - empty or whitespace-only,
   - missing a meeting date, or its date is not a real date (the date itself is supplied by `meeting-metadata`).
5. A missing Attendees line or missing title is NOT a reason to skip.
6. Skipping one note never affects the others and never crashes the tool.
7. Notes are read-only; they are never modified.
8. Processing order is deterministic (same folder gives same order).

## Edge cases (sample folder)
| File | Outcome |
|---|---|
| 2026-09-09-notes-final-v2.md | skipped: empty |
| scratch.md | skipped: binary |
| untitled.md | skipped: no date |
| 2026-10-03-sales-pipeline.md | skipped: invalid date (`sometime last week`) |
| 2026-09-19-offsite-draft.txt | ignored silently |

Expected: 36 files in folder, 35 `.md`; 4 skipped; 31 ingested.

## Depends on
`meeting-metadata` (date validity). Feeds `ingest-report`.
