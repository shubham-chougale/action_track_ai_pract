# Tasks — people-roster

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [ ] **T27 Learn people from attendees** — FR: FR-6
  **Done when:** after reading the sample folder the known people are exactly the 9 listed in requirement.md section 4, and no person comes from the roster.
- [ ] **T28 Roster email loading** — FR: FR-19
  **Done when:** a `name,email` CSV attaches emails by exact full name; a missing roster file, a missing person, and a row for an unknown name all load without error (the unknown name adds no person).
- [ ] **T29 Name lookup rules** — FR: FR-14, FR-18
  **Done when:** `Priya Nair` and `priya nair` find one person; `Anita` finds Anita Desai; `Priya` fails with a message listing Priya Nair and Priya Shah; `Rahul` lists both Rahuls; `unassigned` is accepted where allowed.
