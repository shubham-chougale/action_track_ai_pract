# Module: due-date-resolution

Requirements covered: FR-10.

## Purpose
Convert a due phrase into an exact date, relative to the meeting date, or leave it empty when no exact day can be determined.

## Inputs
- Raw due phrase (may be absent).
- Meeting date.

## Outputs
- Resolved date, or empty.
- Raw phrase kept when unresolved, with an "unresolved date" flag for the ingest report.

## Rules
1. `YYYY-MM-DD` is used as is.
2. Weekday names (`Friday`, `Mon`) resolve to the first such weekday strictly after the meeting date; if the meeting is on that weekday, 7 days later.
3. `Wed 16 Sep` uses the explicit date.
4. `tomorrow` = meeting date + 1. `EOD` = meeting date. `by EOD tomorrow` = meeting date + 1.
5. Day+month without a year (`10 Sep`, `Oct 3rd`, `15 October`) uses the nearest date on or after the meeting date (a December meeting saying `5 Jan` means the next January).
6. `next <weekday>` resolves to a specific date.
7. Phrases that cannot give one exact day leave the due date empty, keep the raw phrase, and are flagged "unresolved date": `mid-October`, `end of month`, `end of next week`, `for November`, `before the next review`. Such items are never overdue.
8. No due phrase means no due date; such items are never overdue.
9. Deterministic: same phrase and meeting date always give the same result.

## Phrases in the sample notes
`by Friday`, `by Mon`, `by tomorrow`, `EOD`, `by 2026-09-08`, `by 10 Sep`, `Wed 16 Sep`, `Oct 3rd`, `15 October`, `by next Tuesday`, `end of next week`, `mid-October`, `end of month`, `for November`, `by EOD tomorrow`.

## Depends on
`meeting-metadata`, `action-item-extraction`.
