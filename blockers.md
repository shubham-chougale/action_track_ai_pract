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
| _None_ | | | | | | | | |

## Completed

| ID | Type | Task | Title | Priority | Impact | Source | Fix needed | Resolution | Raised | Resolved |
|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | T01 | Tech stack and T1 scope | Medium | Project scaffold; tasks.md has no scaffold task (T01 is fixtures) | User request "do T1" vs tasks.md T01 | Choose stack; decide scope of T1 | Python (setuptools, pytest) chosen; scaffold done without ticking T01, fixtures still pending | Python 3.11+ + pytest chosen by user; scaffold committed, T01 left unchecked | 2026-10-28 | 2026-10-28 |
