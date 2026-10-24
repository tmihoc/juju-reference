---
name: juju-docs-epics
description: "The two priority JIRA epics behind the architecture-docs branch, where the notes live, and the PR-splitting context"
metadata:
  node_type: memory
  type: project
  originSessionId: 89a79675-2d3d-49fe-857d-b281559963e6
  modified: 2026-09-29T11:21:17.664Z
---

Priority epics: **JUJU-9632** (rewrite the architecture explanation) and **JUJU-9635** (illustrate the docs: 10+ diagrams + a DOCUMENTED diagram-creation process). Source branch: `4.0-docs-rewrite-juju-architecture-juju-9632` (tmihoc fork), merge-base 6469ebfa74, 318 commits.

Notes live in `~/git/ggarch/` (HANDOFF.md, TODOS.md, TODOS-archive-2026-09-26.md "batch 7" gap map ~line 820, SESSIONS.md addendum 74o) and `~/git/misc/JUJU-9632-architecture-doc-rewrite.md`. Known gap: the contributor guide page for diagram creation is NOT yet written. Backup/restore diagram is N/A on 4.0 (Backups facade is a stub).

Blocker for diagram PRs: the ggarch tool lives in the personal repo tmihoc/ggarch (Makefile pip-installs ~/git/ggarch; CI gate checks out tmihoc/ggarch@main unpinned) - needs a distribution decision before upstream can build it.

**Why:** the user must deliver both epics soon; they want the big PR split into smaller 4.1 PRs, easy uncontroversial ones first (contributor-docs dissolution, controller-config update).
**How to apply:** see [[juju-pr-workflow]] for per-PR rules.
