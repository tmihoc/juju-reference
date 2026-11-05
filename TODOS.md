# Live queue (rewritten 2026-11-05; the previous queue is `archive/TODOS-session-129.md`)

Ordered. Each item names the epic it serves and how to know it is done.

## Mechanism (serves all three epics and what comes after)

1. **Test procedure v2 on new developments (E84).** Choose six or more merged PRs from code-side facts only, covering kinds E83 missed (a removal, a configuration key, a status or hook change, an error change). Predict, then compare. Stop when two consecutive rounds need no rule change. Done when the results file records thresholds and failures.
2. **Settle the open questions that block decisions**: Q1 (relevant level, question templates), Q2 (page versus section by change-coupling and reading paths), Q3 (does the section grammar follow source artifact classes), Q8 (unit of a development). Done when each has a registered test and a result.
3. **Package the mechanism**: turn `method/requirement-set.md` and `method/docs-decision-procedure.md` into an `AGENTS` rule or a skill that takes "we built X" and returns the documentation change set with traces. Done when it reproduces the E83 and SSH results.

## JUJU-10585: reference

4. **Audit the PR's additions with the procedure**: for the 12 new pages and the larger additions, apply the necessity test (R27) and the ownership rules. Output keep, trim or move per item plus a backlog. Done when every added page has a recorded justification.
5. **Fix what the audit and E83 found**: the upgrade guide backup section and the SSH follow-ups (`method/evidence/ssh-documentation-decision.md`, residual checks 1 to 5). Needs the user's approval per change.
6. **Coverage**: reconcile the 35 selected pages with the full reference scope once the Jira acceptance text is available.

## JUJU-10586: error contract

7. **Per-call verification**: for each documented call, trace message, code, trigger and remediation from the raise site to the client rendering; design the association-level drift check. The current checker matches text only. Open: Q5 (home of an error raised by several calls).
8. **How-to troubleshooting links** to the error entries once their homes are fixed.

## JUJU-9635: figures

9. **Rendered anchor `#action-task-status`** (missing target; the single-view visitor drops node IDs). Review the extension scope, then repair with approval.
10. **Figure acceptance**: for each selected view check source, caption, alt text, light and dark rendering, and `ggarch check`. Settle the contributor and feedback process. Done when each figure has a recorded check.

## Needs the user

Jira acceptance text; the four 402-denied scopes; approval of any concrete page, rule, tool or figure change; each push; the PR body; whether to commit the archive records.

## Parked

Everything else from the previous queue is in `archive/TODOS-session-129.md`, including the Pending reference edits, the E34 manifest follow-ups and the reviewer notes. Defects and leads: `epics/source-questions.md`.
