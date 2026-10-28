# Tasks — duplicate-merging

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [x] **T36 Task text normalisation** — FR: FR-11
  **Done when:** wording that differs only by case, articles, punctuation, or the due phrase is treated as equal; clearly different tasks are not.
- [ ] **T37 Same-owner match, different-owner no match** — FR: FR-11
  **Done when:** the same wording with different resolved owners stays as two items; the same owners with near-identical wording merge.
- [ ] **T38 Quote item merges across three notes** — FR: FR-11
  **Done when:** "Priya to send the revised quote to Acme" from 09-01, 09-08 (`Priya N.`, em dash) and 09-15 (`[x]`) becomes one item with one ID, three sources, status done.
- [ ] **T39 Latest-wins for status** — FR: FR-11
  **Done when:** a later `[x]` sets done; a later `[ ]` after that reopens it; processing notes in date order, not file order, gives the same result.
- [ ] **T40 Latest-wins for due date** — FR: FR-11
  **Done when:** a later due date replaces an earlier one; a later mention with no due date keeps the existing one.
- [ ] **T41 Manual done overrides merges** — FR: FR-11, FR-12
  **Done when:** after a manual `done`, a later note with `[ ]` for the same item leaves it done.
