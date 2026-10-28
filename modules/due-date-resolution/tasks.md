# Tasks — due-date-resolution

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [x] **T21 Explicit dates** — FR: FR-10
  **Done when:** `by 2026-09-08` → 2026-09-08; `Wed 16 Sep` → 2026-09-16.
- [ ] **T22 Weekday rule** — FR: FR-10
  **Done when:** for a meeting on Tue 2026-09-01, `Friday` → 2026-09-04; for a Monday meeting, `Mon` → 7 days later; `next Tuesday` returns one specific date.
- [ ] **T23 Tomorrow and EOD** — FR: FR-10
  **Done when:** `tomorrow` = meeting+1; `EOD` = meeting date; `by EOD tomorrow` = meeting+1.
- [ ] **T24 Day+month without year** — FR: FR-10
  **Done when:** `10 Sep`, `Oct 3rd`, `15 October` resolve to the nearest date on/after the meeting date; a 2026-12-20 meeting with `5 Jan` → 2027-01-05.
- [ ] **T25 Unresolvable phrases** — FR: FR-10
  **Done when:** `mid-October`, `end of month`, `end of next week`, `for November`, `before the next review` each give empty date, keep the raw phrase, and set the "unresolved date" flag; no phrase gives empty date with no flag.
- [ ] **T26 Determinism** — FR: FR-10, NFR
  **Done when:** running every phrase in the sample notes twice gives identical results.
