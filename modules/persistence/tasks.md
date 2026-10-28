# Tasks — persistence

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [x] **T02 Data folder** — FR: FR-12
  **Done when:** running in directory A then directory B creates two separate `.actiontrack/` folders; data written in A is invisible from B.
- [x] **T03 Item store: create and read** — FR: FR-12, section 6
  **Done when:** an item written, then read in a fresh process, returns every field unchanged.
- [ ] **T04 Sequential IDs** — FR: FR-12
  **Done when:** three items get IDs 1, 2, 3; deleting nothing and re-opening the store keeps them; the next new item gets 4 (never a reused number).
- [ ] **T05 Update item without losing fields** — FR: FR-12
  **Done when:** after the update, ID and first-seen order are unchanged and earlier sources are all still present.
- [ ] **T06 Manual-done marker** — FR: FR-12, FR-17
  **Done when:** an item marked done manually keeps status done even after an update that sets it open from a note.
- [ ] **T46 Idempotent re-ingest** — FR: FR-12, SC5
  **Done when:** a second `ingest` of the sample folder reports 0 new items, creates no duplicates, and the stored data is byte-for-byte unchanged.
- [ ] **T47 Re-ingest after done and after new notes** — FR: FR-12
  **Done when:** after `done` on an item, re-ingest keeps it done; after adding one new note, only that note's new items and sources are added; existing IDs are unchanged.
- [ ] **T48 Notes untouched** — FR: NFR
  **Done when:** file hashes of every note are identical before and after ingest.
