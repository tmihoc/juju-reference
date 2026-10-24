# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 83, 2026-10-20. The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

---

You are continuing two linked jobs: (1) a research project on the structure of Juju reference documentation (`~/git/misc/juju-reference`), and (2) **epic JUJU-9635, illustrate the docs, due 2026-10-21, to be delivered as ONE PR**. Code under study: `~/git/misc/juju-v2-preview` (4.1; branch `wip-entity-reference-pilots` must never be pushed). Never touch the main checkout `~/git/juju`.

## Read first, in this order
1. `HANDOFF.md`, the block "State at the end of session 83 (final)".
2. `page-recipe.md` (the procedure and every page rule, now including the session 83 rules below) and the end of `skeleton-v6.md`.
3. `TODOS.md` (the first items of the live queue are the skeleton cracks, the SSH server plan, and the ggarch notes), `pr-epic-notes.md` (what the PR description must say; the model page section is new), `WORKING-RULES.md`, `memory-export/MEMORY.md`.

## State of the epic PR
- Branch `4.1-docs-illustrate-docs-juju-9635`, worktree `~/git/misc/juju-tutorial-diagrams`, off `upstream/4.1` at `e5db99d585`. **Nothing is pushed.** Commits: tutorial diagrams (`44c29b27fd`), SSH key page (`338dac9413`), cloud page (`eb4fcc87a0`), about ten `fixup!` commits.
- **Uncommitted in the worktree (commit these first, with the user's say-so):** `docs/reference/model.md` (new page, done), `docs/reference/cloud.md` and `ssh-key.md` (Rules/Errors grouping, glue line, opener wording, Oxford commas, data models keep invariants only), `docs/juju.ggarch` (model ERD, migration phases state view, migration sequences), `docs/howto/manage-models.md` (migration troubleshooting replaced by a link; upgrade skew error replaced by a link), `docs/howto/manage-your-juju-deployment/troubleshoot-your-juju-deployment.md`, `docs/requirements.txt` (ggarch pin bumped to `000384e250377b3f57d7b4f75bb8ec14c66ec31e`). Suggested commits: fixups for `cloud.md`, `ssh-key.md` and the pin into their commits; one new commit `docs(reference): rewrite the model page and draw its figures` for the rest. Before any push: `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash upstream/4.1`, rebuild both formats, ask the user (origin only; PR text fenced, never hard-wrapped, no Jira, target 4.1).
- ggarch (the user's repo, pushing allowed): branch `hide-fields`, tip `000384e` (state view ports spread). The scratch clone is `~/git/misc/ggarch-scratch` (the docs venv `~/git/misc/docs-venv` has the pin installed). Live TODOs in `~/git/ggarch/TODOS.md`, "SESSION 83 QUEUE": inline code in captions does not render (the user keeps the backticks), roles such as `{ref}` in captions, links in node and edge labels, the slideshow lost in the expanded view.
- Figures done: SSH key 2 (ERD, import sequence), cloud 1 (ERD), model 3 (ERD with two database groups, migration phase state diagram, migration slideshow of four sequences). Tutorial 3 do not count.

## Your task, in order
0. Commit the uncommitted work (above) once the user agrees.
1. **The SSH server page** (dissolve `explanation/juju-ssh.md`; plan in `TODOS.md`, item "Dissolve explanation/juju-ssh.md"). Code to read: `internal/worker/sshserver`, `internal/worker/sshsession`, `internal/worker/sshtunneler`, `internal/sshtunneler`, `internal/sshconn`, `internal/ssh`, `core/sshproxy`, `apiserver/internal/handlers/sshproxy`, `apiserver/facades/client/sshclient/facade.go` (read: all methods need model admin or superuser; `VirtualHostname`, `PublicHostKeyForTarget`, `PublicKeys`, `Proxy`, `ModelCredentialForSSH`), `apiserver/facades/agent/sshsession` and `hostkeyreporter`, `domain/ssh`. Tables (4.1): controller `controller_ssh_host_key`, `controller_ssh_server_port`; model `machine_ssh_host_key`, `machine_virtual_ssh_host_key`, `unit_virtual_ssh_host_key`, `ssh_connection_request`. Also move the SSH key page's session rule and its error (`public key ... is not associated with model ...`) into this page's connecting operation. Keep the `juju-ssh` label, remove the explanation entry from `explanation/index.md`, add a redirect to `docs/redirects.txt`. The four existing views (SSH proxy overview, connections, Kubernetes, machine reverse tunnel) move to the new page where they help.
2. **The controller page**, with a fixed one-hour probe first: derive the Agent rule (the processes that act for an entity) from the model worker manager and the controller's worker engine; if no rule falls out, write the workers as plain description and log the failed derivation. This is the first process-centric entity, where the skeleton is untested.
3. Then `space` (with `subnet` and `zone`), `secret-backend`, `machine`. The upgrade of a model is done on the model page.
4. Per page: `python3 tools/extract_facade.py <facade dir>` from the 4.1 tree (it reads only the facade; read service and state code too), `python3 tools/build_page_schema.py ...` for the ERD, write the page, `python3 tools/check_page_rules.py <page>`, `ggarch check docs/juju.ggarch`, build `dirhtml` and `latex` into a temp dir (`sphinx-build -b latex . $TMPDIR/x -c . -d $TMPDIR/d`), look at the figures (`experiments/e45/render/shot.sh`, state views via `state_tut.py`), run a Gricean read.
5. When pages are done: squash fixups, write the PR description from `pr-epic-notes.md` when the user asks, ask before pushing. Say in the PR what the skeleton does not cover yet (process-centric entities, a failure part, entities without pages). Acceptance criterion 4 (user feedback on the diagrams) is open.

## Rules the user gave in session 83 (all are in `page-recipe.md`)
Per operation: `Required access:`, then `Rules:` (all rules grouped under one bullet, even one), then `Errors:` (no word "Related"); one generic glue line before them ("The operation's required access, rules, and errors are:"); openers are the gerund phrase plus what it does ("Destroying models removes ..."), never "is the operation that"; a data model keeps only invariants of the records (what an operation does goes in the operation); Oxford comma in every list; link or define jargon at first mention in each section; no metalanguage in captions; no sentence that anticipates the next block; do not repeat a fact in two places; slideshows tell a narrative; a table that repeats the slideshow goes; `model database` is linked like `controller database`.

## Standing directives (binding)
- First principles; nothing random; pre-register before running an experiment; report fails as fails; compute numbers by script; the code is the source of truth (comments are not evidence). Readers are human and AI, more likely AI. Reference pages are client agnostic.
- Never ask for verdicts or offer option menus when the code can decide; when the user asks "should we", investigate and give a recommendation. Ask before any push to juju (the user allowed pushing to ggarch). Run git network, Go, Sphinx and shell commands with the sandbox disabled (the sandbox does not start). Use `python3`, not `python`.
- Check both docs builders. Every PR targets 4.1; branch starts `4.1-`. The user spots wording problems fast (see the rules above).

## Mistakes to avoid
- A scripted string search for a heading matched inside a longer fence (a four-backtick fence string matched inside a five-backtick one) and edited the wrong how-to block; check `git diff` after every scripted edit of a shared file.
- Claims written from memory or from the old pilot without checking the code; a definition removed together with the table that held it (the word "envelope" stayed unexplained); an operation rule left in a data model.
- `pkill -f` kills your own shell; a `latex` build into the worktree's `_build` wipes the live preview.

## Known weak spots, do not hide them
- E44: the pattern is not shown to help AI readers (gain was content, not structure). The form held on SSH key, cloud and model (record-centric) and is untested on process-centric entities.
- Unverified by running: block definitions, import for another user, Kubernetes session identity, cloud spec contents, removal rule, the model page's remediation advice, the migration status strings as a client sees them, the upgrade dry run and the unsupported-base blocker. A question for the Juju developers about key import is in `TODOS.md`.
- The how-to's remaining upgrade troubleshooting item (unit agent not restarting) stays; its facts (agent.conf path, systemd unit names) are unverified and belong on the `agent` or `jujuagentd` page.

## End of session
1. Write the next launch prompt to `NEXT-PROMPT.md` (overwrite) and copy it unchanged to `prompts/session-<N>.md`, where N is the session it launches (84 for this file). Never edit an archived prompt.
2. Append the outcome to `SESSIONS.md` with a one-line pointer to the prompt file that launched this session.
3. Tell the user the one-line start.
