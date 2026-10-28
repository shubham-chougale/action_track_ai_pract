# Tasks — note-scanning

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [x] **T11 Folder scan scope** — FR: FR-1
  **Done when:** on the sample folder the scan lists 35 `.md` files, ignores the `.txt` silently (not in skipped list), and a fixture subfolder's `.md` is not scanned.
- [ ] **T12 Fatal folder errors** — FR: FR-1
  **Done when:** a missing path and a path that is a file each give an error message and non-zero exit.
- [ ] **T13 Malformed-note skipping** — FR: FR-5
  **Done when:** on the sample folder exactly 4 notes are skipped with reasons: 2026-09-09-notes-final-v2.md (empty), scratch.md (binary), untitled.md (no date), 2026-10-03-sales-pipeline.md (invalid date); the other 31 pass through; an unreadable file does not stop the scan.
- [ ] **T14 Deterministic scan order** — FR: FR-1, NFR
  **Done when:** two scans of the sample folder return the same order.
