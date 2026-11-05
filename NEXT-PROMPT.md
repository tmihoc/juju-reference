# Next session

Read `HANDOFF.md`, `method/settled-results.md`, `method/requirement-set.md`, `method/docs-decision-procedure.md` and `TODOS.md`, in that order.

**Goal:** a mechanism that, given a development, decides what needs documentation, where, in which category and form, and that we can use to finish JUJU-10585, JUJU-10586 and JUJU-9635. It exists as procedure v2 (untested) and a requirement set with open questions.

**Do next:** TODOS item 1 (E84). Register the cases before reading any documentation diff, run procedure v2, compare against the maintainers' edits, and revise only what the failures require.

**Hard gates:** never touch `~/git/juju`; no edits to pages, rules, tools, figures or the checker without approval; ask before every push; never push security-revealing material; do not relaunch the four 402-denied scopes; stage explicit paths only.

**Source:** `git -C ~/git/misc/juju-tutorial-diagrams show e5db99d585:<path>` (no checkout). Docs worktree: `~/git/misc/juju-tutorial-diagrams`.

**Style:** decide and say so; show the trace; report failures as plainly as successes; no option menus.
