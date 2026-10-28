# Tasks — owner-resolution

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [x] **T30 Owner: full name, first name, handle** — FR: FR-6
  **Done when:** `Anita Desai`, `Anita` (attendee), `@anita` all resolve to Anita Desai.
- [x] **T31 Owner: attendees-first, then global** — FR: FR-6
  **Done when:** a first name matching exactly one attendee resolves to them even if another person elsewhere shares it; a first name with no attendee match resolves to the single known person with that name; with no match anywhere it is "unknown".
- [x] **T32 Owner: ambiguous** — FR: FR-6
  **Done when:** `Priya` and `Rahul` in 2026-09-30-q4-offsite.md resolve to "ambiguous", keep raw text, and are flagged.
- [ ] **T33 Owner: first name + initial** — FR: FR-6
  **Done when:** `Priya N.` → Priya Nair and `Priya S.` → Priya Shah; an initial matching nobody gives "unknown".
- [ ] **T34 Owner: non-person and missing** — FR: FR-7
  **Done when:** `Someone`, `TBD`, `Everyone`, `Team`, `Owner` and a line with no owner give Unassigned with original wording preserved, e.g. "Someone to update the CRM notes".
- [ ] **T35 Owner: co-owners** — FR: FR-8
  **Done when:** `Anita & Rahul` in 2026-09-18-design-review.md gives owners Anita Desai and Rahul Mehta (resolved by that meeting's attendees); `Lena (with Priya)` gives two owners.
