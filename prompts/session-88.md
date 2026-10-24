# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 86, 2026-10-21. The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

---

**Priority (user, 2026-10-21): make progress.** Get all the reference docs, or a substantial portion of them, into the new shape, following the analysis (`page-manifest.md`, `page-inventory.md`, `claims-ledger.md`, `page-recipe.md`). The result feeds the user's lightning talk on how to identify what goes into reference docs, how to chunk it, and how to structure it, so breadth matters more than polish. Fewer distractions: run the pipeline below in parallel batches, do not stop to ask, and do not re-litigate settled rules.

You are continuing two linked jobs: (1) the research project in `~/git/misc/juju-reference`, and (2) the single PR #23661 (draft, branch `4.1-docs-illustrate-docs-juju-9635`, worktree `~/git/misc/juju-tutorial-diagrams`, base 4.1). Code under study: `~/git/misc/juju-v2-preview` (4.1; branch `wip-entity-reference-pilots` must never be pushed). Never touch the main checkout `~/git/juju`.

## State (end of session 86)
- **Pushed to origin: tip `21b7494df3`.** Sixteen reference pages are rewritten (ssh-key, cloud, model, ssh-server, controller, secret-backend, machine, space, subnet, zone, credential, user, secret, relation, offer, action), plus the tutorial and the high availability figure. 33 figure directives in the docs.
- **PR text:** `pr-description.md` (title and body, fenced; the user pastes it). It is current as of `21b7494df3`. Update it for every page added after.
- **Remaining pages by the manifest (tables, noun/facet):** application (21), storage (20, needs a section split first), charm (18), unit (14, process-centric), model-migration (13, mechanism: the model page covers it, decide), link-layer-device (13, no page yet), resource (8), annotation (8, facet), object-store (6), database (5), constraint (4, facet), external-controller (3), telemetry (3), model-defaults (2), upgrade (2), agent-version (2), lease (2), image-metadata (1). `application` waits on the Agent question for its provisioner (see `HANDOFF.md`); decide it with the code, do not ask.
- **Rules added this session** (all in `page-recipe.md`, `WORKING-RULES.md`, `memory-export/`): never glue two facts with different subjects using ", and"; no "batch" or "carry"; base case first, then the variants; kinds that records decide are described in the data model bullet of the deciding record; a status's allowed values stay in the data model and its state diagram and transitions go in the operation that changes it; never write "databag" (say settings); file each fact with its owner (no relic subsections); name the caller first and define "unit agent" once in the Operations introduction (an identity, not an access level); records and software never share a figure. `tools/check_page_rules.py` now flags ", and" glue, a missing Oxford comma, "batch", and "can carry". Its hits for "bullet list with no intro sentence" on nested label bullets and for "top-level title not in the map" on kept titles are accepted false positives.

## The pipeline (it worked: five pages in parallel in about an hour)
1. **Draft agents, one fresh agent per page, five to six at once.** Prompts are in this session's transcript pattern: read `page-recipe.md`, two finished exemplar pages (`credential.md`, `secret.md`, `relation.md`), the old page (audit purpose and benefits, keep every inbound label), and `experiments/e48/grice-review-prompt.md`; rewrite one `.md` only; write the figure views to `/tmp/ggarch-fragments/<page>.ggarch` (never edit `docs/juju.ggarch` in parallel), validated on a temp copy; report needed how-to anchors (do not edit how-tos); run the checker; no commit, no build; trace every error text, code, and access level to file:line.
2. **You merge:** append fragments to `docs/juju.ggarch`, add how-to anchors (an explicit `(label)=` line above the heading), run `ggarch check`, build `dirhtml` and `latex` into fresh `mktemp -d /tmp/...` directories (venv `/home/dora/git/misc/docs-venv/bin`).
3. **Review agents, one per page in parallel** (the Grice prompt). The reviews find 17 to 30 problems per draft, 0 to 13 false statements: they are not optional.
4. **Fix agents:** resume the draft agent with `SendMessage` and the review table (it has the code in context). A bare `{ref}` to a label that now sits on a bullet needs explicit link text.
5. **Commit one page per commit** (signed; Before/After body; read `CONTRIBUTING.md` first), figure sources and how-to anchors in a commit before the pages. Ask before every push (origin only, plain push).
Agents die on the session limit with "You've hit your session limit"; resume them with `SendMessage` after the reset, and read the file first to see what is already applied.

## Open items from session 86
- The ssh-server fix pass was thin: rows 16-19, 21, 23, 26, and 29 of its review were never verified, and the agent-facing operations (`WatchSSHConnRequest`, `GetSSHConnRequest`, `/ssh-tunnel/:tunnelID`, `ReportKeys`) have no section. Redo it.
- Audit the earlier pages (machine, model, ssh-server, controller, secret-backend, space, subnet, zone, credential, cloud, ssh-key) against the newer rules: relic subsections, "the agent of the unit", unit agent defined once, the status diagram placement (model page), "non-x" phrasing, "destroy" where the command says "remove".
- No rendered figure of the new pages has been looked at (live preview: `cd docs; sphinx-autobuild -b dirhtml --host 127.0.0.1 --port 8002 . _build -c . -d .sphinx/.doctrees`, started with the sandbox disabled). Look at the cardinality marks on the cloud, zone, controller, and credential figures and at the two state diagrams.
- Code questions for the Juju developers are in `TODOS.md` and in the PR text (task cancel statement, `machinemanager.go:179`, revoke level, how-to versus code differences, `ImportKeys`).
- The claims read from code and never run are listed in the PR text under "Not verified by running".

## Standing directives (binding)
First principles; the code is the source of truth; report fails as fails; pre-register before an experiment. Readers are human and AI. Reference pages are client agnostic. Decide and edit: no option menus, no verdict-asking. Ask before any push (origin only). Run git network, Go, Sphinx, and shell commands with the sandbox disabled; use `python3`. Check both docs builders. Every PR targets 4.1; branch starts `4.1-`. `gh` is not installed: use `curl` for read-only checks. PR text in fenced blocks, never hard-wrapped, Jira JUJU-9635 line kept. The user's usage meter matters: use fresh Sonnet agents with narrow prompts for sweeps and reviews, keep this context small, and write state to disk early.

## End of session
Overwrite this file, copy it unchanged to `prompts/session-<N>.md` (N is 89 for this file's successor; 87 was an interim safety copy and 88 is this file), append the outcome to `SESSIONS.md`, update the block in `HANDOFF.md`, tell the user the one-line start.
