# actiontrack — Task list

Sources: `requirement.md` and the 13 module specs in `modules/*/spec.md` (there is no root-level `spec.md`).
Tasks are ordered so each one only depends on earlier ones. Each task: module, FRs, and a done-when test. No code or tech-stack choices here.

Conventions for the tests:
- "Sample folder" = the provided `notes/` folder (36 files).
- "Today" is passed with `--today` wherever dates matter, so results are deterministic.
- Each task ends with its done-when test passing, plus no earlier test regressing.

---

## Phase 0 — Test fixtures

- [ ] **T01 Small fixture notes** — module: all (test support) — FR: n/a
  Build a few tiny hand-written notes under a test folder: one per header style, one with each checkbox marker, a nested pair, a code-block decoy, a comment decoy, an empty file, a binary file, a no-date file, a bad-date file, a `.txt` file.
  **Done when:** each fixture is listed in the test folder with a one-line comment of what it exercises, and the sample folder is untouched.

---

## Phase 1 — Persistence foundation

- [ ] **T02 Data folder** — module: persistence — FR-12
  Create/locate the hidden `.actiontrack/` folder in the current directory.
  **Done when:** running in directory A then directory B creates two separate `.actiontrack/` folders; data written in A is invisible from B.

- [ ] **T03 Item store: create and read** — module: persistence — FR-12, section 6
  Store an item with all fields from section 6 (owners, task, original line, due/raw phrase, status + manual flag, flag + reason, sources, first-seen order) and read it back.
  **Done when:** an item written, then read in a fresh process, returns every field unchanged.

- [ ] **T04 Sequential IDs** — module: persistence — FR-12
  **Done when:** three items get IDs 1, 2, 3; deleting nothing and re-opening the store keeps them; the next new item gets 4 (never a reused number).

- [ ] **T05 Update item without losing fields** — module: persistence — FR-12
  Add a source to an item; change status or due date.
  **Done when:** after the update, ID and first-seen order are unchanged and earlier sources are all still present.

- [ ] **T06 Manual-done marker** — module: persistence — FR-12, FR-17
  **Done when:** an item marked done manually keeps status done even after an update that sets it open from a note.

---

## Phase 2 — Reading a note

- [ ] **T07 Meeting metadata, header style A** — module: meeting-metadata — FR-4
  **Done when:** a style A fixture returns title, date `YYYY-MM-DD` and the attendee list.

- [ ] **T08 Meeting metadata, header style B** — module: meeting-metadata — FR-4
  **Done when:** 2026-09-16-standup.md (YAML front matter, bracketed attendees) returns the same shape as style A.

- [ ] **T09 Missing/invalid date reasons** — module: meeting-metadata — FR-4, FR-5
  **Done when:** untitled.md gives reason "missing date"; 2026-10-03-sales-pipeline.md gives "invalid date"; a note with `2026-02-30` gives "invalid date"; a note with no attendees and no title still returns a valid date.

- [ ] **T10 No filename-date fallback** — module: meeting-metadata — FR-4
  **Done when:** a note named `2026-09-09-x.md` with no body date is reported missing date, not dated 2026-09-09.

- [ ] **T11 Folder scan scope** — module: note-scanning — FR-1
  **Done when:** on the sample folder the scan lists 35 `.md` files, ignores the `.txt` silently (not in skipped list), and a fixture subfolder's `.md` is not scanned.

- [ ] **T12 Fatal folder errors** — module: note-scanning — FR-1
  **Done when:** a missing path and a path that is a file each give an error message and non-zero exit.

- [ ] **T13 Malformed-note skipping** — module: note-scanning — FR-5
  **Done when:** on the sample folder exactly 4 notes are skipped with reasons: 2026-09-09-notes-final-v2.md (empty), scratch.md (binary), untitled.md (no date), 2026-10-03-sales-pipeline.md (invalid date); the other 31 pass through; an unreadable file does not stop the scan.

- [ ] **T14 Deterministic scan order** — module: note-scanning — FR-1, NFR
  **Done when:** two scans of the sample folder return the same order.

---

## Phase 3 — Extracting action items

- [ ] **T15 Checkbox detection** — module: action-item-extraction — FR-2
  **Done when:** `-`, `*`, `+` with `[ ]`, `[x]`, `[X]`, at any indentation, are each found with the right open/done state.

- [ ] **T16 Non-items ignored** — module: action-item-extraction — FR-2
  **Done when:** the table row and `ACTION:` line in 2026-09-30-q4-offsite.md produce no items.

- [ ] **T17 Nested items independent** — module: action-item-extraction — FR-2
  **Done when:** Karan's item nested under Meera's in the offsite note yields two separate items with no link between them.

- [ ] **T18 Decoys flagged** — module: action-item-extraction — FR-3
  **Done when:** in 2026-10-09-security-review.md the fenced-block template item and the HTML-commented item are extracted, each carries a flag with reason "code block" / "comment", and the real items are not flagged.

- [ ] **T19 Split line into owner, task, due phrase** — module: action-item-extraction — FR-9
  **Done when:** `Priya N. to send the slides by Friday` gives owner text `Priya N.`, task `send the slides`, due phrase `by Friday`, and the original line is kept verbatim; the em-dash variant from 2026-09-08 leaves no stray dash in the task text.

- [ ] **T20 Owner-less and unusual owner syntax split** — module: action-item-extraction — FR-9, FR-7, FR-8
  **Done when:** lines with `@anita`, `Anita & Rahul`, `Lena (with Priya)`, `Someone`, and no owner each yield the expected raw owner text (or none).

---

## Phase 4 — Due dates

- [ ] **T21 Explicit dates** — module: due-date-resolution — FR-10
  **Done when:** `by 2026-09-08` → 2026-09-08; `Wed 16 Sep` → 2026-09-16.

- [ ] **T22 Weekday rule** — module: due-date-resolution — FR-10
  **Done when:** for a meeting on Tue 2026-09-01, `Friday` → 2026-09-04; for a Monday meeting, `Mon` → 7 days later; `next Tuesday` returns one specific date.

- [ ] **T23 Tomorrow and EOD** — module: due-date-resolution — FR-10
  **Done when:** `tomorrow` = meeting+1; `EOD` = meeting date; `by EOD tomorrow` = meeting+1.

- [ ] **T24 Day+month without year** — module: due-date-resolution — FR-10
  **Done when:** `10 Sep`, `Oct 3rd`, `15 October` resolve to the nearest date on/after the meeting date; a 2026-12-20 meeting with `5 Jan` → 2027-01-05.

- [ ] **T25 Unresolvable phrases** — module: due-date-resolution — FR-10
  **Done when:** `mid-October`, `end of month`, `end of next week`, `for November`, `before the next review` each give empty date, keep the raw phrase, and set the "unresolved date" flag; no phrase gives empty date with no flag.

- [ ] **T26 Determinism** — module: due-date-resolution — FR-10, NFR
  **Done when:** running every phrase in the sample notes twice gives identical results.

---

## Phase 5 — People and owners

- [ ] **T27 Learn people from attendees** — module: people-roster — FR-6
  **Done when:** after reading the sample folder the known people are exactly the 9 listed in requirement.md section 4, and no person comes from the roster.

- [ ] **T28 Roster email loading** — module: people-roster — FR-19
  **Done when:** a `name,email` CSV attaches emails by exact full name; a missing roster file, a missing person, and a row for an unknown name all load without error (the unknown name adds no person).

- [ ] **T29 Name lookup rules** — module: people-roster — FR-14, FR-18
  **Done when:** `Priya Nair` and `priya nair` find one person; `Anita` finds Anita Desai; `Priya` fails with a message listing Priya Nair and Priya Shah; `Rahul` lists both Rahuls; `unassigned` is accepted where allowed.

- [ ] **T30 Owner: full name, first name, handle** — module: owner-resolution — FR-6
  **Done when:** `Anita Desai`, `Anita` (attendee), `@anita` all resolve to Anita Desai.

- [ ] **T31 Owner: attendees-first, then global** — module: owner-resolution — FR-6
  **Done when:** a first name matching exactly one attendee resolves to them even if another person elsewhere shares it; a first name with no attendee match resolves to the single known person with that name; with no match anywhere it is "unknown".

- [ ] **T32 Owner: ambiguous** — module: owner-resolution — FR-6
  **Done when:** `Priya` and `Rahul` in 2026-09-30-q4-offsite.md resolve to "ambiguous", keep raw text, and are flagged.

- [ ] **T33 Owner: first name + initial** — module: owner-resolution — FR-6
  **Done when:** `Priya N.` → Priya Nair and `Priya S.` → Priya Shah; an initial matching nobody gives "unknown".

- [ ] **T34 Owner: non-person and missing** — module: owner-resolution — FR-7
  **Done when:** `Someone`, `TBD`, `Everyone`, `Team`, `Owner` and a line with no owner give Unassigned with original wording preserved, e.g. "Someone to update the CRM notes".

- [ ] **T35 Owner: co-owners** — module: owner-resolution — FR-8
  **Done when:** `Anita & Rahul` in 2026-09-18-design-review.md gives owners Anita Desai and Rahul Mehta (resolved by that meeting's attendees); `Lena (with Priya)` gives two owners.

---

## Phase 6 — Merging

- [ ] **T36 Task text normalisation** — module: duplicate-merging — FR-11
  **Done when:** wording that differs only by case, articles, punctuation, or the due phrase is treated as equal; clearly different tasks are not.

- [ ] **T37 Same-owner match, different-owner no match** — module: duplicate-merging — FR-11
  **Done when:** the same wording with different resolved owners stays as two items; the same owners with near-identical wording merge.

- [ ] **T38 Quote item merges across three notes** — module: duplicate-merging — FR-11
  **Done when:** "Priya to send the revised quote to Acme" from 09-01, 09-08 (`Priya N.`, em dash) and 09-15 (`[x]`) becomes one item with one ID, three sources, status done.

- [ ] **T39 Latest-wins for status** — module: duplicate-merging — FR-11
  **Done when:** a later `[x]` sets done; a later `[ ]` after that reopens it; processing notes in date order, not file order, gives the same result.

- [ ] **T40 Latest-wins for due date** — module: duplicate-merging — FR-11
  **Done when:** a later due date replaces an earlier one; a later mention with no due date keeps the existing one.

- [ ] **T41 Manual done overrides merges** — module: duplicate-merging — FR-11, FR-12
  **Done when:** after a manual `done`, a later note with `[ ]` for the same item leaves it done.

---

## Phase 7 — Ingest command and report

- [ ] **T42 Ingest pipeline end to end** — module: ingest-report, persistence (wiring) — FR-1..FR-12
  Wire scan → metadata → extract → dates → owners → merge → store.
  **Done when:** `ingest` on a small fixture folder stores the expected items with owners, dates, flags and sources.

- [ ] **T43 Counts** — module: ingest-report — FR-13
  **Done when:** the report prints files scanned/ingested/skipped and items new/merged/unchanged; on the sample folder: 35 scanned (the `.md` files; the `.txt` is not counted), 31 ingested, 4 skipped.

- [ ] **T44 Skip reasons and flags in report** — module: ingest-report — FR-13
  **Done when:** the report lists each of the 4 skipped files with its reason, and lists flagged items grouped as ambiguous/unknown owner, unresolved due phrase, and code-block/comment items.

- [ ] **T45 Exit codes** — module: ingest-report — FR-13
  **Done when:** exit 0 with skipped notes; non-zero only for the fatal folder errors from T12.

- [ ] **T46 Idempotent re-ingest** — module: persistence — FR-12, SC5
  **Done when:** a second `ingest` of the sample folder reports 0 new items, creates no duplicates, and the stored data is byte-for-byte unchanged.

- [ ] **T47 Re-ingest after done and after new notes** — module: persistence — FR-12
  **Done when:** after `done` on an item, re-ingest keeps it done; after adding one new note, only that note's new items and sources are added; existing IDs are unchanged.

- [ ] **T48 Notes untouched** — module: persistence — NFR
  **Done when:** file hashes of every note are identical before and after ingest.

---

## Phase 8 — `done` command

- [ ] **T49 Mark done** — module: mark-done — FR-17
  **Done when:** `done 3` marks item 3 done and prints its ID, owner and task.

- [ ] **T50 Done edge cases** — module: mark-done — FR-17
  **Done when:** `done 999` and `done abc` give an error and non-zero exit; a second `done 3` prints "already done" with exit 0; a co-owned item is closed for both owners; a flagged item can be dismissed.

---

## Phase 9 — `list` command

- [ ] **T51 Status definitions** — module: item-listing — FR-15
  **Done when:** with `--today 2026-10-28`: open item due 10-27 → overdue; due 10-28 → open; done item with past date → done; no-date item → open; flagged item with past date → never overdue; unresolved-date item → never overdue.

- [ ] **T52 Default output order and columns** — module: item-listing — FR-16
  **Done when:** all items (including done) print sorted by due date, no-due-date last, with columns ID, Owner(s), Task, Due, Status, Source; the table ends with a total count.

- [ ] **T53 Due, source and flag display** — module: item-listing — FR-16
  **Done when:** unresolved date shows the raw phrase marked `?`; no date shows `-`; a flagged item shows a flag marker; a merged item shows its latest source plus the count of other mentions; a co-owned item appears under each owner.

- [ ] **T54 Empty result and JSON** — module: item-listing — FR-16
  **Done when:** a filter with no matches prints `No items match`; `--json` output parses as valid JSON with the same items as the table.

- [ ] **T55 Owner filter** — module: item-listing — FR-14
  **Done when:** `--owner "Priya Nair"` works; `--owner Priya` fails with a message listing both Priyas and non-zero exit; `--owner unassigned` shows only unassigned items.

- [ ] **T56 Status and due-before filters** — module: item-listing — FR-14
  **Done when:** `--status open|done|overdue` each return the right sets; `--due-before 2026-10-01` is strictly before and excludes no-date items; `--due-before 10/01/2026` errors with non-zero exit.

- [ ] **T57 Combined filters** — module: item-listing — FR-14
  **Done when:** owner + status + due-before together return only items satisfying all three.

- [ ] **T58 `--today` override** — module: item-listing — FR-15
  **Done when:** the same data gives different overdue sets for two `--today` values; without `--today` the computer's date is used.

---

## Phase 10 — `followup` command

- [ ] **T59 Item selection** — module: followup-email — FR-18
  **Done when:** for Priya Nair the selection has her open and overdue items only; done, unassigned, ambiguous and flagged items are excluded; co-owned items appear for each co-owner; a merged item appears once.

- [ ] **T60 Owner resolution in followup** — module: followup-email — FR-18
  **Done when:** `followup Priya` fails with the candidate list and non-zero exit; `followup "Priya Nair"` proceeds.

- [ ] **T61 No-items case and unassigned count** — module: followup-email — FR-18
  **Done when:** an owner with no qualifying items creates no draft and prints a message; the run prints how many unassigned items exist.

- [ ] **T62 Subject line** — module: followup-email — FR-20
  **Done when:** subject is `Action items follow-up: Priya Nair (<n> overdue, <m> open)` and n, m equal the counts in the body.

- [ ] **T63 Body layout** — module: followup-email — FR-20
  **Done when:** body is plain text, starts `Hi Priya,`, has a short intro, then **Overdue** before **Open**; each item shows task, due date (or raw phrase, or "no due date"), source meeting name and date, and item ID; no sign-off is added by the tool.

- [ ] **T64 Recipient from roster** — module: followup-email — FR-19
  **Done when:** with a roster row the recipient is that email; with no roster file or no row the draft content is still produced with no recipient and a warning printed.

---

## Phase 11 — Gmail draft

- [ ] **T65 Create one draft** — module: gmail-draft — FR-21
  **Done when:** against the Gmail connector, `followup "Priya Nair"` creates exactly one draft, prints its link/ID, and no message is sent (the Sent folder is unchanged).

- [ ] **T66 Always new draft** — module: gmail-draft — FR-21
  **Done when:** running followup twice creates two drafts; the first draft is not modified or searched for.

- [ ] **T67 Connector failure** — module: gmail-draft — FR-22
  **Done when:** with the connector unavailable or signed out, the command prints what failed and how to retry, exits non-zero, does not retry, writes no fallback file, and the stored data is unchanged.

---

## Phase 12 — Acceptance on the sample folder (requirement.md section 8)

- [ ] **T68 Check 1: skips** — **Done when:** `ingest notes` skips exactly the 4 listed `.md` files with reasons, ignores the `.txt`, ingests 31. (SC1)
- [ ] **T69 Check 2: quote item** — **Done when:** `list` shows "Priya to send the revised quote to Acme" once, done. (SC2)
- [ ] **T70 Check 3: offsite ambiguity** — **Done when:** "Priya to own the hiring plan…" and "Rahul to prepare the architecture overview…" are flagged ambiguous owner. (SC3)
- [ ] **T71 Check 4: billing initials** — **Done when:** `Priya N.` / `Priya S.` billing items show Priya Nair / Priya Shah. (SC3)
- [ ] **T72 Check 5: unassigned** — **Done when:** "Someone to update the CRM notes", "TBD to write the design-system changelog", "Everyone to submit…", "Team to decide…" all appear under `--owner unassigned`.
- [ ] **T73 Check 6: co-owners** — **Done when:** "Anita & Rahul to agree on the component API" has owners Anita Desai and Rahul Mehta.
- [ ] **T74 Check 7: decoys** — **Done when:** the security-review template item and commented item are flagged, never overdue, and absent from every follow-up draft.
- [ ] **T75 Check 8: owner filter** — **Done when:** `list --owner Priya` fails listing both Priyas; `list --owner "Priya Nair"` works.
- [ ] **T76 Check 9: followup drafts** — **Done when:** `followup "Priya Nair"` creates one draft, sends nothing, and a second run creates a second draft. (SC4)
- [ ] **T77 Check 10: re-ingest** — **Done when:** after using `done`, a second `ingest notes` reports 0 new items and changes nothing. (SC5)
- [ ] **T78 Never-crash sweep** — **Done when:** every command run against the sample folder, the fixtures, and a folder of garbage files produces a message or report and never a crash; the notes folder stays unmodified. (NFR)
- [ ] **T79 Windows run** — **Done when:** T68–T78 pass on Windows from a normal terminal, including paths with spaces.

---

## Coverage check

| FR | Tasks |
|---|---|
| FR-1 | T11, T12, T14 |
| FR-2 | T15, T16, T17 |
| FR-3 | T18 |
| FR-4 | T07–T10 |
| FR-5 | T09, T13 |
| FR-6 | T27, T29–T33 |
| FR-7 | T20, T34 |
| FR-8 | T20, T35 |
| FR-9 | T19, T20 |
| FR-10 | T21–T26 |
| FR-11 | T36–T41 |
| FR-12 | T02–T06, T41, T46, T47 |
| FR-13 | T43–T45 |
| FR-14 | T55–T57 |
| FR-15 | T51, T58 |
| FR-16 | T52–T54 |
| FR-17 | T49, T50 |
| FR-18 | T59–T61 |
| FR-19 | T28, T64 |
| FR-20 | T62, T63 |
| FR-21 | T65, T66 |
| FR-22 | T67 |

---

## Task ownership (split into `modules/*/tasks.md`)

Each task is owned by exactly one module, except the cross-cutting tasks below, which live only in this file.

- **Cross-cutting (no single module):** T01 (test fixtures, module: all) and T68–T79 (Phase 12 acceptance on the sample folder and never-crash/Windows sweeps).
- **T42 (ingest pipeline end to end)** names two modules, `ingest-report` and `persistence` (wiring). It is owned by `ingest-report` (the `ingest` command); `persistence` is a dependency, not a second owner.
