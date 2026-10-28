# actiontrack — Requirements Document

Status: Final. Open questions: none. Assumptions: none.
Source of every statement: the user's brief (B), the user's answers to clarifying questions (A), or verified inspection of the provided `notes/` folder (N).
Out of this document: tech stack, architecture, database, specification.

---

## 1. Business goal

Team meeting notes accumulate as markdown files. Action items get lost and follow-up emails are written late or never. `actiontrack` is a small command-line tool that (B):

1. reads meeting notes and extracts action items,
2. tracks each item's owner, task, due date, source and status,
3. drafts one follow-up email per owner in Gmail for the user to review. It never sends.

### Success criteria
- SC1. Ingesting the sample `notes/` folder completes without crashing and reports every skipped note with a reason.
- SC2. The same action item repeated across meetings appears once in `list`.
- SC3. Items for the two Priyas (Nair, Shah) and two Rahuls (Mehta, Verma) are never mixed up; unresolvable cases are flagged, not guessed.
- SC4. `followup <owner>` creates one Gmail draft per run and nothing is ever sent.
- SC5. Re-running `ingest` on the same folder changes nothing (no duplicates, no status resets).

## 2. Users and context
- Single user (the person running the tool on their own machine). Command line only (A).
- Platform: Windows (A).
- Recipients of drafts are teammates (owners of items). The user reviews and sends drafts manually in Gmail (B).

## 3. Out of scope (A)
Sending email; editing or writing back to the notes files (notes are read-only; done status lives only in actiontrack's own data); reminders, scheduling, calendar or chat integration; multi-user sharing; web UI; macOS and Linux; confidentiality handling (owners only receive their own items, and the user reviews every draft).

## 4. Domain facts about the provided notes (N)
The sample `notes/` folder has 36 files: 35 `.md` and 1 `.txt`. Observed variations the tool must cope with:

| Feature | Example |
|---|---|
| Header style A | `# Meeting: <title>`, `Date: YYYY-MM-DD`, `Attendees: A, B, C` |
| Header style B | YAML front matter: `title:`, `date:`, `attendees: [A, B, C]` (e.g. 2026-09-16-standup.md) |
| Checkbox markers | `- [ ]`, `- [x]`, `- [X]`, also bullets `*` and `+` |
| Nested checkboxes | Karan's item indented under Meera's (2026-09-30-q4-offsite.md) |
| Non-checkbox items | Markdown table row and `ACTION:` line in 2026-09-30-q4-offsite.md (ignored, see FR-2) |
| Decoy items | Fenced code block template and HTML-commented item in 2026-10-09-security-review.md |
| Empty file | 2026-09-09-notes-final-v2.md (0 bytes) |
| Binary file | scratch.md |
| No header/date/attendees | untitled.md |
| Unparseable date | 2026-10-03-sales-pipeline.md has `Date: sometime last week` |
| Non-note file | 2026-09-19-offsite-draft.txt |
| Name variants | `Priya`, `Priya N.`, `Priya S.`, `Rahul`, `@anita`, `Anita & Rahul`, `Lena (with Priya)` |
| Non-person owners | `Someone`, `TBD`, `Everyone`, `Team`, `Owner` (template) |
| Date phrases | `by Friday`, `by Mon`, `by tomorrow`, `EOD`, `by 2026-09-08`, `by 10 Sep`, `Wed 16 Sep`, `Oct 3rd`, `15 October`, `by next Tuesday`, `end of next week`, `mid-October`, `end of month`, `for November`, `by EOD tomorrow` |
| Repeated items | "Priya to send the revised quote to Acme" in 09-01, 09-08 (as "Priya N." with an em dash) and 09-15 (`[x]`) |
| Same-name people | Priya Nair / Priya Shah; Rahul Mehta / Rahul Verma. Both Priyas and both Rahuls attend the 2026-09-30 offsite. |

People known from Attendees lines: Priya Nair, Priya Shah, Rahul Mehta, Rahul Verma, Anita Desai, Sam Okafor, Meera Iyer, Karan Joshi, Lena Fischer.

## 5. Commands

Common: global option `--today YYYY-MM-DD` on `list` and `followup` overrides today's date. Default is the computer's current date (A).

### 5.1 `actiontrack ingest <folder>`

**FR-1 Scope of scan (A).** Scans only top-level `.md` files in `<folder>`. No subfolder recursion. Other files (e.g. `.txt`) are ignored silently and not reported. A missing folder or a path that is not a folder is a fatal error (message, non-zero exit).

**FR-2 What is an action item (A).** A line that is a markdown checkbox: bullet `-`, `*` or `+`, followed by `[ ]` (open) or `[x]`/`[X]` (done), at any indentation. Table rows and `ACTION:` lines are NOT action items. Nested checkboxes are independent items with no parent/child link.

**FR-3 Decoy items (A).** Checkbox lines inside fenced code blocks or HTML comments are extracted but marked **flagged**. Flagged items: shown in `list` with a flag marker; never counted as overdue; excluded from follow-up emails; can be dismissed with `done`.

**FR-4 Meeting metadata (A).** Meeting date and attendees come from the note body (header style A or B, FR table in section 4). The filename date is never used as a fallback.

**FR-5 Malformed notes (A).** A `.md` note is skipped entirely, with a reason in the report, if it is:
- unreadable or binary,
- empty or whitespace-only,
- missing a meeting date, or its date is not a real date.

A missing Attendees line or missing title does NOT make a note malformed. Skipped notes never stop ingestion of the others and never crash the tool.

**FR-6 Owner resolution (A).**
- Accepted forms: full name; first name; first name + initial (`Priya N.`); `@handle` (`@anita`).
- A bare first name resolves among that meeting's attendees first. If exactly one attendee has that first name, that person is the owner.
- If no attendee matches, it resolves to the single person with that first name across all notes.
- If two or more people match (e.g. `Priya` at the offsite, where both Priyas attended), or none, the owner is flagged **ambiguous/unknown**: the raw text is kept, shown in `list` and in the ingest report, and the item is excluded from follow-up emails.
- First name + initial resolves by matching the surname initial among known people.
- Names are learned from Attendees lines. The roster supplies emails only.

**FR-7 Non-person and missing owners (A).** `Someone`, `TBD`, `Everyone`, `Team`, `Owner`, or no owner at all gives the owner `Unassigned`. The original wording is preserved. These items are listed (filter with `--owner unassigned`) but never appear in follow-up emails. `followup` reports how many unassigned items exist.

**FR-8 Co-owners (A).** `A & B to…` and `A (with B) to…` produce one item with all named people as owners. It appears under each person in `list` and in each person's follow-up. One `done` closes it for everyone.

**FR-9 Task text (A).** Stored task = the line without owner and due phrase, e.g. owner Priya Nair, task `send the slides`, due resolved date. The original full line is also kept.

**FR-10 Due-date resolution (A)** relative to the meeting date:
- `YYYY-MM-DD` is used as is.
- Weekday names (`Friday`, `Mon`, `Wed 16 Sep` uses the explicit date) resolve to the first such weekday strictly after the meeting date. If the meeting is on that weekday, it is 7 days later.
- `tomorrow` = meeting date + 1; `EOD` = meeting date.
- Day+month dates without a year (`10 Sep`, `Oct 3rd`, `15 October`) use the nearest date on or after the meeting date (a December meeting saying `5 Jan` means the next January).
- `next <weekday>` resolves to a specific date.
- Phrases that cannot give one exact day (`mid-October`, `end of month`, `end of next week`, `for November`, `before the next review`) leave the due date empty. The raw phrase is kept and shown, and flagged as "unresolved date" in the ingest report. Such items are never overdue.
- No due phrase means no due date. Such items are never overdue.

**FR-11 Duplicates and merging (A).**
- Two mentions are the same item when the resolved owner(s) match and the task wording is similar after normalising case, articles, punctuation and the due phrase. Small rewording (a dropped "the", `Priya N.` vs `Priya`) must still match. Different owners never merge.
- A merged item is one row with one ID. All source notes (file and meeting date) are kept.
- The latest meeting wins for status and due date: a later `[x]` marks it done, a later `[ ]` reopens it, a later due date replaces an earlier one. A later mention with no due date does not erase an existing one.

**FR-12 Persistence and re-ingest (A).**
- IDs are short sequential numbers assigned at first ingestion, never reused, stable across re-ingests and merges.
- Re-running ingest on the same folder, or adding new notes, never creates duplicates and never resets status. It adds only new items and sources.
- A manual `done` always sticks, regardless of what any later note shows.
- Data and the roster live in a hidden `.actiontrack/` folder in the directory where the user runs the tool, so separate directories keep separate data.

**FR-13 Ingest report (A).** Printed on completion:
- files scanned / ingested / skipped,
- items new / merged / unchanged,
- each skipped file with its reason,
- flagged items: ambiguous or unknown owner, unresolved due phrase, items from code blocks or comments.

Exit status 0 even when notes were skipped. Non-zero only for fatal errors (e.g. missing folder).

### 5.2 `actiontrack list`

**FR-14 Filters (A).**
- `--owner <name>`: full name always works (case-insensitive). A first name works only if exactly one known person has it; otherwise the command fails with a message listing the matching people (e.g. Priya Nair, Priya Shah). `unassigned` is accepted.
- `--status open|done|overdue`.
- `--due-before YYYY-MM-DD`: strictly before the date. Items with no resolved due date never match. An invalid date gives an error and non-zero exit.
- Filters combine (AND).

**FR-15 Status definitions (A).**
- `done`: ticked in the latest note or marked with `done`.
- `overdue`: open AND due date strictly before today. An item due today is open. Done items, items with no due date, and flagged items are never overdue.
- `open`: anything else not done.

**FR-16 Output (A).** Default: all items, including done, sorted by due date (soonest first, no-due-date last). Text table with columns: ID, Owner(s), Task, Due (resolved date; the raw phrase marked `?` when unresolved; `-` when none), Status (open/done/overdue, plus a flag marker for flagged items), Source (file and meeting date; merged items show the latest source and the count of other mentions). Ends with a total count. An empty result prints `No items match`. `--json` gives machine-readable output.

### 5.3 `actiontrack done <id>`

**FR-17 (A).** Marks the item done and prints it (ID, owner, task). Unknown or non-numeric ID: error message, non-zero exit. Already done: prints "already done", exit 0. One ID per call. No un-do.

### 5.4 `actiontrack followup <owner>`

**FR-18 Scope (A).** One owner per run, one Gmail draft per run, using the same owner-matching rules as `--owner` (an ambiguous first name fails with the list of candidates). The draft covers that owner's open and overdue items, excluding done, unassigned, ambiguous and flagged items. If the owner has no such items, no draft is created and a message says so. Co-owned items are included for each owner. Merged duplicates appear once.

**FR-19 Recipient (A).** Recipient comes from the roster file `.actiontrack/` CSV with header `name,email` (full name exactly as in Attendees, e.g. `Priya Nair,priya.nair@example.com`). If the roster file or the person is missing, the draft is still created with no recipient and a warning is printed.

**FR-20 Draft content (A).**
- Subject: `Action items follow-up: <Full Name> (<n> overdue, <m> open)`, counts matching the email.
- Body: plain text; greeting `Hi <first name>,`; short intro line; section **Overdue** first, then **Open**. Each item shows task, due date (or raw phrase for unresolved dates, or "no due date"), source meeting name and date, and item ID.
- The user's configured Gmail signature is appended. The tool adds no sign-off of its own.

**FR-21 Never sends (B, A).** Only drafts are created, through the Gmail MCP connector. Each run creates a new draft; existing drafts are not searched or modified. The draft link/ID is printed.

**FR-22 Failure (A).** If the Gmail connector is unavailable, not signed in, or draft creation fails: clear error explaining what failed and how to retry, non-zero exit, no retry, no fallback file, no data changed.

## 6. Data the tool must keep (business view)
Per item: ID; owner(s) (resolved person, or Unassigned / ambiguous / unknown with raw text); task; original line; due date or raw unresolved phrase; status (open/done) and whether set manually; flagged marker and reason; all source mentions (file, meeting date, meeting title); first-seen order. Plus per person: full name, optional email (roster).

## 7. Non-functional requirements
- Works on Windows (A).
- Never crashes on malformed input; every problem is reported to the user (B).
- Results are deterministic for the same notes and `--today` date.
- Notes are never modified (A).

## 8. Acceptance checks on the sample folder (N)
1. `ingest notes` skips exactly these 4 `.md` files with reasons: 2026-09-09-notes-final-v2.md (empty), scratch.md (binary), untitled.md (no date), 2026-10-03-sales-pipeline.md (invalid date). The `.txt` file is ignored silently. The other 31 files ingest.
2. "Priya to send the revised quote to Acme" appears once, done (latest note 2026-09-15 ticks it).
3. The `2026-09-30` offsite items "Priya to own the hiring plan…" and "Rahul to prepare the architecture overview…" are flagged ambiguous owner (both Priyas and both Rahuls attended).
4. `Priya N.` / `Priya S.` items in billing notes resolve to Priya Nair / Priya Shah.
5. "Someone to update the CRM notes", "TBD to write the design-system changelog", "Everyone to submit…" and "Team to decide…" are Unassigned.
6. "Anita & Rahul to agree on the component API": the Rahul is resolved by that meeting's attendees (2026-09-18 lists only Rahul Mehta), giving two owners.
7. The security-review template item and the commented-out item are flagged, never overdue, absent from emails.
8. `list --owner Priya` fails listing both Priyas; `list --owner "Priya Nair"` works.
9. `followup "Priya Nair"` creates exactly one draft, no draft is sent, and a second run creates a second draft.
10. A second `ingest notes` run reports 0 new items and changes nothing, even after `done` was used.

## 9. Confirmed decisions log
Formats checkbox-only; decoys extracted+flagged; roster for emails; attendees-first name resolution; weekday = next occurrence, 7 days if same day; vague dates empty; fuzzy duplicate match same owner; latest-wins merge; unassigned excluded; co-owners one item; missing date = malformed (no filename fallback); malformed = unreadable/binary and empty; manual done sticks; overdue strictly before today; list default all by due date; owner filter full or unique first name; sequential IDs; followup one owner per run; email shows overdue first, task+due, source, ID; people from attendees; initials and @handle accepted; task text stripped; year rule nearest-on/after; nested independent; subject format; plain text + Gmail signature; always new draft; ingest report + exit 0; text table + `--json`; top-level `.md` only; `.actiontrack/` in current directory; done edge cases; flagged behaviour; roster CSV; due-before strict `YYYY-MM-DD`; `--today` flag; Gmail failure error only; no confidentiality handling; Windows only; out-of-scope list.
