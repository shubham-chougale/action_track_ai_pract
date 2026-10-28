# Blockers

Living log of bugs, open decisions, and other blockers. New items go into the
open sections below as they are discovered; when resolved, they move to
**Completed** (always the last section).

## Column guide

| Column | Meaning |
|---|---|
| ID | `B-###` bug, `D-###` decision, `X-###` other blocker |
| Task | Task name from `tasks.md` the item relates to |
| Title | Short description |
| Priority | Critical / High / Medium / Low |
| Impact | What part of the project it blocks or affects |
| Source | Where it occurred (file, module, step, meeting) |
| Fix needed | What it takes to fix or decide |
| Next step / Resolution | Planned next action (open) or how it was resolved (completed) |
| Raised | Date raised (YYYY-MM-DD) |
| Resolved | Date resolved (Completed section only) |

## Bugs (Open)

| ID | Task | Title | Priority | Impact | Source | Fix needed | Next step | Raised |
|---|---|---|---|---|---|---|---|---|
| _None_ | | | | | | | | |

## Decisions (Pending)

| ID | Task | Title | Priority | Impact | Source | Fix needed | Next step | Raised |
|---|---|---|---|---|---|---|---|---|
| _None_ | | | | | | | | |

## Other Blockers (Open)

| ID | Task | Title | Priority | Impact | Source | Fix needed | Next step | Raised |
|---|---|---|---|---|---|---|---|---|
| X-001 | T65 Create one draft | `claude -p` has no Gmail connector in headless mode | High | T65 and T76 (real draft, Sent unchanged) cannot be verified; `followup` always fails with a clear error | gmail.py live run: init shows mcp_servers [], no Gmail tools, though `claude mcp list` says Gmail Connected | Make connectors available to `claude -p` (login/config), or choose another bridge (Python MCP client) | Ask user; retry live run from a normal terminal | 2026-10-28 |

## Completed

| ID | Type | Task | Title | Priority | Impact | Source | Fix needed | Resolution | Raised | Resolved |
|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | Decision | T01 | Tech stack and T1 scope | Medium | Project scaffold; tasks.md has no scaffold task (T01 is fixtures) | User request "do T1" vs tasks.md T01 | Choose stack; decide scope of T1 | Python 3.11+ + pytest chosen by user; scaffold committed, T01 left unchecked | 2026-10-28 | 2026-10-28 |
| D-002 | Decision | T09 Missing/invalid date reasons | Accept long-form meeting dates | Medium | Without it 2026-09-09-qa-standup.md and 2026-09-14-onboarding-flow-design.md would be skipped: 6 skipped and 29 ingested instead of the 4 and 31 in requirement.md section 8 | notes/2026-09-09-qa-standup.md (`9 September 2026`), notes/2026-09-14-onboarding-flow-design.md (`Monday, 14 September 2026`); modules/meeting-metadata/spec.md only lists `YYYY-MM-DD` | Decide whether non-ISO dates are valid | Accept `[Weekday,] D Month YYYY` (full or 3-letter month) as valid and normalise to YYYY-MM-DD; other text stays "invalid date". Follows requirement.md (31 ingested). modules/meeting-metadata/spec.md rule 3 updated to document long-form dates | 2026-10-28 | 2026-10-28 |
| D-003 | Decision | T11 Folder scan scope | CLAUDE.md said skip-and-report `.txt`; FR-1 says ignore silently | Medium | Would make the ingest report list the .txt as skipped (5 skipped instead of 4) and contradict T11/T13 | CLAUDE.md (hard rule "wrong extension" and edge case "Non-.md files") vs requirement.md FR-1 and section 8 check 1, modules/note-scanning/spec.md rule 2 | Pick which source wins | Followed requirement.md per the source-of-truth order: non-.md files are ignored silently (not counted, not reported). CLAUDE.md corrected: removed "wrong extension" from the malformed list and reworded the Non-.md bullet | 2026-10-28 | 2026-10-28 |
| D-004 | Decision | T65 Create one draft | How the Python CLI reaches the Gmail MCP connector | High | Blocks T65-T67, T76 and the real followup run | requirement.md FR-21/FR-22, modules/gmail-draft/spec.md | Choose the bridge | User chose: injectable DraftClient interface (fake in tests) with a real backend that shells out to `claude -p`, allowing only the Gmail create_draft tool (never send/reply/forward) | 2026-10-28 | 2026-10-28 |
