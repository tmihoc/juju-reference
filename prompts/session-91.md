# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 90, 2026-10-21. The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

Archive convention: `prompts/session-<N>.md` holds the launch prompt of session N; this one is archived unchanged as `prompts/session-91.md`.

---

**Priority (user, 2026-10-21, late session 89): error counting is anchored to the upstream 4.1 tree, never to the docs' own iteration.** The count (956 entries / 674 distinct messages, 182 of the 229 operations on 33 pages) is of errors the 4.1 code raises, each cited to a file:line in the 4.1 source; the PR text and `error-contract-epic.md` say so. The counting method is now a tool: `tools/count_errors.py <worktree> [--rows]` reproduces session 89's method exactly (it yields 950/670 at the tip `e4eb027c82` and 956/674 at HEAD; run it after any error-list edit). The preview tree (`~/git/misc/juju-v2-preview`) is 3 commits behind `upstream/4.1` (the LXD-profile removal); a worktree of the anchored 4.1 tree (`e5db99d585`) is at `/tmp/juju-41-tree` (recreate with `git -C ~/git/misc/juju-v2-preview worktree add /tmp/juju-41-tree e5db99d585`). Live upstream has advanced past the anchor (`a8591fe1b8`); the anchor is the tree the citations point into. Re-check any future claim against `/tmp/juju-41-tree`, not the preview tree.

## State (end of session 90, final)
- **Branch `4.1-docs-illustrate-docs-juju-9635` (worktree `~/git/misc/juju-tutorial-diagrams`) is even with origin at `4b898b1f24`**; PR #23661 open on juju/juju (base 4.1), head matches. The "three unpushed commits" of the session-89 state were pushed at 14:42 on 2026-10-21, after the state file was written — nothing was left to push.
- **First work: the user's PR review comments** (they arrive with the chat, pasted after the launch line). Process by the review pipeline: verify each comment against the code at file:line before applying, reject with evidence where the code disagrees, one commit per page, both builders checked, ask before push.
- All 34 entity pages (+ high-availability = 35 table rows) are written, reviewed, fixed, pushed. No repo changes this session; the fixes were to the research repo's paste source and records.
- **The PR body on GitHub is one refresh behind** (session-88 numbers: 792/751, "rejected two", agent-version 5, image-metadata 2, model-defaults 0): the user pastes the fenced blocks from the updated `pr-description.md` (headline 956/674 with "182 of the 229 operations on 33 pages"; pages table columns "Figures added or updated" / "Errors documented", full per-page error-entry counts that sum to 956, and a Total row: 49 figures, 956 entries, 674 distinct messages).
- `error-contract-epic.md` updated to 956/674; it still needs recording in Jira (number TBD) — the user's move; the CI-lint stream is the epic's first work after that.
- `tools/count_errors.py` added; verify any count claim with it before publishing.

## Efficiency notes (keep applying them)
1. **Launch agents in waves of 2–3, never more.** OpenRouter pre-reserves the worst-case cost of every in-flight agent request; 4+ concurrent, and even a single new request late in a session, bounce with 402 "can only afford ~2200 tokens".
2. **Wake a parked agent, don't relaunch it.** An agent that died on a 402 keeps its research in `history://<id>`; `write agent://<id>` resumes it with the full context. If it 402s twice, run that slice in-session and say so in the commit.
3. **Put a research budget in every draft prompt** ("wrap up and write the page by about 150 tool calls") and keep reviews read-only — reviews and fixes are separate agents, except when a 402 forces the review in-session.
4. **Absolute paths in every file tool.** The shell cwd is `~/git/juju`, the main checkout that must never be touched.
5. **Fix agents verify each review row against the code before applying it.** Rejects need evidence.
6. **Overlap phases:** run an interim `dirhtml` build as soon as pages land, and run reviews for landed pages while the next drafts still run.
7. **The `todo` tool:** `op:done` with a single `task` string marks that item; `op:done` with an `items` list marks EVERY listed item and once wiped the whole list. Never pass `items` to `done`.
8. **The `edit` tool's line numbers go stale after every write**; re-read before each edit, prefer a full-block `PUT` over a narrow line range, and re-run the checker before every commit. Write commit bodies through a heredoc file (`git commit -F`), never inline `-m` with backticks or quotes in the text.

## The pipeline (unchanged)
1. Draft agents, one per page, 2–3 at once, budget line included: read `page-recipe.md`, the exemplars (`credential.md`, `secret.md`, `relation.md`), the old page if any, and `experiments/e48/grice-review-prompt.md`; rewrite one `.md` only; figure fragments to `/tmp/ggarch-fragments/<page>.ggarch`; run the checker; no commit, no build.
2. **You merge:** append fragments to `docs/juju.ggarch`, add how-to anchors, run `ggarch check`, check every merged figure block for single-colon options and an intact fence, build both builders into fresh `mktemp -d` directories, commit one page per commit (signed; Before/After body; read `CONTRIBUTING.md` first), figure sources in a commit before the pages.
3. Review agents (read-only, the Grice prompt), then fix agents that verify each row first.
4. Ask before every push (origin only, plain push).

## Standing directives (binding)
First principles; the code is the source of truth; report fails as fails; pre-register before an experiment. Readers are human and AI. Reference pages are client agnostic. Decide and edit: no option menus, no verdict-asking. Ask before any push (origin only). Run git network, Go, Sphinx, and shell commands with the sandbox disabled; use `python3`. Check both docs builders. Every PR targets 4.1; branch starts `4.1-`. `gh` is not installed: use `curl` for read-only checks. PR text in fenced blocks, never hard-wrapped, Jira JUJU-9635 line kept. The user's usage meter matters: use fresh narrow agents for sweeps and reviews, keep this context small, and write state to disk early.

## End of session
Overwrite this file, copy it unchanged to the next `prompts/session-<N+1>.md`, append the outcome to `SESSIONS.md`, update the block in `HANDOFF.md`, tell the user the one-line start.
