# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written mid-session 86, 2026-10-21 (usage is at 57%: this is the safety copy). The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

---

You are continuing two linked jobs: (1) a research project on the structure of Juju reference documentation (`~/git/misc/juju-reference`), and (2) the single PR #23661 (draft, branch `4.1-docs-illustrate-docs-juju-9635`, worktree `~/git/misc/juju-tutorial-diagrams`). Code under study: `~/git/misc/juju-v2-preview` (4.1; branch `wip-entity-reference-pilots` must never be pushed). Never touch the main checkout `~/git/juju`.

## Scope decision (user, session 86)
The PR is no longer "illustrate the docs". It rewrites reference pages from the 4.1 code, and the user wants it to cover all reference docs or a substantial portion (per `page-inventory.md`), because the result feeds a lightning talk on how to identify what goes into reference docs, how to chunk it, and how to structure it. The PR title and text must say so. Be efficient: fewer distractions.

## State
- Pushed to origin: tip `1fc9f72427`. Twelve pages done: ssh-key, cloud, model, ssh-server, controller, secret-backend, machine, space, subnet, zone, credential, plus the high availability figure and the tutorial.
- Session 86 ran a Grice review of eleven pages (one agent each, no 402 this time), verified every row against the code, and fixed them in eleven commits (one per page).
- **Not done after the review:** (a) the ssh-server fix fork skipped rows 16-19, 21, 23, 26, 29 and added no agent-facing sections (`WatchSSHConnRequest`, `GetSSHConnRequest`, the `/ssh-tunnel/:tunnelID` route, `ReportKeys`): redo; (b) no rendered figure was opened after the fixes (cloud, zone, controller, credential cardinality marks; optional subnet node rename to "Provider network link"); (c) PR text of #23661 is stale (four pages listed, title wrong).
- `mm.go:179` compares a placement directive with the model UUID: probably a code bug, for the Juju developers; the machine page documents what the code does.
- Read from code, not run: space reload (a known subnet may abort the batch), model agent-stream error text, the weak spots listed in the session 85 prompt (`prompts/session-86.md`).

## New rule (user, 2026-10-21), in `page-recipe.md`
Never glue two facts with different subjects using ", and". Split them or name the relation (so, then, because, when). Name the concrete thing: no "batch", no "carry". "And" stays for same-kind items and two verbs of one subject. `tools/check_page_rules.py` now flags it, the Oxford comma, and "batch / can carry". Counts on the eleven pages before the sweep: ssh-key 9, cloud 3, model 13, ssh-server 11, controller 17, secret-backend 5, machine 24, space 9, subnet 2, zone 2, credential 6.

## Your task, in order
1. Check `git log` and the checker counts: the sweep (one fresh agent per page, rewrite flagged sentences until the checker reports zero ", and" hits, one commit per page) may be partly done.
2. Redo the ssh-server pass (above). Look at the figures once. Push (ask first; plain push).
3. Update the PR title and text (fenced block, never hard-wrapped, Jira JUJU-9635 line kept, upstream 4.1 base).
4. Next pages by schema size and inbound links: `user`, `application`, `secret`, `charm`, `storage` (needs a section split), `unit`, `relation`, `action`, `offer`, `resource`, `constraint`. Pipeline per page: draft agent, Grice review agent (prompt `experiments/e48/grice-review-prompt.md`), fix agent, one commit. Log findings per page by maxim and label for the talk.

## Standing directives (binding)
First principles; pre-register before an experiment; report fails as fails; the code is the source of truth. Readers are human and AI. Reference pages are client agnostic. No option menus when the code can decide. Ask before any push to juju (origin only). Run git network, Go, Sphinx, and shell commands with the sandbox disabled; use `python3`; check both docs builders (`dirhtml`, `latex`; builds go to a fresh `mktemp -d /tmp/...`; venv `/home/dora/git/misc/docs-venv/bin`). Every PR targets 4.1. `gh` is not installed: use `curl` for read-only checks. Read `CONTRIBUTING.md` commit rules before committing; Before/After commit bodies as in the last commits.

## End of session
Overwrite this file, copy it unchanged to `prompts/session-87.md`, append the outcome to `SESSIONS.md`, tell the user the one-line start.
