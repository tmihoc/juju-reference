# Juju reference pages: types and treatment

Revised 2026-09-30 (session 76) after checking the first version against the
4.1 source (`domain/schema`, `cmd/`, the domain packages). Sources: ggarch
ADR-011, ADR-013 (amended the same day), ADR-014, ADR-016, the 4.1 reference
index, and a scan of every top-level page on the prep branch
`origin/4.0-docs-rewrite-juju-architecture-juju-9632`.

The prep branch has 51 top-level pages under `docs/reference/` besides
`index.md`, plus leaf catalogues (CLI pages, hook commands, supported clouds,
config keys, introspect macros). Individual pages were not opened for the
scan: which persistence sections already follow ADR-014 (ERD-first) is
unconfirmed. DPE = declaration / persistence / execution.

## The form for entity pages (ADR-016)

Types 1 and 2 follow the layer-anchored form in `entity-page-form.md`: no
free-standing rules-and-errors section; each rule and error sits inside its
layer, anchored by lifecycle action (declaration), stored record component
(persistence) or operational loop (execution), and filed by the Go raise site.
The worked example is `machine-rewrite-draft.md`.

## Types and treatment

| # | Type | Pages | Treatment |
|---|---|---|---|
| 1 | **Entity, full spine** (16 from ADR-013, plus access) | cloud, credential, user, model, application, unit, relation, offer, secret, action, machine, storage, space, ssh-key, controller, charm; access | ADR-016 form. Take the prep page's final state, re-verify every claim and error against 4.1, file each error by raise site. |
| 2 | **Entity, facet-honest** (a layer is empty or by reference; three cases below) | bundle, constraint, placement-directive, script, subnet, resource-charm, zone | ADR-016 form where layers are real; an empty layer is one sentence. |
| 3 | **Executor** (runs the work; no declaration from the user) | agent, worker, pebble, jujud (jujuagentd), containeragent | Keep their current form. Pebble is an external product. jujud and containeragent are the binaries: re-check against jujuagentd. |
| 4 | **Stage link** (hands persistence to execution) | watcher | Keep its form. Pair with database. |
| 5 | **Substrate** | database | Keep. Its layer titles differ from the spine (ADR-011 meta-entity). |
| 6 | **Instrument, client side** | client, juju-cli, juju-web-cli, juju-dashboard, the juju-metadata plugin | Keep the form, check for stale claims. |
| 7 | **Instrument, on-host or charm side** | jujuc, hook-command, juju-db-repl, resource-compute (alias of machine plus on-machine commands) | Keep the form. `juju-db-repl` is a shell function from the introspection worker, not a client command. |
| 8 | **Observation** | log, telemetry, status | Telemetry belongs to PR 3. Status data lives in each entity's tables; the page explains the `juju status` view. |
| 9 | **Process** | scaling (pure process); removing-things and upgrading-things (chain-walks that also persist `removal` and `upgrade_info` records) | Verify against 4.1. Upgrade passes the entity test: candidate for type 1 later. |
| 10 | **Platform overview** | juju.md, juju-cross-version-compatibility | Keep. |
| 11 | **Leaf catalogues** | list-of-supported-clouds, hook-command list, introspect macros, generated CLI and config-key pages | Out of scope, except pages PRs 2 and 3 own. |

The three facet-honest cases (type 2):

- No record: **bundle** (client-side; Juju stores its contents).
- Record held on another entity's record: **placement-directive**
  (`machine_placement`) and, loosely, **constraint** (which also has its own
  tables).
- Discovered, no declaration: **zone** and **subnet** (`cmd/juju/subnet` has
  `list` only; `availability_zone` and `provider_subnet` are cached provider
  facts). Space is declarable.

## Corrections from the first version

- **high-availability** was a process. The `juju enable-ha` command is gone in
  4.1 (the `EnableHA` call remains on the controller API); HA is the controller's
  Raft/Dqlite arrangement plus the controller charm. File it with **controller**
  (execution layer).
- **watcher** was an Executor. It is the persistence-to-execution hand-off.
- **`juju-db-repl`** was a client instrument. It is an on-host shell function.
- **pebble** is external: Juju stores nothing about it.
- **script** is a kind of operation. The stored entity is the operation and
  its tasks (`0033-operation.sql`, ten tables), shared with action. The
  ADR-013 reason ("charm content") was wrong; the facet-honest class holds.
  Action and script may belong on one page, or the operation gets its own.
- **zone**'s 4.1 page describes it as a constraint or placement key; the zone
  record is a cloud-discovered fact. The mismatch is why it is still on the
  old umbrella.
- **configuration** is a facet of three entities (three config tables).
  **metadata** covers the simplestreams format (external) plus a stored,
  declarable record (`cloud_image_metadata`).
- **hook** (970 lines) mixes the hook protocol (the execution stage's hand-off
  to the charm) with a catalogue of hook kinds and environment variables.
  Treat the protocol as a type 3 concept and the catalogue as type 11.

## Not covered by any page

Declarable things with tables in the schema and no reference page: model
migration (`model_migration_*`, `juju migrate`), secret backend (only inside
secret.md), block commands (`juju disable-command`), firewall rules, model
defaults. Whether they need pages is open.

## Fit with the 5a-5d draft

- The draft splits by topic; the types do not line up with it. 5a mixes
  executors, an instrument, an observation and one new entity (access). 5b
  mixes an executor, a substrate, processes and entities. 5c is nearly all
  type 1 and 2.
- Work differs by type: types 1-2 need ggarch models, raise-site checks and
  the ADR-016 restructure; types 3-11 need claim checks.
- Conflict with open PRs: jujud.md and the `(jujuagentd)=` label
  (#23427 vs #23438) still apply to type 3.
- ADR-016 renames the anchors `(x-declaration-rules)=`, `(x-persistence-rules)=`
  and `(x-execution-rules)=`. Other pages link to them (the watcher page links
  `machine-execution-rules`): stack each anchor on the place its content moves to.

## Rollout status (session 76)

ADR-016 is applied to all type 1 and 2 pages on the branch
`4.1-docs-entity-reference-layers` (worktree `~/git/misc/juju-entity-ref`, 25
commits on upstream/4.1 at 70591a13ec, unpushed): access, action, application,
bundle, charm, cloud, constraint, controller, credential, machine, model, offer,
placement-directive, relation, resource-charm, script, secret, space, ssh-key,
storage, subnet, unit, user and zone, plus the new watcher page. Types 3-11 are
untouched. Diagram fences are removed (see `fence-manifest.md`). The purged docs
build has no new warnings against the upstream/4.1 baseline.

## Status after session 78 (2026-10-19)

The page-structure work in session 78 (structure-discovery-plan.md: E7 to E10, the red team) concerns types 1 and 2 only. Findings that touch the other types: (1) the red team's misfits are types already named here: vocabulary and catalogue pages (constraint and placement-directive are listed as type 2 but behave as value catalogues; status, configuration and the hook list are types 8 and 11), mechanism pages (watcher, removing-things, scaling, HA, telemetry: types 4 and 9) and program pages (juju-cli, dashboard, jujuc: types 6 and 7); (2) the "form for entity pages" above is the layered ADR-016 form, which the plan proposes to replace with identity, interface, state, dynamics and the conditional agent and observation parts (theory v4, not ratified); (3) constraint and placement-directive should be re-examined as catalogue pages, not facet-honest entities; (4) `agent.md` (type 3) now only lists the agent types and points to the controller, machine and model pages, which own their agent.
