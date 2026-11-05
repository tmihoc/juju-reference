# Next session

Read `HANDOFF.md`, then `method/review-mode-contract.md`, `method/rule-derivation.md`, `method/reader-model.md` and `TODOS.md`.

**Goal:** a solid 3-epic PR (JUJU-9635, JUJU-10585, JUJU-10586) on `4.1-docs-reference-principles` (worktree `~/git/misc/juju-reference-principles`, base upstream 4.1 `52e983a435`), where every change cites a finding of the Gricean check, and the check is trustworthy enough to review and improve the PR.

**Do next, in order:**
1. Compare the blind-structure runs in `experiments/cold-run-4/` with the entity grammar. Record which sections fall out of the question list and which do not; add T11 (change streams) if the omission is confirmed.
2. Flesh out `method/reader-model.md` with the user's real readers and questions; write about eight task scenarios (SRE, charm developer, client developer) and run them as the AI-mediated task test on upstream, #23661 and the cold drafts.
3. Run the reviewer agent (`method/reviewer-agent.md`) as a subagent on upstream `status` and one clean page; install it only if it finds the known defects with few false alarms.
4. Trace the unverified findings of the cold runs against source at `52e983a435`; fix the contract gaps listed in the cold-run notes.
5. Then start the new branch's pages, one finding at a time, with the user's approval of each concrete change.

**Gates:** never touch `~/git/juju`; no edits to pages, rules, tools or figures without approval; ask before pushing to juju/juju forks; the archive repo is public, keep security-revealing material out.

**Style:** speak plainly; decide and say so; show the trace; report failures as plainly as successes; no option menus; answer the question asked before proposing more.
