# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 92, 2026-10-21. The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

Archive convention: `prompts/session-<N>.md` holds the launch prompt of session N; this one is archived unchanged as `prompts/session-93.md`.

---

**Priority: the user's PR review comments for PR #23661, given little by little, pasted into the chat after the launch line** (they do not arrive on GitHub; the API showed 0 reviews and 0 comments at the end of session 92). Process each batch by the review pipeline: verify every comment against the 4.1 code at file:line before applying it, reject with evidence where the code disagrees, **one commit per batch** (user directive, session 91), both builders checked, ask before every push.

**Restart the live preview at session start (standing rule, session 92, also in `WORKING-RULES.md`):** `sphinx-autobuild --port 8003` from `~/git/misc/juju-tutorial-diagrams/docs` (the venv sourced; 8002 is the old pilot tree) — the server dies with its session, so start a fresh one, and verify a reference page answers 200.

**Standing naming decision (session 91): the sections are "X database schema", never "X data model"** — they are the entity's simplified database schema. Anchors are `(x-database-schema)=`, view names match, the database page's own section is "Database schema" (no doubled word).

**Standing density decision (session 92): no table names in entity-page prose.** The record-to-table closing paragraphs are gone from all 33 entity pages (`8c034d49ed`, pushed): the surface test and the three dispositions (hide, contain, relocate) are in `page-recipe.md`; the two rules the paragraphs carried live in their record bullets (the offer description fallback: `COALESCE(o.description, cm.description)`, `0032-offer.sql`; the charm insert-delete-only rule: `model.go:222-234`, the 13 guarded charm tables); `database.md` keeps its own mapping (its subject is the storage layer); the dropped paragraphs are archived verbatim in `work/table-mapping-paragraphs.md` (extracted from `a0ff626ad789`); the mapping's home is `juju-db-repl` until the generated tables-by-topic page lands (TODOS item 000000). The zero-surface density audit runs in that stream; `secret.md`'s "four more tables" paragraph is its first candidate.

## State (end of session 92)
- **Branch `4.1-docs-illustrate-docs-juju-9635` pushed at `8c034d49ed`, even with origin; PR #23661 open on juju/juju (base 4.1 at `e5db99d585`), head matches (`8c034d49eda`).** All 35 table pages written, reviewed, fixed, pushed. No review batch arrived this session (GitHub stayed 0 reviews / 0 comments); the session ran the density decision instead.
- Error counts stand at **956 entries / 674 distinct messages / 229 operations (182 carry errors) on 33 pages** — unchanged by the drop, verified; verify any count claim with `tools/count_errors.py <worktree> [--rows]` before publishing. The anchor tree is `/tmp/juju-41-tree` at `e5db99d585` (recreate: `git -C ~/git/misc/juju-v2-preview worktree add /tmp/juju-41-tree e5db99d585`); re-check claims there, not in the preview tree.
- The checker's findings (unit.md, user.md, charm.md, cloud.md bullet-intros; the gerund-nominal and title-map gaps) are the pre-existing false positives, unchanged page-for-page across the drop (user.md lost one ", and" false positive with its paragraph).
- Open: the GitHub PR body is one refresh behind (the user pastes the fenced blocks from `pr-description.md`; headline 956/674); recording `error-contract-epic.md` in Jira is the user's move (number TBD); the CI-lint stream is the epic's first work after that.

## Efficiency notes (keep applying them)
1. **Launch agents in waves of 2–3, never more.** OpenRouter pre-reserves the worst-case cost of every in-flight agent request; 4+ concurrent, and even a single new request late in a session, bounce with 402 "can only afford ~2200 tokens".
2. **Wake a parked agent, don't relaunch it.** An agent that died on a 402 keeps its research in `history://<id>`; `write agent://<id>` resumes it. Two 402s → run that slice in-session and say so in the commit.
3. **Put a research budget in every draft prompt** ("wrap up and write the page by about 150 tool calls"); keep reviews read-only; reviews and fixes are separate agents.
4. **Absolute paths in every file tool.** The shell cwd is `~/git/juju`, the main checkout that must never be touched.
5. **Fix agents verify each review row against the code before applying it.** Rejects need evidence.
6. **Overlap phases:** interim `dirhtml` build as soon as pages land; reviews of landed pages while the next drafts still run.
7. **The `todo` tool:** `op:done` with a single `task` string marks that item; `op:done` with an `items` list marks EVERY listed item and once wiped the whole list. Never pass `items` to `done`.
8. **The `edit` tool's line numbers go stale after every write**; re-read before each edit, prefer a full-block `PUT` over a narrow line range, re-run the checker before every commit. Commit bodies through a heredoc file (`git commit -F`), never inline `-m`.
9. **Don't over-collect (user feedback, session 91).** Scope greps to the live tree plus the governing method files; the archives (`experiments/`, old session logs, pilot trees) are noise. State decisions as decisions, questions as questions, and put a scope statement or a tool-call budget in the prompt when a task is broad.

## The pipeline (unchanged except the commit rule)
1. Draft agents, one per page, 2–3 at once, budget line included: read `page-recipe.md`, the exemplars (`credential.md`, `secret.md`, `relation.md`), the old page if any, and `experiments/e48/grice-review-prompt.md`; rewrite one `.md` only; figure fragments to `/tmp/ggarch-fragments/<page>.ggarch`; run the checker; no commit, no build.
2. **You merge:** append fragments to `docs/juju.ggarch`, add how-to anchors, run `ggarch check`, check every merged figure block for single-colon options and an intact fence, build both builders into fresh `mktemp -d` directories, **one commit per batch of pages** (signed; Before/After body; read `CONTRIBUTING.md` first), figure sources in a commit before the pages.
3. Review agents (read-only, the Grice prompt), then fix agents that verify each row first.
4. Ask before every push (origin only, plain push).

## Standing directives (binding)
First principles; the code is the source of truth; report fails as fails; pre-register before an experiment. Readers are human and AI. Reference pages are client agnostic. Decide and edit: no option menus, no verdict-asking. Ask before any push (origin only). Run git network, Go, Sphinx, and shell commands with the sandbox disabled; use `python3`. Check both docs builders. Every PR targets 4.1; branch starts `4.1-`. `gh` is not installed: use `curl` for read-only checks. PR text in fenced blocks, never hard-wrapped, Jira JUJU-9635 line kept. The user's usage meter matters: use fresh narrow agents for sweeps and reviews, keep this context small, and write state to disk early. Restart the live preview at session start (session 92; `WORKING-RULES.md` has the command).

## End of session
Overwrite this file, copy it unchanged to the next `prompts/session-<N+1>.md`, append the outcome to `SESSIONS.md`, update the block in `HANDOFF.md`, tell the user the one-line start.