---
name: check-prior-decisions
description: Before building something that revisits a design question, think whether it makes sense and look in the decision record for a prior verdict; the user remembers past decisions
metadata:
  type: feedback
---

When the user asks for a change that touches a design question (cardinality numbers on chip diagrams, table versus nested errors, where watchers sit), stop and think whether it makes sense first, and search the decision record (ggarch HANDOFF.md, SESSIONS.md, adr/, the plan file) for a prior verdict before touching code.

**Why:** on 2026-10-19 I started patching ggarch to draw schema-derived cardinality numbers on chips. The user interrupted twice ("Don't jump into implementation -- first try to think whether it makes sense", "I think we thought about this before and decided against it"). The record did say "Cardinality grounded: never drawn", and my own check showed the numbers would mislead (optional satellites would read 1:1). I had to revert the patch.

**How to apply:** when a request sounds like it was settled earlier, grep the notes first, state what the record says, and only then decide whether to reopen it. Prefer stating the fact in caption or prose over changing a tool. Related: [[no-verdict-asking]], [[dpe-generalization]].
