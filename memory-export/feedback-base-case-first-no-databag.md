---
name: feedback-base-case-first-no-databag
description: Page rules from 2026-10-21: base case first, kinds go in the data model, status transitions live in the changing operation, never say "databag", draw records and software apart
metadata:
  type: feedback
---

- The base case comes first, then the variants (relation page: regular, then peer, subordinate, cross-model).
- Kinds that records decide are described in the data model bullet of the deciding record, like the cloud types on the cloud page.
- A status's allowed values sit in the data model. Its state diagram and transitions sit in the operation that changes it.
- Never write "databag". A staff developer says it is community corruption and the codebase says records or settings. Say "settings" (`relation_unit_settings`, `relation_application_settings`).
- A figure shows records or software, never both. An entity-relationship view for records, a sequence view for software. The old Excalidraw relation figure mixed them and was weird.

**Why:** User corrections and a staff developer's view, 2026-10-21. Copied to page-recipe.md.

**How to apply:** Check each new page for these before showing it. See [[feedback-no-comma-and-clauses]] and [[feedback-page-form-rules]].
