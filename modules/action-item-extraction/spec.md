# Module: action-item-extraction

Requirements covered: FR-2, FR-3, FR-9 (acceptance check 8.7).

## Purpose
Find action items in a note's text, mark decoys as flagged, and split each line into owner text, task text and due phrase.

## Inputs
- Text of one valid note.

## Outputs
Per item:
- original full line,
- raw owner text, raw due phrase (either may be absent),
- task text (line without owner and due phrase),
- checked state (open / done),
- flagged marker with reason (code block or HTML comment), if any.

## Rules
1. An action item is a markdown checkbox line: bullet `-`, `*` or `+`, then `[ ]` (open) or `[x]` / `[X]` (done), at any indentation.
2. Table rows and `ACTION:` lines are NOT action items.
3. Nested checkboxes are independent items; no parent/child link.
4. Checkbox lines inside fenced code blocks or HTML comments are still extracted but flagged.
5. Task text is the line with owner and due phrase removed. Example: owner Priya Nair, task `send the slides`, due resolved date.
6. The original full line is always kept.

## Edge cases
- 2026-09-30-q4-offsite.md: Karan's item nested under Meera's yields two independent items; the table row and `ACTION:` line yield none.
- 2026-10-09-security-review.md: template item in a fenced block and the commented-out item are both flagged.
- Em dashes and other punctuation between owner, task and due phrase must not leak into the task text.

## Depends on
None. Feeds `owner-resolution`, `due-date-resolution`, `duplicate-merging`.
