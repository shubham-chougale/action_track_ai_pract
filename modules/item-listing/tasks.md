# Tasks — item-listing

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [x] **T51 Status definitions** — FR: FR-15
  **Done when:** with `--today 2026-10-28`: open item due 10-27 → overdue; due 10-28 → open; done item with past date → done; no-date item → open; flagged item with past date → never overdue; unresolved-date item → never overdue.
- [x] **T52 Default output order and columns** — FR: FR-16
  **Done when:** all items (including done) print sorted by due date, no-due-date last, with columns ID, Owner(s), Task, Due, Status, Source; the table ends with a total count.
- [x] **T53 Due, source and flag display** — FR: FR-16
  **Done when:** unresolved date shows the raw phrase marked `?`; no date shows `-`; a flagged item shows a flag marker; a merged item shows its latest source plus the count of other mentions; a co-owned item appears under each owner.
- [ ] **T54 Empty result and JSON** — FR: FR-16
  **Done when:** a filter with no matches prints `No items match`; `--json` output parses as valid JSON with the same items as the table.
- [ ] **T55 Owner filter** — FR: FR-14
  **Done when:** `--owner "Priya Nair"` works; `--owner Priya` fails with a message listing both Priyas and non-zero exit; `--owner unassigned` shows only unassigned items.
- [ ] **T56 Status and due-before filters** — FR: FR-14
  **Done when:** `--status open|done|overdue` each return the right sets; `--due-before 2026-10-01` is strictly before and excludes no-date items; `--due-before 10/01/2026` errors with non-zero exit.
- [ ] **T57 Combined filters** — FR: FR-14
  **Done when:** owner + status + due-before together return only items satisfying all three.
- [ ] **T58 `--today` override** — FR: FR-15
  **Done when:** the same data gives different overdue sets for two `--today` values; without `--today` the computer's date is used.
