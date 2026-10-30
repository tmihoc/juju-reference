# PR #23661 title and description (sessions 86–105, 2026-10-30). Paste the fenced blocks. Base 4.1. Restructured in session 93: no per-page table — first principles (Why), the reader, the totals, and the comma-separated preview links. Refreshed in session 105 for the work of sessions 103-105. Refresh the counts (tools/count_errors.py, from this file's links line) whenever the pages change.

Title:

```
docs(reference): rewrite the entity reference pages from the 4.1 code, with diagrams
```

Description:

```
Epic: JUJU-9635. This draft is the reference rework of JUJU-10585, the first increment of the error lists of JUJU-10586, and it delivers the diagrams JUJU-9635 set out to add. Merge before 4.1.

## Why

The illustration epic assumed the pages around the diagrams were good and that new diagrams would have a natural home. Neither held: drawing from the 4.1 code showed the pages were incomplete or wrong (the SSH key page said keys are placed on machines after bootstrap; the model page had no operations, errors, or access rules; the cloud page did not say which clouds can be added to which controllers). So the pages were reworked from first principles — one recipe, every claim traced to file:line — and the diagrams then had somewhere to live.

## The form

Each entity page follows one paradigm: a lede that defines the thing; a simplified database schema of the records the controller and model databases keep, drawn as a diagram; the change streams a client or agent can watch; one section per call with its `Caller:` line — a client acting for a user, with that user's access level, or an agent acting for its own machine or unit — the rules, and the client-visible errors; and what a model migration does to the entity. Sections appear only when the entity has facts for them. Each schema figure hosts its own section, and its caption carries how to read the figure and what follows from its shape. The pages are client agnostic: the platform fact comes first, and a CLI or Terraform command appears only as an example.
The paradigm decides the set: a reference page is reworked when it documents a controller API surface or defines a term a `Caller:` line cites; the list pages (supported clouds, CLI commands, hook commands, configuration keys) and the binary and tool pages (`jujuagentd`, `containeragent`, `jujuc`, Pebble, the dashboard) keep their own forms. This first increment covers the 35 entity pages linked below and the agent, client, and watcher concept pages, which the `Caller:` grammar and the change-stream sections cite.

## The reader

These pages are written to be acted on, by a person or by the AI agent of one: one fact has one home, every term is linked at first mention, the statuses are enumerated, each figure's alt text carries every fact it shows, and every error is the exact string a client sees, with its code, its trigger, and its remediation. An operator's agent can match live `juju` output to a documented error and answer with its remediation. Every claim was traced to the 4.1 code at file:line while the pages were written and reviewed, so the reader can trust each without reading the source.

## What this PR adds

- 38 reference pages: 26 reworked from the old prose (the agent and client concept pages among them), 12 new (SSH server, external controller, object store, link-layer device, controller upgrade, agent version, lease, model defaults, image metadata, model migration, annotation, watcher; telemetry was reworked around its records).
- 49 figures on the reference pages (57 with the tutorial and architecture pages), rendered from one model: `docs/juju.ggarch` holds a single ggarch model with 71 views — 45 database-schema diagrams, 22 sequences, 4 state machines — over the 224 records of both databases (full DDL fields) and the nodes, edges, and behaviours of every page. Merging the per-page schemas into the one model also canonicalized the record names: the page that owns a record names it (`Charm resource`, `Stored object`, `File store`, `Permission`, `Export`), with ten pages' captions and figure texts aligned; and every figure was pixel-diffed across the merge — only those intended renames changed. The last step merged the remaining 14 models into one: the six ids that an architecture entity and a database record shared (user, cloud, controller, model, application, charm) now name the entities `arch_user`, `arch_cloud`, and so on, and all 142 renders (light and dark of every view) are identical before and after.
- The client-visible error contract, first increment: 956 error entries — 674 distinct messages — each an error that the 4.1 code raises for a client, with the exact message, its error code, the trigger, and the remediation, each entry traced to the 4.1 source at file:line during drafting and review (182 of the 204 calls on 33 pages carry them). Every entry was traced to the code, never carried over from the earlier docs, and every page entry was re-checked against the upstream 4.1 tree: the count is of the documented 4.1 contract, and the pages keep no entry that the 4.1 code does not raise. This is the substance of JUJU-10586, and the CI check that keeps it true is part of this PR: `scripts/check_error_contract.py` re-extracts every documented message and code from the Go source and its pinned `github.com/juju/*` dependencies and fails the docs build when either side drifts (a short, reasoned exclusion list lives in the script).
- All 34 entity pages and the agent, client, and watcher concept pages were reviewed against the code by an independent reader; every finding was verified against the code before it was applied, and four were rejected with evidence (the storage tombstone gloss, the telemetry field name, the Terraform line for model defaults, and the log-transfer single-record rule). The reviews found 2 to 30 problems per page, concentrated in the error texts (missing wrap segments, wrong HTTP statuses, wrong codes) — all fixed here. Two of the last seven reviews ran in the main session after the review agents failed with provider credit errors.
- Tooling: `docs/requirements.txt` pins `tmihoc/ggarch@b9eb04d` (the `hide-fields` branch) — the commit that adds the `context:` select item, which lets one record model serve every page: each view marks the records another page owns with `context:` and excludes with `except:` the edges its page never drew. Rendered SVGs are not committed.
- The cross-page density pass: the duplicate facts that the pages restated were swept, so each fact keeps one home and every other page links it (24 recorded no-link sentences gained their links in the first linking commit, and 12 more on the six last unswept pages in the second — every entity page is now swept); and the agent page gained a per-facade map of which agent kinds each facade serves, derived from the 4.1 facade constructors.
- The inclusion rule and the paradigm (`docs/agents`): a fact stays on a reference page only if it is true against the code, a reader can meet it (a command's output, an API reply, a status, a log line, or the database through the supported tools), and a named reader asks a question that page owns. `AGENTS.documentation.rules.md` now states the whole paradigm once: the charter, the audiences, the entity page form, the call contract, the figure rules, and the mechanical checks. Applying it, the model page dropped the migration records and the model migration page now leads with its state machine; the 19 change-streams openers say that a change stream is the changes the holders follow, which the watcher page owns; each "the database refuses" claim was audited against the code and the release DDL, and the external-model refusal moved to the call that raises it. The pages also follow two style rules: ` -- ` for the em dash in prose, and no version scoping of any kind (the `versionadded` directives are gone).

## The pages

Preview: [Action](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/action/), [Agent version](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/agent-version/), [Annotation](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/annotation/), [Application](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/application/), [Charm](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/charm/), [Charm resource](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/resource-charm/), [Cloud](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/cloud/), [Constraint](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/constraint/), [Controller](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/controller/), [Controller upgrade](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/controller-upgrade/), [Credential](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/credential/), [Database](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/database/), [External controller](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/external-controller/), [High availability](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/high-availability/), [Image metadata](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/image-metadata/), [Lease](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/lease/), [Link-layer device](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/link-layer-device/), [Machine](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/machine/), [Model](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/model/), [Model defaults](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/model-defaults/), [Model migration](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/model-migration/), [Object store](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/object-store/), [Offer](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/offer/), [Relation](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/relation/), [Secret](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/secret/), [Secret backend](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/secret-backend/), [Space](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/space/), [SSH key](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/ssh-key/), [SSH server](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/ssh-server/), [Storage](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/storage/), [Subnet](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/subnet/), [Telemetry](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/telemetry/), [Unit](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/unit/), [User](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/user/), [Zone](https://canonical-juju-1--23661.com.readthedocs.build/23661/reference/zone/).

## Please check

- Use the Read the Docs preview, not the GitHub diff: the figures render only there. Check them in light and dark mode.
- **Not verified by running:** every error text, code, and access level was read from the code, not run. In particular the block definitions, the Kubernetes session identity, the migration status strings, the upgrade dry run, the control-socket endpoints, the lease claim and expiry, and the object-store drain timeouts.
- **Questions for the Juju developers:**
  - `ImportKeys` checks that the caller can write the model, then imports keys for the user named in the call: a model admin can import keys for any existing user. Intended?
  - The `AgentLifeFlag` facade denies only a login that is an application agent and not a unit agent (`lifeflag/facade.go:62`), so machine and model logins pass, and a model agent can read an application's life flag. Intended?
  - A login as an application exists on Kubernetes (the application provisioner sets the password, `caasapplicationprovisioner/worker.go:171`), but no `containeragent` subcommand for it was found. Who logs in with it?
  - Creating a machine: `machinemanager.go:179` compares a placement directive with the model UUID, so a provider directive such as `zone=x` fails there.
  - A revoke sets the level just below the one named, whatever the user holds. Revoking admin from a user who has only read sets write. Intended?
  - The object store claims a lease in the namespace `object-store`, but `lease_type` has no such row, and the insert selects the type with no error on no match, so the claim is never persisted (`core/lease/interface.go:22`, `domain/lease/state/state.go:125-131`). Add the type or drop the claim?
  - The how-to and the code disagree in three places: removing an offer (offer admin or model admin), removing an offered application (blocked or its offers deleted), and who may write user secrets (admin or write access).

## Checklist

- [x] Code style: imports ordered, good names, simple structure, etc
- [x] Comments saying why design decisions are made
- ~Go unit tests, with comments saying what you're testing~
- ~[Integration tests](https://github.com/juju/juju/tree/main/tests), with comments saying what you're testing~
- ~[doc.go](https://discourse.charmhub.io/t/readme-in-packages/451) added or updated in changed packages~

## QA steps

1. Open the preview links above and check the figures.
2. From `docs/`: `ggarch check juju.ggarch` (1 model, 71 views), then build `dirhtml` and `latex`. Both pass, with only the two pre-existing duplicate-target warnings under `latex`.

## Documentation changes

Docs only; no API or CLI behavior changes.

## Links

**Jira cards:** [JUJU-9635](https://warthogs.atlassian.net/browse/JUJU-9635) (illustrate the docs), [JUJU-10585](https://warthogs.atlassian.net/browse/JUJU-10585) (rework the reference content from first principles), [JUJU-10586](https://warthogs.atlassian.net/browse/JUJU-10586) (error lists in the reference docs), [JUJU-10580](https://warthogs.atlassian.net/browse/JUJU-10580) (dissolve the contributor tree)

[JUJU-9635]: https://warthogs.atlassian.net/browse/JUJU-9635?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ
```
