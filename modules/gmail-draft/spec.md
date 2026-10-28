# Module: gmail-draft

Requirements covered: FR-21, FR-22 (SC4; acceptance check 8.9).

## Purpose
Create the follow-up email as a Gmail draft through the Gmail MCP connector. Never send.

## Inputs
- Recipient (optional), subject, plain-text body from `followup-email`.

## Output
- The draft link or ID, printed to the user.

## Rules
1. Only drafts are created. Nothing is ever sent.
2. Each run creates a new draft. Existing drafts are not searched or modified, so a second run creates a second draft.
3. Failure (connector unavailable, not signed in, or draft creation fails):
   - clear error saying what failed and how to retry,
   - non-zero exit,
   - no retry, no fallback file,
   - no data changed.
4. A missing recipient does not block the draft (the warning comes from `followup-email`).

## Depends on
`followup-email`. External: Gmail MCP connector.
