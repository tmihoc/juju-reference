# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 84, 2026-10-20. The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

---

You are continuing two linked jobs: (1) a research project on the structure of Juju reference documentation (`~/git/misc/juju-reference`), and (2) **epic JUJU-9635, illustrate the docs, due 2026-10-21, delivered as ONE PR**. Code under study: `~/git/misc/juju-v2-preview` (4.1; branch `wip-entity-reference-pilots` must never be pushed). Never touch the main checkout `~/git/juju`.

## Read first, in this order
1. `HANDOFF.md`, the block "State at the end of session 84 (final)".
2. `page-recipe.md` (procedure and every page rule, now including the data model rule test and the remediation rule) and the end of `skeleton-v6.md`.
3. `TODOS.md`, `pr-epic-notes.md`, `WORKING-RULES.md`, `memory-export/MEMORY.md`, and the end of `structure-discovery-plan.md` (E47).

## State of the epic PR
- Branch `4.1-docs-illustrate-docs-juju-9635`, worktree `~/git/misc/juju-tutorial-diagrams`, off `upstream/4.1` at `e5db99d585`. **Pushed to origin** (tip `893bcbb98b`), five signed commits with bodies: tutorial, SSH key, cloud, model, SSH server. The user opens the draft PR from `https://github.com/juju/juju/compare/4.1...tmihoc:juju:4.1-docs-illustrate-docs-juju-9635` and asked for the PR to grow. The PR text (title, why, form, pages to review with RTD links, checklist, Jira JUJU-9635) was given to the user in session 84; the RTD pattern is `https://canonical-juju-1--<PR>.com.readthedocs.build/<PR>/<path>/`.
- **Rules for further commits** (CONTRIBUTING.md and `.github/instructions/agent-commit.instructions.md`, commitlint blocks the PR): `<type>(<scope>): <lowercase description>`, a body on every `docs` commit in Before/After form, lines of 100 characters or fewer, signed (the configured SSH key signs; `%G?` shows N only because no allowed-signers file exists, check `git cat-file -p <sha> | grep gpgsig`). Reviewer-driven fixes go in separate commits on top (no squash after the PR is open). A rewrite of pushed history needs the user's go and `--force-with-lease=<branch>:<old sha>`; ask before every push.
- Figures: 8 outside the tutorial on 4 pages (14 views, counting slides). The epic wants 10 new diagrams, so at least 2 more figures are due: the controller page (HA topology), and space, secret-backend, machine data models.
- ggarch pin `000384e250377b3f57d7b4f75bb8ec14c66ec31e` (`hide-fields`). Open ggarch TODOs in `~/git/ggarch/TODOS.md`, "SESSION 83 QUEUE".

## Your task, in order
1. **Audit the model and SSH key pages with the data model rule test** (a rule stays in the data model only if the DDL enforces it; cite the constraint; move the rest to the operation). Known suspects on the model page: "inactive until creation finishes", "the type follows the cloud", "a model has at most one active migration" (check for a unique index or trigger). Commit as a separate commit on top.
2. **The controller page.** E47 failed to derive an Agent rule (see the plan): write the controller's workers as plain prose, tied to what an interface shows (`juju_engine_report`, `/depengine`), and say so. Facts found: the controller agent is the machine agent's engine on a controller machine (`ifController` wrappers select 39 of 110 manifolds in `cmd/jujuagentd/agent/machine/manifolds.go`, listed by `experiments/e47/classify.py`); a model engine is started per model by the model worker manager (33 manifolds, `cmd/jujuagentd/agent/model/manifolds.go`); unit engines are started by the deployer (`internal/worker/deployer/unit_manifolds.go`). Data model from the 7 controller tables of the manifest; operations from `apiserver/facades/client/controller`; HA topology and bootstrap sequence figures. The SSH server page already holds `SSHServerHostKey` and `SSHServerPort` (controller facade, login access).
3. Then `space` (with `subnet` and `zone`), `secret-backend`, `machine`. Per page: `python3 tools/extract_facade.py <facade dir>` (reads only the facade, and found nothing for `sshclient`: read the facade file too), `tools/build_page_schema.py` for the ERD (trim neighbours by hand, as `docs/juju.ggarch` SSHServerSchema did), write the page, `tools/check_page_rules.py`, `ggarch check docs/juju.ggarch`, build `dirhtml` and `latex` into `$TMPDIR`, render figures (`$TMPDIR/r.sh`-style: `ggarch render` then `experiments/e45/render/shot.sh`), a Gricean read (quality: trace each claim; quantity: what a client needs; relation: exposed on an interface; manner: jargon, negation, repeats), then a per-operation "See also" to the how-to under the heading (add the how-to anchor if none exists and a how-to section does).
4. Say in the PR what the skeleton does not cover yet (process-centric entities, a failure part, entities without pages).

## Rules the user gave in sessions 83 and 84 (all in `page-recipe.md`)
Per operation `Required access:`, `Rules:` (one bullet), `Errors:`; gerund plus entity titles (the entity stays in the title: "Connecting to machines through the SSH server"); openers say what the operation does; the data model keeps only DDL-enforced invariants; remediations say what to do, never a consequence ("Remove the models first"); Oxford comma; link or define jargon at first mention in each section; no metalanguage in captions; no sentence that anticipates the next block; no repeated fact; slideshows tell a narrative (a coarser copy of a later slide is dropped); name every participant the same way across a slideshow (SSH tunnel server, target SSH server, machine SSH server) and keep orientation left to right; grey nodes are software outside Juju; a figure is the first thing in its section and a lede has none; a "See also" link to the how-to goes directly under the operation heading (clear scope), only where a how-to section exists; the old page's purpose and benefits must survive a rewrite (audit the old text); do not state a claim that no code shows (the "inspect" claim was dropped).

## Standing directives (binding)
- First principles; nothing random; pre-register before running an experiment; report fails as fails; compute numbers by script; the code is the source of truth (comments are not evidence: the SSH port's "controller charm owns it" rests on a comment). Readers are human and AI. Reference pages are client agnostic.
- Never ask for verdicts or option menus when the code can decide. Ask before any push to juju (origin only, never upstream). Run git network, Go, Sphinx and shell commands with the sandbox disabled. Use `python3`. Check both docs builders. Every PR targets 4.1; branch starts `4.1-`. `gh` is not installed: use `curl` against the GitHub API for read-only checks. PR text in fenced blocks, never hard-wrapped, Jira JUJU-9635 line kept.

## Mistakes to avoid
- Pushing before checking CONTRIBUTING.md (two commit bodies failed the rules and needed a force-push): read the commit rules first.
- Scripted string edits of shared files: check `git diff` after each. `pkill -f` kills your own shell. A `latex` build into the worktree's `_build` wipes the live preview: build into `$TMPDIR`.
- Participant names that mean two things in one slideshow; unverified inherited claims; rules in data models that only a service enforces.

## Known weak spots, do not hide them
- E44: the pattern is not shown to help AI readers. The form held on SSH key, cloud, model and SSH server (record-centric); untested on process-centric entities. E47: no Agent rule fell out.
- Unverified by running: block definitions, import for another user, Kubernetes session identity, cloud spec contents, removal rule, the model page's remediation advice, migration status strings as a client sees them, the upgrade dry run, machine host keys after a migration, the SSH server page's relay endpoint and error statuses, the port set over the control socket by the controller charm.
- A question for the Juju developers about key import is in `TODOS.md` and in the PR text.

## End of session
1. Write the next launch prompt to `NEXT-PROMPT.md` (overwrite) and copy it unchanged to `prompts/session-<N>.md` (N is 86 for this file's successor). Never edit an archived prompt.
2. Append the outcome to `SESSIONS.md` with a one-line pointer to the prompt that launched the session.
3. Tell the user the one-line start.
