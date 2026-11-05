# Reference-page skeleton: research summary (state at the end of session 78, 2026-10-19)

Start here in a new chat, then read `HANDOFF.md` (router, discipline, branches) and `TODOS.md` and the end of `structure-discovery-plan.md` (full record). This file is the map: the question, what was tried, what the evidence says, what is open, and where everything lives.

## The question

What is the right fixed structure ("skeleton") for a reference page about a Juju entity (machine, controller, model, unit, access, ...)? Requirements set by the user: a tight dictionary logic (the same parts in the same order on every page); client-agnostic (the CLI and Terraform docs point to the reference, never the other way round); how-tos follow the entity lifecycle, reference follows entity attributes; the skeleton must be grounded in the shape of the software, and judged as a scientific theory: explanatory (fits the starting data) and predictive (fits new data). Human raters are ruled out (error prone); LLM raters were used for the sentence experiments and are a known weakness.

What belongs in docs/ (the inclusion test, from the plan, 2026-10-19): every fact observable at a named user-facing interface (operator CLI, config, status and logs; client developer API and errors; charm developer hook tools, metadata and Ops), pulled up from wherever it is authored, plus spanning facts that no single package can state (cross-process, cross-domain). Local developer-only facts stay in `doc.go`, schema comments and CONTRIBUTING.

## How the theory moved (each step was argued, then tested or withdrawn)

1. Layered form (declaration, persistence, execution; ADR-016). PR #23451. Weak for errors (55% blind agreement), reliable for rules (80%). **The PR will not land** (user, 2026-10-19).
2. Flat page: lede, data model, change streams, operations, plus an optional actor part (agent or workers) for entities with their own process or engine. Pilots: machine, controller, model.
3. Order argued several times: actor first, then withdrawn for the causal chain (records, streams, actor, operations), then the user's "agent is tied to existence" intuition. Evidence on order is weak (see below).
4. First-principles derivation: state, observation, agent, dynamics (plus identity). Tested by blind classification (E7 to E10).
5. Theory v4 after a red team: identity, interface (addressing and syntax), state (vocabulary first), dynamics (operations with preconditions and errors), then agent and observation only when non-empty; applicability and guidance as annotations on the statement they qualify; an error index by string; shared mechanisms on their own pages. Proposed, not ratified.
6. Software-first (E11, the current direction): derive the parts from the artifact classes in the code and use the docs only as something to compare against.

## Evidence (all numbers recorded in the plan; scripts in `experiments/`)

| Experiment | What | Result |
|---|---|---|
| Layers (E3) | blind classification into declaration/persistence/execution | errors kappa 0.33, rules 0.70: weak axis |
| Agent test (machine page) | 16 questions, layered against pilot page | tie when the whole page fits; padded tables hurt under chunking |
| E7 | 72 sentences from the pilots into 5 kinds, two raters | raters 94% (kappa 0.93), against filing 89% |
| E8 | 206 sentences not written under the skeleton (18 layered pages, Go package docs), 6 classes | kappa 0.88; "none" 4-5% on user docs, 26-28% on developer docs (rationale, code layout); 35% secondary labels, mostly state against dynamics |
| E9 | boundary rule state/dynamics on 90 fresh sentences | rule effect unobservable (baseline straddles were already few); agreement 0.77 to 0.85 |
| Reader test (access.md) | 13 questions plus 2 probes, old against new, graded blind | whole page 30/30 both; chunked 29 new against 25 old (one run) |
| Red team | an independent agent attacked v4 | missing kinds: interface, applicability, guidance; vocabulary, mechanism and program pages misfit; 29 empty-slot filler sentences; errors need an index by string |
| E10 | 202 sentences from 70 random reference pages plus errors, 8 classes, no error instruction | kappa 0.87; interface about a third, failure 15% (recognised as a kind), agent 3%; order evidence thin (44 pairs) |
| E13 | recall test: 152 claims from 4 pre-existing human-written pages checked against the code | shallow pass: 26% strictly derivable (55% with partial) against a pre-registered 80%: failed; the deeper E14 pass shows the shallow "not derivable" label was mostly a search-depth artifact (94% of claims are code-decidable, 51% strictly supported); 3 doc claims contradicted by the code |
| E14 | close scrutiny of the 68 "non-mechanical" claims from E13 | 57% hold, 24% overstated, 6% wrong; 59 of 68 decidable by the code, so E13's "not derivable" was a depth artifact; 94% of all 152 claims are code-decidable |
| E15 | version stability, 4.0.15 DDL against 4.1 DDL, typing replayed in SQLite | registered criterion failed (a, b, c pass; the source-diff reverse check and one domain-ownership difference fail); table-level typing stable and exact, domain typing depends on code ownership; release DDLs are histories, namespace ids renumbered |
| E11 | the software itself: real 4.1 DDL (generated by a throwaway Go program, includes Go-made triggers), Go census, facades, workers | see below |

## What the software shows (E11, 4.1; pilot worktree at d963678fb9)

- 330 tables (249 model, 94 controller counting overlaps). Artifact classes: tables, 406 foreign keys, 160 unique, 33 checks, lookup tables (allowed values), 79 views (derived attributes), change-log triggers (74 watched model tables), immutable-table triggers (23 tables), a `removal_type` lookup.
- **Lifecycle entities against records is a hard split, in the schema:** only 13 model tables carry `life_id` (model, machine, machine cloud instance, application, unit, relation, remote offerer and consumer, storage instance, volume, filesystem and attachments; controller node and object store backend in the controller schema). The docs' "no life column, no state machine" claims match the code for every entity checked.
- **Removal is one mechanism** (`domain/removal`, 20 removal types, 13 services with one shape: remove with force and wait, mark not alive with cascade, schedule job, agent marks dead, job checks guards and deletes). The per-type cascade and guard errors are derivable from the code.
- Domains are of at least four kinds: lifecycle entity (7), record entity (23), value store or lookup (14), mechanism or service-only (11). "Exactly three types" was not confirmed.
- **Observation has two layers:** the schema generates change-log namespaces per table; the service exposes `Watch*` methods separately. Access has a trigger and no watch method.
- **Explicit state machines in code:** migration phase (`validTransitions`), relation, volume and filesystem status transitions. Unit, application and machine statuses have none (matches "upserts gated by writer").
- Exported-declaration census (3,375 in 62 domains): state shapes, request shapes (`*Args`, `*Params`), vocabularies, validators, identifier generators, errors, migration, services; no recurring construct outside the six parts, other than developer-only plumbing. Refinements: state machines as code, events delivered to charms (a vocabulary), external collaborators as actors in operation steps.
- **Exposure tiers** (computed from the code): T1 client-facing, T2 cross-process (agent and controller facades), T3 internal to one process, T0 unreferenced. Against the pilots: machine watchers 6 of 9 are T1/T2 (pilot lists 4); all model watchers are internal except the credential one (the pilot lists internal ones); errors documented on the pilots: machine 21 of 23, model 12 of 13, controller node 5 of 5, relation 18 of 23. The machine pilot lacks the removal cascade (units, child machines, storage) and the force and wait parameters.

## Where things stand against "explanatory and predictive" (updated at the end of session 78)

- Explanatory: yes. The kinds fit the data (kappa about 0.87 on unfiltered text), and the artifact classes in the code line up with them.
- Predictive: partly. The content of the observation, error, state-machine and removal parts can be derived from the code, and hand-written text differs from the derivation (which direction depends on the exposure tier). Not shown: that the structure is what readers need; the entity typing is unsettled; order is weakly supported (identity first; state before dynamics and before failure; dynamics before failure).
- Caveats: LLM raters only; heuristic ownership of tables; error reachability is a name-based call graph; the single reader test has one run.

## Open items

1. Decide what the entity page shows of observation. See the note in the plan: surface the trigger semantics and the client-facing streams, not Go method names; cross-process triggers appear as the "trigger" of dynamics entries; internal watchers stay in `doc.go`.
2. Fix interface scope (platform-level addressing and request grammar; CLI flags belong to the client docs) and the dynamics/interface boundary.
3. Error index by string (one generated global page, JSON twin; authoring stays nested at the home).
4. Shared pages for cross-cutting mechanisms: removal, migration, status, authorisation, hooks and leadership.
5. Rename the client-specific sequence views in `docs/juju.ggarch` before client docs link to them.
6. The pilots are not yet reconciled with the exposure tiers (model observation shrinks; machine gains two cross-process streams and the removal cascade).
7. Convert the unit page; re-run the sentence classification on rewritten pages.

## Proposed tests of the skeleton as a predictor (pre-registered in the plan; test 1 has run as E13 and failed its 80% criterion, with a post hoc reading in the plan)

- Out-of-sample recall: for the 16 entities, take the human-written pages of upstream/4.1 (written by others before our rewrite), extract the facts they state, and check how many are derivable from code artifacts; the residue should fall into named classes.
- Version stability: derive the typing and part inventory from the 4.0.15 DDL and from 4.1; the typing should be unchanged for entities that did not change.
- Generator: build the part inventory for held-out domains purely from the code and compare with the existing pages.

## Where everything is

- `HANDOFF.md` (router), `TODOS.md` (live queue), `SESSIONS.md` (history), `WORKING-RULES.md`, `memory-export/`.
- `structure-discovery-plan.md`: the full record; the last sections are E7 to E11 and the first-principles derivation.
- `entity-page-form.md` (v1, v2 pointer, v3 note), `entity-page-form-v2-proposal.md`, `reference-page-types.md` and `error-inventory-vs-howto-troubleshooting.md` (both carry a session 78 status note).
- `experiments/e7/` (sentence experiments E7 to E10, `reader/` for the reader test and `redteam.md`), `experiments/e11/` (`inventory.py`, `artifacts.py`, `census.py`, `observe.py`, `errors_tier2.py`, DDL copies `model.ddl` and `controller.ddl`, `tables.json`, `artifacts.json`).
- Pilots: worktree `~/git/misc/juju-v2-preview`, local branch `wip-entity-reference-pilots` (never push). Commits on top of `01caeb030b`: `7e27ac4f86` actor part, `cf5f22959e` agent page, `8ca19bf496` one home per fact, `ac597e34b0` causal order, `c605affa18` controller chain, `5533b1e109` machine intros, `d963678fb9` access in the attribute skeleton. Pages: `docs/reference/{machine,controller,model,access,agent}.md`.
- Regenerating the DDL: a throwaway `main` in the pilot worktree that writes `schema.ModelDDL().Patches()` and `schema.ControllerDDL().Patches()` through `coreschema.Stmt` (the repo's `generate/ddlgen` does the same for released versions); delete it afterwards.
- Previews: `cd juju-v2-preview/docs && source ~/git/misc/docs-venv/bin/activate && sphinx-autobuild --port 8002 --host 127.0.0.1 . _build -c . -d .sphinx/.doctrees -b dirhtml -j auto -D llms_txt_enabled=0 --ignore '_build/*' --ignore '.sphinx/*'`. The sandbox does not start: run git network, sphinx and Go with it off.

## Update at the end of session 78
E12 to E14 are recorded in the plan. In short: the code decides 94% of the claims on four old pages; the conceptual layer is checkable and about a third of it fails the check; the skeleton is a pipeline (code facts generated, with exposure tiers; hand-written statements admitted through a citation gate). Next, in order: test 2 (version stability, 4.0.15 against 4.1), test 3 (held-out generator), the claim-gate prototype. See `HANDOFF.md` and `TODOS.md` for the first tasks and the branch state.

## Update, session 79
Test 2 ran as E15 (see the plan). Table-level typing (life, status, watched, immutable, lookup) is a version-stable function of the net schema and changes exactly where the schema changed; the registered criterion failed at the two checks that bring in source history and code ownership. Model lifecycle set unchanged (15 life tables, not 13); controller lifecycle grows from 1 to 3 tables; observation grew the most. Next: test 3 (held-out generator), claim-gate prototype.
