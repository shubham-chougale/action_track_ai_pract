# Tasks — ingest-report

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [ ] **T42 Ingest pipeline end to end** — FR: FR-1..FR-12
  **Done when:** `ingest` on a small fixture folder stores the expected items with owners, dates, flags and sources.
- [ ] **T43 Counts** — FR: FR-13
  **Done when:** the report prints files scanned/ingested/skipped and items new/merged/unchanged; on the sample folder: 35 scanned (the `.md` files; the `.txt` is not counted), 31 ingested, 4 skipped.
- [ ] **T44 Skip reasons and flags in report** — FR: FR-13
  **Done when:** the report lists each of the 4 skipped files with its reason, and lists flagged items grouped as ambiguous/unknown owner, unresolved due phrase, and code-block/comment items.
- [ ] **T45 Exit codes** — FR: FR-13
  **Done when:** exit 0 with skipped notes; non-zero only for the fatal folder errors from T12.
