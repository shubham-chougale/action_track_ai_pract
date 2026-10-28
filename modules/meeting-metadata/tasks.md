# Tasks — meeting-metadata

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [ ] **T07 Meeting metadata, header style A** — FR: FR-4
  **Done when:** a style A fixture returns title, date `YYYY-MM-DD` and the attendee list.
- [ ] **T08 Meeting metadata, header style B** — FR: FR-4
  **Done when:** 2026-09-16-standup.md (YAML front matter, bracketed attendees) returns the same shape as style A.
- [ ] **T09 Missing/invalid date reasons** — FR: FR-4, FR-5
  **Done when:** untitled.md gives reason "missing date"; 2026-10-03-sales-pipeline.md gives "invalid date"; a note with `2026-02-30` gives "invalid date"; a note with no attendees and no title still returns a valid date.
- [ ] **T10 No filename-date fallback** — FR: FR-4
  **Done when:** a note named `2026-09-09-x.md` with no body date is reported missing date, not dated 2026-09-09.
