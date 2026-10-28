# Module: ingest-report

Requirements covered: FR-13 (SC1).

## Purpose
Tell the user what `actiontrack ingest` did and what needs attention.

## Inputs
- Results from `note-scanning`, `owner-resolution`, `due-date-resolution`, `action-item-extraction`, `duplicate-merging`.

## Output (printed on completion)
- Files scanned / ingested / skipped.
- Items new / merged / unchanged.
- Each skipped file with its reason.
- Flagged items, grouped by cause:
  - ambiguous or unknown owner (raw text shown),
  - unresolved due phrase (raw phrase shown),
  - item found in a code block or HTML comment.

## Rules
1. Exit status 0 even when notes were skipped.
2. Non-zero exit only for fatal errors (e.g. missing folder).
3. Every problem found is reported; nothing is dropped silently, except non-`.md` files, which are ignored by design.
4. Re-ingest of the same folder reports 0 new items.

## Depends on
`note-scanning`, `action-item-extraction`, `owner-resolution`, `due-date-resolution`, `duplicate-merging`.
