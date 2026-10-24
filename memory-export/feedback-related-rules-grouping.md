---
name: related-rules-grouping
description: "In entity reference operation subsections, group all rules (even one) under one \"Related rules:\" bullet, like \"Related errors:\""
metadata:
  node_type: memory
  type: feedback
  originSessionId: d0cfeb42-a54a-422e-80b7-180e97f8c1c0
  modified: 2026-10-20T17:40:45.027Z
---

Group multiple rules of an operation under a single `*Rules:*` bullet with nested items (no "Rule:" prefix), the way errors sit under `*Errors:*`. This holds even for a single rule (user, 2026-10-20, second round).

The word "related" is dropped from both labels (user, 2026-10-20): it said nothing once both lists are grouped.

**Why:** the user (2026-10-20) saw a flat run of `Rule:` bullets next to a grouped error list and asked for consistency.
**How to apply:** per-operation shape is `Required access`, `Rules`, `Errors`. Recorded in `~/git/misc/juju-reference/page-recipe.md`; applied to the model, cloud and SSH key pages. See [[project-epic-9635-state]].
