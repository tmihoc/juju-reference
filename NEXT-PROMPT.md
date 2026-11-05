# Next session

**Start here:** item 2 below (item 1 is done). The user's one-line prompt is only "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and follow it." Everything else the user used to type is in this file: follow the Gates and Style sections as standing instructions.

Read `HANDOFF.md`, then `method/review-mode-contract.md`, `method/rule-derivation.md`, `method/reader-model.md` and `TODOS.md`.

**Goal:** a solid 3-epic PR (JUJU-9635, JUJU-10585, JUJU-10586) on `4.1-docs-reference-principles` (worktree `~/git/misc/juju-reference-principles`, base upstream 4.1 `52e983a435`), where every change cites a finding of the Gricean check, and the check is trustworthy enough to review and improve the PR.

**Do next, in order:**
1. (Done, see `experiments/cold-run-4/compare-structure.md`.) With the grammar withheld, the questions and maxims gave kinds, rules, identity, status and settings sections for `relation`, and none of the grammar's section names. Next: decide how to justify the grammar (change coupling and set-wide uniformity, not the questions alone), and add two questions to the list that the runs missed: how a client or agent learns that something changed (change streams), and who may do it and what the refusal says.
2. Flesh out `method/reader-model.md` with the user's real readers and questions; write about eight task scenarios (SRE, charm developer, client developer) and run them as the AI-mediated task test on upstream, #23661 and the cold drafts.
3. Run the reviewer agent (`method/reviewer-agent.md`) as a subagent on upstream `status` and one clean page; install it only if it finds the known defects with few false alarms.
4. Trace the unverified findings of the cold runs against source at `52e983a435`; fix the contract gaps listed in the cold-run notes.
5. Then start the new branch's pages, one finding at a time, with the user's approval of each concrete change.

**Open decision for the user:** the blind relation run's access-related observation was pushed to the public archive repo in commit `b83c57c` and replaced by a placeholder in `8019bc3`; the original stays in history unless the user approves a history rewrite and force-push. Also to report to the maintainers (draft the notes, do not post): that observation, and the constraint-validation one withheld earlier.

**Gates:** never read, edit or run anything in `~/git/juju`; no edits to pages, rules, tools or figures without the user's approval of the concrete change; ask before pushing to juju/juju forks (the archive repo may be committed and pushed, but it is public: screen every agent's output for security-revealing material before committing, and keep such material out); stage explicit paths only.

**Style:** the user asked for plain speech: answer the question asked before proposing more, and do not leave the user to ask what a request means; speak plainly; decide and say so; show the trace; report failures as plainly as successes; no option menus; answer the question asked before proposing more.
