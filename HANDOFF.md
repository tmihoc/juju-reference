# Handoff (rewritten 2026-11-05, session 131; the previous one is `archive/HANDOFF-session-129.md`)

## What this is

The working archive behind juju/juju PR #23661 (JUJU-9635 figures, JUJU-10585 reference, JUJU-10586 error contract). #23661 is an open draft from `~/git/misc/juju-tutorial-diagrams` (branch `4.1-docs-illustrate-docs-juju-9635`, base `e5db99d585`) and stays the reference candidate. The **new PR** is built on `4.1-docs-reference-principles` in `~/git/misc/juju-reference-principles`, based on upstream 4.1 `52e983a435` (2026-11-05), with no commits yet. This directory holds the method, the evidence and the queue.

## Goal

A solid 3-epic PR whose every change cites a finding from a Gricean check, and a check that can say why a statement in upstream is wrong (false, stale, not enough, excess, misplaced, unclear) the way a competent reviewer would. The check is judged by running it cold from upstream and comparing the result with upstream and with #23661, never with "matches #23661".

## Read in this order

1. `method/review-mode-contract.md`: findings, defect types (statements, boundaries, errors, figures), addressee model, scoring sheet.
2. `method/rule-derivation.md`: each writing rule derived from a maxim and a reader premise, or marked conventional.
3. `method/reader-model.md`: the readers (draft; needs the user's real questions).
4. `method/reviewer-agent.md`: design of a pre-review agent (not installed, not yet run).
5. `method/docs-decision-procedure.md`, `method/requirement-set.md`, `method/settled-results.md`: the older method. `method/page-recipe.md`: the entity page form.
6. `experiments/` (cold runs 1 to 4, comparison, placement determinacy, PLAN, lens lists) and `method/evidence/audit-pr23661.md`, `review-mode-trial-1.md`.
7. `TODOS.md`.

## State (2026-11-05)

- The audit of #23661 found real losses and right removals, and two of its restore proposals were corrected by cold runs (`constraint` min and max; `relation` controller-external flags): restoring the old text would add errors.
- Cold runs from upstream: `status` twice (about 80% agreement on substantive findings; one draft misstated a rule its trace cited correctly), `constraint` and `relation` at `52e983a435`. Three findings per page were verified by the parent; the rest are claims.
- Placement: the entity grammar decided about half to three quarters of the facts on `relation` and few on `status` and `constraint`. Because the agents were given the grammar, this is not independent convergence.
- Blind-structure runs (cold run 4: `relation-blind`, `status-blind`) withhold the grammar. See `experiments/cold-run-4/`; check whether they finished, then compare their section lists with the entity grammar. They finished; see `experiments/cold-run-4/compare-structure.md`.
- The question list has no question that yields `X change streams` (25 PR pages have that section); proposed T11 "how does a client or agent learn that it changed, and what does it receive?" Not yet added.
- Source check: the traced status and secret files have no diff between `e5db99d585` and `52e983a435`.
- Public record: the archive repo `tmihoc/juju-reference` is public. One source observation about validation in the constraint path was withheld from it; report it to the maintainers.

## Gates (standing)

- Never read, edit or run anything in `~/git/juju` (the main checkout). Git ran from the docs worktree only.
- No change to pages, rules, tools, figures or the checker without the user's approval of the concrete change.
- The user may commit and push archive records, but nothing security-revealing goes into the public repo. Ask before pushing anything to juju/juju forks; never push to upstream.
- Cold agents write only under `experiments/`; they cannot write a file named findings; record those from their report.
- Do not relaunch the four 402-denied scopes (`WorkloadModel`, `HookCommandPages`, `KubernetesCloudAttributes`, `CrayonEvaluation`).

## Scratch worktree and preview servers

`~/git/misc/preview-status` is a detached scratch worktree at `52e983a435` with `reference/status.md` replaced by cold run 1's draft (uncommitted). Remove it with `git worktree remove --force ~/git/misc/preview-status` from the docs worktree when done. Server on 8001 serves it if still running.

Two `sphinx-autobuild` servers were run at close-out: 8001 (new branch, upstream as is) and 8002 (#23661). Stop them if still running: `pkill -f sphinx-autobuild`.

## Close-out

Update this file and `TODOS.md`, add an entry to `archive/SESSIONS.md`, commit that session's files, stop the servers.
