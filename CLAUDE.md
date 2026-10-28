# Project instructions

## Project: actiontrack

Team meeting notes pile up as markdown files; action items get lost and
follow-up emails are late or never written. `actiontrack` is a small CLI that
reads meeting notes, tracks action items, and drafts follow-up emails for
review. Single user, runs locally on Windows, command line only.

Source of truth, in order: `requirement.md` (what), `modules/*/spec.md` (13
module specs, no root-level spec), `tasks.md` (ordered build tasks with
done-when tests), `Scenario.md` (original brief). Sample input is `notes/`
(36 files, several long/messy, some deliberately malformed). If sources
conflict, follow `requirement.md` and log the conflict in `blockers.md`.
Tech stack is not fixed by the docs; ask before choosing one.

## Commands

1. `actiontrack ingest <folder>`: parse every `.md` meeting note in the folder.
   Each note has a date, attendees, and free-form text; action items appear as
   lines like `- [ ] Priya to send the revised quote by Friday`. Store each item
   with owner, task, due date (relative dates like "Friday" resolved to a real
   date), source file, and status. Report skipped notes with a reason.
2. `actiontrack list`: show items. Filters: `--owner`, `--status
   open|done|overdue`, `--due-before <date>`. Overdue = open and past due.
3. `actiontrack done <id>`: mark an item done.
4. `actiontrack followup <owner>`: one email per owner covering their open and
   overdue items; create a Gmail draft via the Gmail MCP connector. Never send.

## Hard rules

- **Never send email.** Only create drafts (`create_draft`). Never call
  `send_message`, `reply`, or `forward`. The user reviews and sends manually.
- **Never crash on bad input.** Malformed notes (bad/missing date, empty file,
  binary file, broken structure) are skipped and reported with
  the file name and reason. The run continues.
- **Never guess an owner.** If a name is ambiguous or unresolvable, flag the
  item instead of assigning it.
- **Ingest is idempotent.** Re-running `ingest` on the same folder must not
  create duplicates or reset statuses (e.g. a `done` item stays `done`).
- **Dates are deterministic.** Support a `--today <date>` option wherever dates
  matter (relative-date resolution, overdue) so tests give stable results.
- Don't modify `notes/`; it is read-only input.

## Edge cases the tool must handle

- **Duplicates:** the same item repeated across several meetings appears once
  in `list` (merge, keep every source reference).
- **No owner or no due date:** keep the item; show it as unassigned / no due
  date. Do not drop it and do not invent values.
- **Same first name:** two Priyas (Nair, Shah) and two Rahuls (Mehta, Verma)
  must never be mixed up. Resolve using attendees/context, otherwise flag.
- **Malformed notes:** skip, report, continue (see hard rules).
- **Markers and decoys:** handle the different checkbox markers and header
  styles; ignore checkbox-looking lines inside code blocks and comments.
- **Non-`.md` files** (e.g. `.txt`) are not notes; ignore silently (not counted,
  not reported). See FR-1.

## Module map

Each module has `modules/<name>/spec.md`; read the spec before touching it.
Modules: `note-scanning`, `meeting-metadata`, `action-item-extraction`,
`owner-resolution`, `people-roster`, `due-date-resolution`,
`duplicate-merging`, `persistence`, `ingest-report`, `item-listing`,
`mark-done`, `followup-email`, `gmail-draft`.

## Working style

- Work task by task in `tasks.md` order; each task depends only on earlier
  ones. A task is done only when its done-when test passes and no earlier test
  regresses. Tick the task's checkbox in `tasks.md` when done.
- Match existing style and keep changes minimal and scoped to the task.
- Tests use small fixtures (T01) plus the full sample `notes/` folder.
- Before running destructive or outward-facing actions, confirm first.
- Whenever you need to ask the user a question, use the AskUserQuestion tool.
- Don't commit unless asked.

## Task completion (`tasks.md`)

- When a task is completed, mark it done right away: change `[ ]` to `[x]` in
  **both** the module's `modules/<name>/tasks.md` and the top-level `tasks.md`.
  Cross-cutting tasks (T01, T68-T79) and T42 exist only in the top-level file
  or the owning module; tick every place the task appears.
- Only tick a task after its done-when test passes (and no earlier test
  regresses).
- If a task is partially done or blocked, leave it unchecked and add a short
  note under it explaining why (also log blockers in `blockers.md`).

## Blocker tracking (`blockers.md`)

Keep `blockers.md` up to date automatically, without being asked:

- When a bug, an unresolved decision, or any other blocker comes up (failing
  test, error we can't get past, missing info, open design/tech choice, external
  dependency), add it right away to the matching open section: **Bugs (Open)**,
  **Decisions (Pending)**, or **Other Blockers (Open)**.
- Each entry is one table row with a unique ID (`B-001` bug, `D-001` decision,
  `X-001` other) and every column filled in (see the column guide in
  `blockers.md`): task name, title, priority, impact, source (where it
  occurred), fix needed, next step, and date raised.
- When one is resolved (fix landed, decision made, blocker cleared), remove its
  row from the open table and add a row to **Completed** with its type, the
  resolution, and the resolved date.
- **Completed** must remain the last section of the file.
- Replace the `_None_` placeholder row when a table gets its first entry, and
  restore it if a table becomes empty.
- Don't add duplicates; check existing entries first.

## Keeping this file short

Keep `CLAUDE.md` under 200 lines. Put detail in `requirement.md` or module
specs and link to it here instead of copying it.
