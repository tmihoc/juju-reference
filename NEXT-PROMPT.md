# Next session

Read `HANDOFF.md` first: its state, style, gates and open decisions apply throughout. Then read `method/review-mode-contract.md`, `method/rule-derivation.md`, `method/reader-model.md` and `TODOS.md`.

**Goal:** a solid 3-epic PR (JUJU-9635, JUJU-10585, JUJU-10586) on `4.1-docs-reference-principles` (worktree `~/git/misc/juju-reference-principles`, base upstream 4.1 `52e983a435`), where every change cites a finding of the Gricean check, and the check is trustworthy enough to review and improve the PR.

**Do next, in order:**
1. Done: the blind-structure comparison (`experiments/cold-run-4/compare-structure.md`). Remaining from it: decide how to justify the entity grammar (change coupling and set-wide uniformity, not the questions alone), and add to the question list the two questions the runs missed (how a client or agent learns that something changed; who may do it and what the refusal says).
2. Start here: flesh out `method/reader-model.md` with the user's real readers and questions; write about eight task scenarios (SRE, charm developer, client developer) and run them as the AI-mediated task test on upstream, #23661 and the cold drafts.
3. Run the reviewer agent (`method/reviewer-agent.md`) as a subagent on upstream `status` and one clean page; install it only if it finds the known defects with few false alarms.
4. Trace the unverified findings of the cold runs against source at `52e983a435`; fix the contract gaps listed in the cold-run notes.
5. Then start the new branch's pages, one finding at a time, with the user's approval of each concrete change.
