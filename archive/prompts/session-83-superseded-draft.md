# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 82, 2026-10-20. The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

---

You are continuing a research project on the structure of Juju reference documentation. Epic JUJU-9635 (diagrams) was built in session 82 and awaits the user's decision on pushing. Read `HANDOFF.md` ("State at the end of session 82"), `TODOS.md` items 000 and 0, the plan's "E45 results (session 82)", `WORKING-RULES.md` and `memory-export/MEMORY.md`. Standing directives are in `HANDOFF.md` ("Session discipline") and in the session 82 prompt (`prompts/session-82.md`): first principles, pre-register before running, report fails as fails, code is the source of truth, no option menus, ask before any push (origin only), run git network, Go, Sphinx and shell commands with the sandbox disabled, check both docs builders.

## Your task
1. Ask the user whether to push the epic branch and in which split (TODOS item 000). Do not push without the answer. If the user wants changes, the worktree is `~/git/misc/juju-diagrams` (branch `4.1-docs-illustrate-docs-juju-9635`; old figure removals are staged, nothing committed). Commit with review fixes separate.
2. Close the open E45 items in order: derive kind O from the call graph (pre-register first; `experiments/e30`, `e37`), the `cloud` ERD, the cross-model topology, a hook-order figure. Re-run `experiments/e45/rank.py` after fixing the page-to-domain mapping.
3. E44 follow-ups (TODOS item 0): coverage sweep, structure-free control, ledger and skeleton updates.

## Known weak spots, do not hide them
- E44: the pattern is not shown to help AI readers; judges and readers are the same model family as the author.
- E45 thresholds (4 to 12 tables, 3 actors) are untested; kind O was not derived; epic acceptance 4 (user feedback) is open.
- Some ERD captions and the migration caption were written from code reads, not reviewed by a second reader.

## End of session
1. Write the next launch prompt to `NEXT-PROMPT.md` (overwrite) and copy it unchanged to `prompts/session-<N>.md`, where N is the session it launches. Never edit an archived prompt.
2. Append the outcome to `SESSIONS.md` with a one-line pointer to the prompt file that launched this session.
3. Tell the user the one-line start.
