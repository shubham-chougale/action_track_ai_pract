# Module: mark-done

Requirements covered: FR-17 (and the "manual done sticks" rule of FR-12).

## Purpose
`actiontrack done <id>`: mark one item as done by hand.

## Inputs
- One item ID.

## Behaviour
1. Marks the item done (recorded as set manually) and prints it: ID, owner, task.
2. Co-owned items: one `done` closes the item for everyone.
3. Works on flagged items too (this is how a decoy is dismissed).
4. Unknown or non-numeric ID: error message, non-zero exit.
5. Already done: prints "already done", exit 0.
6. One ID per call. No undo.
7. A manual `done` sticks: later notes, including a later `[ ]`, never reopen it.

## Depends on
`persistence`.
