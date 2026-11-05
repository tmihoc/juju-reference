# Live queue (rewritten 2026-11-05; the previous queue is `archive/TODOS-session-129.md`)

Ordered. Each item names the epic it serves and how to know it is done.

## Do first: audit the PR with the procedure (JUJU-10585)

1. **Audit the PR against its base (e5db99d585) in refactor mode**, not only its additions. Size: 148 commits; 87 hand-written files, +7,600 and -3,600 lines; 15 pages added, 13 files deleted; about 24 pages with real churn (reference pages lose 1,150 lines to rewrites). Order by lines removed: `secret`, `charm`, `relation`, `user`, `machine`, `telemetry`, `storage`, `constraint`, `database`, `manage-models`, then the 15 added pages. For each, classify removed statements (moved, obsolete, duplicate, dropped), check the added ones (true, necessary, placed), and check every old label and URL. Pilot done: `method/evidence/audit-pilot-metadata.md` (found a candidate regression: the simplestreams data layout is nowhere in the PR's docs). Done when every changed page has a recorded verdict. Revise the procedure only where the audit shows it failing.
2. **Fix what the audit and E83 found**: the upgrade guide backup section and the SSH follow-ups (`method/evidence/ssh-documentation-decision.md`, residual checks 1 to 5). Needs the user's approval per change.
3. **Coverage**: reconcile the 35 selected pages with the full reference scope once the Jira acceptance text is available.

## JUJU-10586: error contract

4. **Per-call verification**: for each documented call, trace message, code, trigger and remediation from the raise site to the client rendering; design the association-level drift check. The current checker matches text only. Open: Q5 (home of an error raised by several calls).
5. **How-to troubleshooting links** to the error entries once their homes are fixed.

## JUJU-9635: figures

6. **Rendered anchor `#action-task-status`** (missing target; the single-view visitor drops node IDs). Review the extension scope, then repair with approval.
7. **Figure acceptance**: for each selected view check source, caption, alt text, light and dark rendering, and `ggarch check`. Settle the contributor and feedback process. Done when each figure has a recorded check.

## Later: the mechanism (do not let it displace the PR)

8. **Settle the open questions only when the audit hits them**: Q1 (relevant level, question templates), Q2 (page versus section), Q3 (section grammar), Q8 (unit of a development). No standalone validation study; a further comparison against past developments only if the audit shows the procedure cannot decide.
9. **Package the mechanism** as an `AGENTS` rule or a skill once the audit has exercised it. Done when it reproduces the E83 and SSH results.

## Block in progress (2026-11-05)

Plan: `experiments/PLAN-unsupervised-1.md`. Done: reviewer-agent design (`method/reviewer-agent.md`), rule ledger (`method/rule-derivation.md`), review-mode contract (`method/review-mode-contract.md`), cold runs on `status` (x2), `constraint` and `relation` with findings, comparison and placement determinacy (`experiments/`), source-drift check against the new tip, lens-list draft. New branch `4.1-docs-reference-principles` in `~/git/misc/juju-reference-principles` (no commits).

Next: (1) trace the claimed findings of the three pages (about 60 are unverified); (2) a second cold run with placements on `relation` for an agreement figure; (3) calibrate the reviewer agent on `status` and one clean page; (4) fix the contract failures listed in the cold-run notes (false-by-enumeration type, defect types for R23, R24 and layout markup, confidence for a self-contradicting source, error class for agent-consumed errors, code open); (5) decide Q5 and Q3 with the placement evidence; (6) corrections to our PR #23661 pages found along the way (audit rows for `constraint` and `relation` now say do not restore the old text as written).

## PR description (needs the user to post)

10. **Collect, per epic, the list of what its lens let the PR cover** (truth, relevance, sufficiency, placement, clarity, errors, figures), for the PR body: how the PR connects to JUJU-9635, JUJU-10585 and JUJU-10586, and why going deep (per-call traces, per-statement source traces, the figure-removal test) is how the PR reached wide. Sources: `method/evidence/audit-pr23661.md`, `experiments/cold-run-*`, the per-call error traces. Draft the lists; the user pastes the body.

## Needs the user

Jira acceptance text; the four 402-denied scopes; approval of any concrete page, rule, tool or figure change; each push; the PR body; whether to commit the archive records.

## Parked

Everything else from the previous queue is in `archive/TODOS-session-129.md`, including the Pending reference edits, the E34 manifest follow-ups and the reviewer notes. Defects and leads: `epics/source-questions.md`.
