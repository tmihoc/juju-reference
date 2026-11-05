# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 81, 2026-10-20. The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

---

You are continuing a research project on the structure of Juju reference documentation, and the user has made one deliverable the priority: **epic JUJU-9635, due 2026-10-21 (tomorrow)**. Work in `~/git/misc/juju-reference` for the record and in the worktree `~/git/misc/juju-diagrams` (branch `4.1-docs-illustrate-docs-juju-9635`, from `upstream/4.1` at `e5db99d585`, no commits yet) for the docs. Never touch the main checkout `~/git/juju`. The code under study is `~/git/misc/juju-v2-preview` (Juju 4.1; branch `wip-entity-reference-pilots` must never be pushed).

## The epic (the user's text, spirit over letter)
Documentation is heavily text-based with limited visual aids outside tutorial and architecture docs. Add diagrams to explanation and reference docs.
Acceptance: (1) 10 new diagrams integrated into explanation and reference docs; (2) all follow the style and tooling of the architecture doc (ggarch, `docs/juju.ggarch`); (3) the diagram creation process is documented for contributors; (4) user feedback confirms the diagrams help (cannot be met in a day: report it as open).
Card breakdown: identify and prioritise opportunities (candidates the user listed: charm lifecycle, HA topology, cross-model relations, storage, secrets, agent workers, migration, backup/restore, network spaces, relation databag flow; pick 10 by pain and impact); create 10 diagrams (version-controlled sources, existing build pipeline, a narrative for each); document the process (contributor guide, tooling setup, build integration, review process).
The user's additions: the 3 diagrams in `tutorial/index.md` can be converted to ggarch now (3 of 10); the intent is to get rid of every non-ggarch diagram, by converting it or discarding it as bad; add ERDs to data-model parts and sequence diagrams to operations parts of the reference so the reference serves every Juju client (all of them point there); this reference redo started because the pages had no rhyme or reason that would make diagrams meaningful.

## Read first, in this order
1. `HANDOFF.md`, the block "State at the end of session 81" (it lists the legacy figures, the tooling facts, the E44 result and the user's directives).
2. The plan, E45 (pre-registered, plus "E45 results so far") and E44 amendments A1 and A2. `skeleton-v6.md` and `claims-ledger.md` (a bare `Cnn` is settled, `Cnn*` partial). `WORKING-RULES.md`, `memory-export/MEMORY.md` (the caption style, tabs alphabetical, no unearned negation, capitals after a colon, both docs builders).
3. `docs/agents/AGENTS.documentation.rules.md` in the worktree (lines 34-36 and 169-190: one model `docs/juju.ggarch`, no committed SVGs, colour means ownership only, captions carry the technical detail, `ggarch check`, the pinned SHA), and `~/git/ggarch/SKILL.md` (authoring guide; section 0 covers `ggarch scaffold` from DDL).

## Standing directives from the user (binding)
- Use first principles. Do nothing at random; do not rush to satisfy the epic in a way that discards the reference work or has to be redone. Be strategic: derive the diagram set from properties of the software (E45), then build.
- Never ask for verdicts or offer option menus; investigate and let the answer come out of the code. Ask before any push; push to origin only. Run git network, Go, Sphinx and shell commands with the sandbox disabled.
- Pre-register before running anything; report fails as fails; label post hoc readings; compute numbers by script, never from memory.
- Code is the source of truth; existing pages and diagrams are weak precedent. Check each legacy figure against the code before converting it (the HA, relation and status figures may state things the code contradicts).
- Readers are human and AI, more likely AI: the caption and alt text restate each figure's facts. Structure by the logic of the running thing, not by persona or code layers; show what an interface exposes and keep unexposed jargon off the page (Grice: quality, quantity, relevance, manner).
- Every PR targets 4.1, branch starts `4.1-`, PR text in a fenced block never hard-wrapped, no Jira. Check both docs builders (`dirhtml` and `latex`; `experiments/build.sh <worktree> <dirhtml|latex> <log>`). Run `gci` on any Go file touched (none expected). The ggarch distribution blocker (the tool lives in `tmihoc/ggarch`, pinned by SHA in `docs/requirements.txt`) is known; do not change the pin without checking the build.

## Your task
1. Finish E45 as registered: kinds O (sequences: interface operations whose call graph crosses at least 3 actors with at least 4 ordered steps, from `experiments/e30` and `e37` data and the code), L (life and status state diagrams with at least 3 states and explicit transitions: ledger C16, C39), T (topology with multiplicities that differs per deployment: HA, cross-model); the exposure ranking; for each ERD component above 12 tables, the split by the E41 section levels checked against the code; the disposition of every legacy figure listed in HANDOFF (convert, discard, or stays) by the same rule, each checked against the code first. Write the ranked list into the plan with the code facts behind each row.
2. Build the first ten (the three tutorial figures convert as 3 of 10 only if they pass the rule or are explained: they are small topology sketches of the architecture the architecture doc already draws; reuse its views where the model already has the nodes). ERDs from `ggarch scaffold` on `experiments/e11/*.ddl` (regenerate from the 4.1 tree if stale); sequences with a file and line per step. Add the views to `docs/juju.ggarch`, embed with `{ggarch}` plus caption and alt text, and write a narrative. Remove the retired figure files and their `.excalidraw` sources. Run `ggarch check`, then both builders, and look at the rendered figures.
3. Write the contributor guide (a page under `docs/`, linked from the docs index or contributor area as the repo's layout allows; the content is in AGENTS.documentation.rules.md and SKILL.md: tooling setup, adding a node and a view, embedding, preview, review checklist, the pin).
4. Update the record: plan (E45 results), HANDOFF, TODOS, SESSIONS (add "Launched by prompts/session-82.md"). Tell the user what is done against the four acceptance criteria and what is open (feedback). Propose the PR split; ask before pushing.
5. Only after the epic: the E44 follow-ups in `TODOS.md` item 0 (coverage sweep, structure-free control, ledger and skeleton updates).

## Known weak spots, do not hide them
- E44: the pattern is not shown to help AI readers (gain is `ssh-key` alone; content, not structure); all judges and readers are the same model family as the author.
- E45 thresholds (4 to 12 tables, 3 actors) come from the shape of existing views and are untested.
- 49 of 63 ledger rows have had no second reader; ten page groups split between the judges and the schema rule.

## End of session
1. Write the next launch prompt to `NEXT-PROMPT.md` (overwrite) and copy it unchanged to `prompts/session-<N>.md`, where N is the session it launches. Never edit an archived prompt.
2. Append the outcome to `SESSIONS.md` with a one-line pointer to the prompt file that launched this session.
3. Tell the user the one-line start.
