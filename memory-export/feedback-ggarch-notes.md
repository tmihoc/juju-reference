---
name: ggarch-session-notes
description: "After substantive ggarch or architecture-docs work, update the local notes in ~/git/ggarch (HANDOFF State, SESSIONS addendum, TODOS queue, ADRs) as the work lands"
metadata:
  type: feedback
---

When work touches ggarch or the architecture-docs split, keep the private session notes in `~/git/ggarch/` current as the work lands, not at the end: `HANDOFF.md` (State block at the top of "## State"; gotchas go to Appendix B), `SESSIONS.md` (append-only addendum: what happened, WASTE/LESSONS with mechanism and cost, CHANGES), `TODOS.md` (live queue), and `adr/` for decisions that bind (tracked; HANDOFF, SESSIONS and TODOS are gitignored and must never be committed or pushed).

**Why:** the user reminded me (2026-09-29) that earlier iterations always updated these files; they are the recoverable state between sessions and the entry point for the next one.
**How to apply:** after each landed intervention, refresh the HANDOFF State; before closing, write the addendum and queue items. Run the geometry audit (`scripts/audit-geometry.py --gate`) before and after each engine edit (HANDOFF rule 3). Related: [[juju-docs-epics]], [[ggarch-ci-check-todo]].
