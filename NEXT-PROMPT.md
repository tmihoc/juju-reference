# Next session

Read `HANDOFF.md`, `method/settled-results.md`, `method/requirement-set.md`, `method/docs-decision-procedure.md` and `TODOS.md`, in that order.

**Goal:** a mechanism that, given a development, decides what needs documentation, where, in which category and form, and that we can use to finish JUJU-10585, JUJU-10586 and JUJU-9635. It exists as procedure v2 (untested) and a requirement set with open questions.

**Do next:** TODOS item 1, the audit of the PR's additions with procedure v2 (necessity, ownership, source check of every claim). Report keep, trim or move per page and the fixes needed. Revise the procedure only where the audit shows it failing. Do not start a separate method-validation study.

**Hard gates:** never touch `~/git/juju`; no edits to pages, rules, tools, figures or the checker without approval; ask before every push; never push security-revealing material; do not relaunch the four 402-denied scopes; stage explicit paths only.

**Source:** `git -C ~/git/misc/juju-tutorial-diagrams show e5db99d585:<path>` (no checkout). Docs worktree: `~/git/misc/juju-tutorial-diagrams`.

**Style:** decide and say so; show the trace; report failures as plainly as successes; no option menus.
