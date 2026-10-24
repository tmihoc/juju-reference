# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 102, 2026-10-24 (attended; the session that shipped the CI-lint stream, finished the sweep, and moved the whole working archive off the old machine). The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

Archive convention: `prompts/session-<N>.md` holds the launch prompt of session N; this one is archived unchanged as `prompts/session-103.md`. **The whole archive is now a public repo: https://github.com/tmihoc/juju-reference — commit and push the session records at every close-out.**

## New machine setup (first session on the machine only)

The session records reference these paths; recreate them before the ritual:
- Clone the archive: `git clone https://github.com/tmihoc/juju-reference ~/git/misc/juju-reference`.
- Clone the fork and add the docs worktree: `git clone git@github.com:tmihoc/juju.git ~/git/juju`, then `git -C ~/git/juju worktree add ~/git/misc/juju-tutorial-diagrams -b 4.1-docs-illustrate-docs-juju-9635 origin/4.1-docs-illustrate-docs-juju-9635`.
- The 4.1 anchor tree: `git -C ~/git/juju worktree add /tmp/juju-41-tree e5db99d585`.
- The docs venv: `python3 -m venv ~/git/misc/docs-venv && ~/git/misc/docs-venv/bin/pip install -r ~/git/misc/juju-tutorial-diagrams/docs/requirements.txt`.
- Git identity and commit signing as configured on the old machine (`commit.gpgsign true`); `gh` is not installed: read-only GitHub checks go through `curl` on api.github.com.

**Session 103 state:** branch `4.1-docs-illustrate-docs-juju-9635` even with origin at `a0f17f6c8e`; PR #23661 open (base `e5db99d585`); counts 956/674/204/182; all 35 entity pages swept; the error-contract CI check is part of the PR.

**The queue, in order:**
1. **The PR body paste** (the user pastes the fenced blocks from `pr-description.md` — refreshed to sessions 86-102, with the CI check and the second linking sweep in the bullets; totals 956/674/204/182).
2. **The ggarch stream:** the session-83 queue items 1-4 (caption inline-code rendering, caption roles and `{ref}` links, node/edge-label hyperlinks, the modal slideshow keeping prev/next/counter/arrow keys) — await the user's pick; do not start unbidden. The live queue is in the ggarch repo's `TODOS.md` (untracked there by convention; a dated snapshot lives in `work/ggarch-state/`).
3. **The recorded duplicate-fact restructure candidates** (session-102 sweep, in `work/duplicate-facts-99.md`): the migration record set, the constraint merge rules, the change-block glosses — page restructuring, needs the user's review before anything moves.
4. **The checker's 19 reasoned exclusions** (`docs/scripts/check_error_contract.py`): most are pages that drop the `juju/errors` constructor's rendered suffix (`... bad request`, `... not yet available`) — candidate docs fixes; triage with the user; fixing them shrinks the list.
5. Review batches pipeline unchanged (a pasted batch preempts whatever runs); fix 15 still blocked on the ggarch router work.

**Ritual at session start (standing rule, session 92, also in `WORKING-RULES.md`):** restart the live preview (the previous session kills its server at close-out): `cd ~/git/misc/juju-tutorial-diagrams/docs && source ~/git/misc/docs-venv/bin/activate && sphinx-autobuild --port 8003 --host 127.0.0.1 . _build -c . -d .sphinx/.doctrees -b dirhtml -j auto -D llms_txt_enabled=0 --ignore '_build/*' --ignore '.sphinx/*'` (8002 is the old pilot tree; if 8003 is busy, kill the previous server by pid and start fresh). Give the long-running call a service `name` so its `ready` block is honored (service-mode takes `ready.timeout`, not `timeout`/`async`); the ready-grep `[Bb]uild (succeeded|finished)` matches this sphinx-autobuild (the harness rejects `(?i)` — use a plain character class). Verify a reference page answers 200. Verify state: counts **956/674/204/182** (`python3 ~/git/misc/juju-reference/tools/count_errors.py ~/git/misc/juju-tutorial-diagrams`), branch even with origin at `a0f17f6c8e`, PR #23661 open (base `e5db99d585`; `gh` is not installed: use `curl` on api.github.com).

**The user's PR review comments for PR #23661 arrive only when pasted into the chat (they do not arrive on GitHub), and the user adds to the queue whenever they think of something — no standing review priority (user, close of session 99).** When a batch is pasted, verify every comment against the 4.1 code at file:line in `/tmp/juju-41-tree` (at `e5db99d585`; recreate with `git worktree add /tmp/juju-41-tree e5db99d585`, `git worktree prune` first if it is a missing registration) before applying, reject with evidence where the code disagrees, **one commit per batch** (user directive, session 91), checker + `tools/count_errors.py` (must stay **956/674/204/182**) + both builders before every commit. A pasted batch preempts whatever is running. **Pushes pre-authorized when the plan was clear (sessions 97-102); ask only when a decision was contested or open.**

**Standing decisions (binding):** the sections are "X database schema", never "X data model" (91); no table names in entity-page prose (92; the surface test and the three dispositions hide, contain, relocate are in `page-recipe.md`); "operation" is the domain word only, one documented API interaction is a "call" (93, applied 94); no version phrases (93; the 3.6-to-4.1 upgrade how-to excepted); the access bullet is `Caller:` and levels attach to users, never clients (93, applied 94); the page filename matches its title (94); the paradigm decides the set (94); "hook tools" are "hook commands" and every specific name hyperlinks to its documenting section (95); each schema figure hosts its own `###` section, figure first (95); a call is a `###` under a `## ... calls` section only — counts 956/674/204/182, never re-widen without the user (95); the figure caption carries the takeaway, the alt text carries the inventory (99, in `page-recipe.md` §2). All in `page-recipe.md` except where noted.

**Efficiency notes (keep applying them)**
1. **Launch agents in waves of 2-3, never more.** The model-provider key pre-reserves the worst-case cost of every in-flight agent request; 4+ concurrent bounce with 402.
2. **Wake a parked agent, don't relaunch it.** An agent that died on a 402 keeps its research in `history://<id>`; `write agent://<id>` resumes it. Two 402s → run that slice in-session and say so in the commit.
3. **Put a research budget in every draft prompt** ("wrap up and write the page by about 150 tool calls"); keep reviews read-only (`agent: "scout"`); reviews and fixes are separate agents.
4. **Absolute paths in every file tool.** The edit tool resolves relative paths against the shell cwd.
5. **Fix agents verify each review row against the code before applying it.** Rejects need evidence; re-verify every subagent table against the code before it lands in a page.
6. **Overlap phases:** interim builds as soon as pages land; reviews of landed pages while the next drafts still run.
7. **The `todo` tool:** `op:done` with a single `task` string marks that item; never pass `items` to `done`. The list is disposable: rebuild with `op:init`, clear with `op:drop`, carry the state in the reply prose.
8. **The `edit` tool's line numbers go stale after every write** — re-read before each edit, prefer whole-block `PUT`; body rows are verbatim insertions, so never include unchanged boundary lines in the body. Commit bodies through a heredoc file (`git commit -F`), never inline `-m`.
9. **Don't over-collect.** Scope greps to the live tree plus the governing method files; the archives are noise. State decisions as decisions, questions as questions, and put a scope statement or a tool-call budget in every broad prompt.
10. **`git add -A` sweeps the worktree:** stage named paths, or check `git status --short` against the commit's intent before committing.
11. **Latex WARNING counts: grep `WARNING:` case-sensitively** — the config dump's `suppress_warnings` inflates a case-insensitive count.
12. **A tool-call budget on exploratory fixes:** pre-register the rule — which variant wins, what gets kept, when to stop — and follow it.
13. **Checker comparisons via `git show HEAD:` temp copies: no digits in the temp filenames; compare full outputs, never tails.**
14. **Read the diff before every commit.**
15. **Type the path string explicitly in every `grep`/`glob` call** — a missing `path` silently searches the workspace root. `todo` `done` needs the exact verbatim task string. When a search misfires, fall back to a targeted `ls` or a direct `read`.

**The pipeline (review batches)**
1. The user pastes a batch; verify every row against the 4.1 code at file:line in `/tmp/juju-41-tree` before applying; rejects need evidence.
2. **You merge and commit:** checker on every touched page, `tools/count_errors.py` unchanged at **956/674/204/182**, both builders into fresh `mktemp -d` dirs, **one commit per batch** (signed, body via `git commit -F`, read `CONTRIBUTING.md` first), figure sources in a commit before the pages.
3. Reviews of landed pages (when asked) are read-only agents; fix agents verify each row first; all new and edited text uses "call", the `Caller:` line, user-attributed levels, "hook command" with linked names.
4. Pushes pre-authorized when the plan was clear; ask when a decision was contested or is open.

**Standing directives (binding)**
First principles; the code is the source of truth; report fails as fails; pre-register before an experiment. Readers are human and AI. Reference pages are client agnostic. Decide and edit: no option menus, no verdict-asking. Analyze till the answer falls out, within reason — no rabbit holes. Don't ask for verdicts: investigate till the right answer falls out, then propose the plan, execute and report. Ask before any push that a clear plan does not cover (origin only). Run git network, Go, Sphinx, and shell commands with the sandbox disabled; use `python3`. Check both docs builders. Every PR targets 4.1; branch starts `4.1-`. `gh` is not installed: use `curl` for read-only checks. PR text in fenced blocks, never hard-wrapped. The user's usage meter matters: use fresh narrow agents for sweeps and reviews, keep this context small, and write state to disk early. Restart the live preview at session start; kill it at close-out (session 92 rule, `WORKING-RULES.md` has the command).

## End of session
Overwrite this file, copy it unchanged to the next `prompts/session-<N+1>.md`, append the outcome to SESSIONS.md, update the block in HANDOFF.md, **commit and push the archive repo (https://github.com/tmihoc/juju-reference)**, tell the user the one-line start.