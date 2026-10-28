# Tasks — gmail-draft

Tasks owned by this module, copied from the top-level `tasks.md` (do not edit here; change the top-level file and re-split).

- [ ] **T65 Create one draft** — FR: FR-21
  **Done when:** against the Gmail connector, `followup "Priya Nair"` creates exactly one draft, prints its link/ID, and no message is sent (the Sent folder is unchanged).
- [x] **T66 Always new draft** — FR: FR-21
  **Done when:** running followup twice creates two drafts; the first draft is not modified or searched for.
- [x] **T67 Connector failure** — FR: FR-22
  **Done when:** with the connector unavailable or signed out, the command prints what failed and how to retry, exits non-zero, does not retry, writes no fallback file, and the stored data is unchanged.
