# Tasks — followup-email

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [x] **T59 Item selection** — FR: FR-18
  **Done when:** for Priya Nair the selection has her open and overdue items only; done, unassigned, ambiguous and flagged items are excluded; co-owned items appear for each co-owner; a merged item appears once.
- [x] **T60 Owner resolution in followup** — FR: FR-18
  **Done when:** `followup Priya` fails with the candidate list and non-zero exit; `followup "Priya Nair"` proceeds.
- [x] **T61 No-items case and unassigned count** — FR: FR-18
  **Done when:** an owner with no qualifying items creates no draft and prints a message; the run prints how many unassigned items exist.
- [x] **T62 Subject line** — FR: FR-20
  **Done when:** subject is `Action items follow-up: Priya Nair (<n> overdue, <m> open)` and n, m equal the counts in the body.
- [ ] **T63 Body layout** — FR: FR-20
  **Done when:** body is plain text, starts `Hi Priya,`, has a short intro, then **Overdue** before **Open**; each item shows task, due date (or raw phrase, or "no due date"), source meeting name and date, and item ID; no sign-off is added by the tool.
- [ ] **T64 Recipient from roster** — FR: FR-19
  **Done when:** with a roster row the recipient is that email; with no roster file or no row the draft content is still produced with no recipient and a warning printed.
