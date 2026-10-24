# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 82, 2026-10-20. The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

---

You are continuing two linked jobs: (1) a research project on the structure of Juju reference documentation (`~/git/misc/juju-reference`), and (2) **epic JUJU-9635, illustrate the docs, due 2026-10-21, to be delivered as ONE PR**. Code under study: `~/git/misc/juju-v2-preview` (4.1; branch `wip-entity-reference-pilots` must never be pushed). Never touch the main checkout `~/git/juju`.

## Read first, in this order
1. `HANDOFF.md`, the block "State at the end of session 82 (final)".
2. `page-recipe.md` (the procedure for a page: facts, sections, text rules, figures, checks) and the end of `skeleton-v6.md` (every rule the user gave in session 82, with the reason). These replace the old Identity/State/Dynamics parts for the pages we write.
3. `TODOS.md` (the live queue starts with the epic page order), `pr-epic-notes.md` (what the PR description must say; the user will ask for the text later), `WORKING-RULES.md`, `memory-export/MEMORY.md`.

## State of the epic PR
- Branch `4.1-docs-illustrate-docs-juju-9635`, worktree `~/git/misc/juju-tutorial-diagrams`, off `upstream/4.1` at `e5db99d585`. **Nothing is pushed.** Commits so far: tutorial diagrams (`44c29b27fd`), SSH key page (`338dac9413`), cloud page (`eb4fcc87a0`), then about ten `fixup!` commits on the last two. **Before any push, squash them:** `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash upstream/4.1` (interactive editors are not available), rebuild both formats, then ask the user before pushing (origin only; the PR text goes in a fenced block, never hard-wrapped, no Jira, target 4.1).
- ggarch: the pin in `docs/requirements.txt` is `tmihoc/ggarch@aeb653ab3d08e4399f2ca5d4762ea0fed5f9aa0e` (branch `hide-fields`, pushed): `fields: hidden` (collapsed records that keep 1/m cardinalities), `charmed-entity` (dotted entity with the Juju mark), `context-record` (record badge plus an outlined arrow). The scratch clone is `~/git/misc/ggarch-scratch` and is installed in the docs venv `~/git/misc/docs-venv`; `ggarch render` cannot draw state views (the Sphinx build can; `experiments/e45/render/state.py` renders one).
- Held back, not in the PR: the relation, action, model ERDs, migration phases, HA figure and status-figure removal are committed only on the local branch `4.1-docs-held-back-figures` (worktree `~/git/misc/juju-diagrams`). The user judged the relation and databag figures weak; the migration phase state diagram (11 phases, `core/migration/phase.go`) and the HA topology are good candidates to reuse once their pages exist.
- Preview servers: port 8003 serves the epic worktree (cloud at `/reference/cloud/`), port 8002 the old pilots. **Never run `experiments/build.sh ... latex` into the worktree's `_build` while the server runs**: it wipes the HTML. Build the PDF check into a temp dir (`sphinx-build -b latex . $TMPDIR/x -c . -d $TMPDIR/d`). Never `pkill -f` (it kills your own shell): use `kill <pid>`.

## Your task, in order
1. Next pages, content first, diagrams only after the content is settled (the user's rule): **`model`** (foundational; pilot at `~/git/misc/juju-v2-preview/docs/reference/model.md`; ERD of the 4-table model-database star; the migration phase state diagram and a migration sequence; effects of other operations), then **the SSH server** (dissolve `explanation/juju-ssh.md` into a reference page; plan in `TODOS.md`), **`space` with `subnet` and `zone`**, **`secret-backend`**, **`controller`** (HA topology, bootstrap), **`machine`** (provisioning). Later, once the Agent rule exists: unit, application, charm, hooks, agent. Foundational notions per the user: client, controller, cloud, charm, application, unit, machine. The epic's list (charm lifecycle, HA topology, cross-model relations, storage, secrets, agent workers, migration, backup/restore, network spaces, relation databag flow) is only a source of ideas; say in the PR which topics are not covered.
2. For each page: `python tools/extract_facade.py <facade dir>` (it reads only the facade: read the service and state code too), `python tools/build_page_schema.py ...` for the ERD, write the page, `python tools/check_page_rules.py <page>`, `ggarch check docs/juju.ggarch`, build `dirhtml` and the PDF check, look at the figures, run a Gricean read. Diagram count today: tutorial 3 (do not count against the 10), SSH key 2 (ERD, import sequence), cloud 1 (ERD). The 10 new diagrams must be honest: a sequence only when the operation crosses at least three actors with one outside the controller and the order matters; an ERD where the page has related records.
3. Keep the user's rules in `page-recipe.md` current as new ones arrive; the SSH key page took about twenty rounds of feedback, so check each new page against the recipe before showing it.
4. When the pages are done: squash the fixups, write the PR description from `pr-epic-notes.md` when the user asks, ask before pushing. Report acceptance criterion 4 (user feedback on the diagrams) as open.
5. Only after the epic: the E44 follow-ups in `TODOS.md` (structure-free control, ledger and skeleton updates), the error index, the tables-by-topic page, the watcher concept page.

## Standing directives (binding)
- First principles; nothing random; pre-register before running an experiment; report fails as fails; compute numbers by script; the code is the source of truth (comments are not evidence). Readers are human and AI, more likely AI. Reference pages are client agnostic.
- Never ask for verdicts or offer option menus when the code can decide; when the user asks "should we", investigate and give a recommendation. Ask before any push. Run git network, Go, Sphinx and shell commands with the sandbox disabled (the sandbox does not start).
- Check both docs builders. Run `gci` on any Go file touched (none expected). Every PR targets 4.1; branch starts `4.1-`.
- The user spots wording problems fast: definitions not descriptions, no metalanguage ("this section covers"), no unearned negation, no table names or CLI links, link jargon at first mention per section, American spelling, `Required access` not `Authority`, lists need a substantive intro sentence, figures first in their section with self-sufficient captions, the page's own subject as the grammatical subject.

## Known weak spots, do not hide them
- E44: the pattern is not shown to help AI readers (gain was content, not structure); judges and readers are the same model family as the author. The form was settled on one small entity (SSH key) and is untested on large ones.
- Unverified by running (listed in `pr-epic-notes.md`): the block definitions, import for another user, the Kubernetes session identity, the cloud spec contents, the removal rule. A question for the Juju developers about import is in `TODOS.md`.
- The extraction script reads facade code only; domain errors and checks in other layers need reading.

## End of session
1. Write the next launch prompt to `NEXT-PROMPT.md` (overwrite) and copy it unchanged to `prompts/session-<N>.md`, where N is the session it launches. Never edit an archived prompt.
2. Append the outcome to `SESSIONS.md` with a one-line pointer to the prompt file that launched this session (`prompts/session-83.md`).
3. Tell the user the one-line start.
