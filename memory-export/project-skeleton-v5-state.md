---
name: project-skeleton-v5-state
description: "Session 79 state of the entity reference skeleton research: v5.3 proposal, what is solid vs open, registered tests and their verdicts"
metadata:
  node_type: memory
  type: project
  originSessionId: 8c1e4c6e-570b-417b-bc47-eea27d0d6ac3
  modified: 2026-10-19T20:50:05.909Z
---

Router for a new chat: ~/git/misc/juju-reference/HANDOFF.md (queue in TODOS.md, history in SESSIONS.md). Skeleton v5.3 lives in ~/git/misc/juju-reference/skeleton-v5.md; the full record is structure-discovery-plan.md (E15 to E27 added in session 79), generated data in part-inventory.md and domain-inventories.md, scripts in experiments/e15 to e27.

**Solid (replicated or code-checked):** spine = identity + state, plus interface, dynamics, failure for topics that earn a page; scope (controller/model/both) and life column are schema-derived and version-stable; observation predictable from schema (89% vs 58%); migration is generic export plus per-domain legacy import (not a package question); authority has kinds (level, caller-scoped, owner by tag, none, inherited); exposed is not always live (client change streams are NotImplemented in 4.1); the gate must trust code, never comments.

**Open:** order of interface/observation/agent (kept as the user's causal chain, no evidence either way); exposure measure (import- and call-based both undercount; facets and HTTP/socket channels missed); claim gate layer 3 (judge with citations) only run as E27 on 11 unseen pages; fit-test gaps shrank not to zero (rounds: 94.5%, 94.9%, 98.6%).

**Why:** the user wants a predictive, explanatory skeleton grounded in code and asked "how close are we to roll out with confidence"; the honest answer was: spine yes, full skeleton not yet.

**How to apply:** pre-register each test in the plan before running; spot-check subagent findings against the code; do not reopen the user's causal-chain order; pilots (local branch wip-entity-reference-pilots, never push) got model observation and machine removal/stream edits, commits 52c8aa0c82 and later.
