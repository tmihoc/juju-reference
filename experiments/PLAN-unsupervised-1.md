# Plan: first unsupervised half hour (2026-11-05)

**Goal served:** a solid 3-epic PR on `4.1-docs-reference-principles`, built by a check that can say why upstream is wrong and justify every change. This block advances the evidence that the check works (agreement across runs, drift against the new tip) and prepares the reviewer and the PR-description lists.

**Gates (hold for the whole block):** no edits to pages, rules, tools, figures or the checker; no writes outside `~/git/misc/juju-reference` (and the scratchpad); no push; no commit; never touch `~/git/juju` or the new worktree; cold agents write only under `experiments/`. If a step fails, record it in `notes` and go on.

| # | Step | Done when | State |
|---|---|---|---|
| 1 | Check that source traced at `e5db99d585` still holds at the new tip `52e983a435` | Traced status and secret files show no diff; relation domain has 1 changed file, noted | Done: no diff in 8 traced files; `domain/relation` has one changed non-test file; `cmd/juju/status` and `core/status/status.go` changed (machine modification status removed), outside the unit and application traces |
| 2 | Cold runs on `relation` and `constraint` at the new tip, two agents in parallel | Both return findings, draft, trace, placements | Launched |
| 3 | Write the reviewer-agent design | `method/reviewer-agent.md` | Done |
| 4 | Compare cold runs 1 and 2 on `status` (statements kept, dropped, added; anchors) | `experiments/cold-run-compare-status.md` | |
| 5 | Verify the five highest-severity findings of runs 3 per page against source at the new tip | A verified list per page; failures recorded | After step 2 returns |
| 6 | Compute placement agreement where two runs exist; record determinacy for runs 2 and 3 | One table | After step 2 |
| 7 | Draft the lens lists for the PR body v0 (truth, sufficiency, placement, clarity, errors, figures), each item naming the finding and the lens | `experiments/pr-description-lenses-v0.md` | |
| 8 | Update `TODOS.md` and `archive/SESSIONS.md`; stop; list what needs the user | Both files updated, no commit | End |

**Stop rules:** at the end of the block, whatever is unfinished goes into TODOS with its state. A cold agent that has not returned is reported as running; its output is not read until it returns.

**Needs the user afterwards:** whether to commit the archive records; whether the reviewer prompt is installed as an agent definition; the claimed-but-unverified findings; any edit to the PR.
