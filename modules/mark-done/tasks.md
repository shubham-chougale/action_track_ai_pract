# Tasks — mark-done

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [x] **T49 Mark done** — FR: FR-17
  **Done when:** `done 3` marks item 3 done and prints its ID, owner and task.
- [x] **T50 Done edge cases** — FR: FR-17
  **Done when:** `done 999` and `done abc` give an error and non-zero exit; a second `done 3` prints "already done" with exit 0; a co-owned item is closed for both owners; a flagged item can be dismissed.
