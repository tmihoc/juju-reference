# Next session

Read `HANDOFF.md`, `method/settled-results.md`, `method/requirement-set.md`, `method/docs-decision-procedure.md` and `TODOS.md`, in that order.

**Goal:** a mechanism that, given a development, decides what needs documentation, where, in which category and form, and that we can use to finish JUJU-10585, JUJU-10586 and JUJU-9635. It exists as procedure v2 (untested) and a requirement set with open questions.

**Do next:** TODOS item 1, the audit of the PR **against its base** in refactor mode (the PR also refactored heavily: check what was removed and moved as well as what was added). Start with the pages that lost the most lines. Report keep, trim, move or restore per page, with evidence, and the fixes needed. Revise the procedure only where the audit shows it failing. Do not start a separate method-validation study.

**Hard gates:** never touch `~/git/juju`; no edits to pages, rules, tools, figures or the checker without approval; ask before every push; never push security-revealing material; do not relaunch the four 402-denied scopes; stage explicit paths only.

**Source:** `git -C ~/git/misc/juju-tutorial-diagrams show e5db99d585:<path>` (no checkout). Docs worktree: `~/git/misc/juju-tutorial-diagrams`.

**Style:** decide and say so; show the trace; report failures as plainly as successes; no option menus.

**The user's direction (2026-11-05):** the repo is disposable; what matters is a solid 3-epic PR (JUJU-9635, JUJU-10585, JUJU-10586) and, longer term, a Gricean guide and check for the docs as a whole that an AI can use to decide what to document and how. Do not build more method than the PR needs. The mechanism (`method/`) earns its place by auditing the PR and by deciding cases like SSH. Reach clear conclusions; show the trace; say what is unresolved and what would resolve it.

**State at hand-off:** the audit pilot on the deleted `reference/metadata.md` found a candidate regression (the simplestreams data layout, product IDs and directory tree, is nowhere in the PR's docs; the old text is partly out of date, so restore it corrected). The SSH decision keeps `reference/ssh-server.md` and drops the maintainers' explanation page. Two real defects are in `epics/source-questions.md`: the upgrade-guide backup statement and the missing `#action-task-status` anchor. The repo is pushed through the squash commit; later commits are local.
