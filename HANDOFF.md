# Handoff (rewritten 2026-11-05; the previous 767-line handoff is `archive/HANDOFF-session-129.md`)

## What this is

The working archive behind juju/juju PR #23661 (epic JUJU-9635 figures, JUJU-10585 reference, JUJU-10586 error contract). The pages themselves live in the PR worktree `~/git/misc/juju-tutorial-diagrams`. This directory holds the method, the evidence, and the queue.

## Read in this order

1. `method/settled-results.md`: what 130 sessions established, what failed, what is open.
2. `method/requirement-set.md`: the 27 requirements (what `docs/` holds, categories, chunking, ownership, page form, errors and figures, necessity), each with grounds and status, and open questions Q1 to Q8.
3. `method/docs-decision-procedure.md` (v2): the steps that turn a development into a documentation change set.
4. `TODOS.md`: the queue, by epic.
5. `method/page-recipe.md` and `method/WORKING-RULES.md` when writing or checking a page.

Evidence for the mechanism: `method/evidence/e83-predictions.md`, `method/evidence/e83-results.md` (procedure v1 against six real developments) and `method/evidence/ssh-documentation-decision.md` (a worked decision). Defects and leads: `epics/source-questions.md`. Everything older is in `archive/`, which mirrors the old paths.

## State (observed 2026-11-05; recheck before relying)

- Docs worktree `~/git/misc/juju-tutorial-diagrams` at `48ef1fca17`, base `e5db99d585` (the 4.1 source anchor). PR #23661 was open as a draft.
- Counts from `python3 tools/count_errors.py ~/git/misc/juju-tutorial-diagrams`: 960 entries, 674 distinct messages, 204 calls, 182 with entries. Do not widen the counted set.
- The source anchor `/tmp/juju-41-tree` no longer exists. Read source with `git -C ~/git/misc/juju-tutorial-diagrams show e5db99d585:<path>` and `git grep ... e5db99d585 -- <path>`, which need no checkout.
- The mechanism: procedure v1 tested (E83), v2 untested, one worked decision (SSH). Not yet a validated method.
- Four research scopes were denied with HTTP 402: `WorkloadModel`, `HookCommandPages`, `KubernetesCloudAttributes`, `CrayonEvaluation`. Do not relaunch or work around them; ask the user.
- Jira acceptance text for the epics is unavailable; reconcile it before declaring completion.

## Gates (standing)

- Never read, edit or run anything in `~/git/juju` (the main checkout).
- No change to pages, the skeleton, rules, tools, figures or the checker without the user's approval of the concrete change.
- Ask before every push, and push to origin only. Never push security-revealing material.
- The user pastes the PR body. Pre-existing uncommitted changes are the user's: stage explicit paths only.
- Register a test before running it only when its result will decide a rule; otherwise log it. Keep failures and counterexamples.

## Close-out

Update this file and `TODOS.md`, add a short entry to `archive/SESSIONS.md`, commit only that session's files locally, stop any preview server. Do not push.
