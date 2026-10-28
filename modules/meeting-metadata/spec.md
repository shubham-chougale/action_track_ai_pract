# Module: meeting-metadata

Requirements covered: FR-4 (supports FR-5, FR-6, FR-10).

## Purpose
Read the meeting title, date and attendees from the note body.

## Inputs
- Text of one note.

## Outputs
- Meeting title (optional).
- Meeting date (required for the note to be ingested).
- Attendee list as full names (optional).
- Or a failure reason: date missing / date not a real date.

## Rules
1. Two header styles must be recognised:
   - Style A: `# Meeting: <title>`, `Date: YYYY-MM-DD`, `Attendees: A, B, C`.
   - Style B: YAML front matter with `title:`, `date:`, `attendees: [A, B, C]` (e.g. 2026-09-16-standup.md).
2. The meeting date comes only from the note body. The filename date is never used as a fallback.
3. A date that is not a real calendar date (e.g. `sometime last week`, `2026-02-30`) is reported as invalid.
4. Missing attendees or missing title is allowed; the note is still usable.
5. Attendee names are the source from which `people-roster` learns people.

## Edge cases
- untitled.md: no header, date or attendees: reported as missing date.
- 2026-10-03-sales-pipeline.md: `Date: sometime last week`: reported as invalid date.
- Attendees written in either list style (comma separated line or bracketed list).

## Depends on
None. Used by `note-scanning`, `owner-resolution`, `due-date-resolution`, `people-roster`.
