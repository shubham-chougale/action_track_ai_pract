# Tasks — action-item-extraction

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [x] **T15 Checkbox detection** — FR: FR-2
  **Done when:** `-`, `*`, `+` with `[ ]`, `[x]`, `[X]`, at any indentation, are each found with the right open/done state.
- [x] **T16 Non-items ignored** — FR: FR-2
  **Done when:** the table row and `ACTION:` line in 2026-09-30-q4-offsite.md produce no items.
- [x] **T17 Nested items independent** — FR: FR-2
  **Done when:** Karan's item nested under Meera's in the offsite note yields two separate items with no link between them.
- [x] **T18 Decoys flagged** — FR: FR-3
  **Done when:** in 2026-10-09-security-review.md the fenced-block template item and the HTML-commented item are extracted, each carries a flag with reason "code block" / "comment", and the real items are not flagged.
- [x] **T19 Split line into owner, task, due phrase** — FR: FR-9
  **Done when:** `Priya N. to send the slides by Friday` gives owner text `Priya N.`, task `send the slides`, due phrase `by Friday`, and the original line is kept verbatim; the em-dash variant from 2026-09-08 leaves no stray dash in the task text.
- [ ] **T20 Owner-less and unusual owner syntax split** — FR: FR-9, FR-7, FR-8
  **Done when:** lines with `@anita`, `Anita & Rahul`, `Lena (with Priya)`, `Someone`, and no owner each yield the expected raw owner text (or none).
