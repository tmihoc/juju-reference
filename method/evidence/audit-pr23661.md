# Audit of PR #23661 against its base (2026-11-05)

Refactor mode (`method/docs-decision-procedure.md`), base `e5db99d585`, head `48ef1fca17`. Source read with `git show` and `git grep` at the base; no live run. Scratch tools: `addr2.py` (labels, redirects, dangling `{ref}`) and `removed.py` (removed lines whose backticked terms or wording appear nowhere in the head corpus). Both live in the session scratchpad and are not committed.

## Coverage

| Level | Pages |
|---|---|
| Read and traced (removed statements classified, source checked where marked) | `metadata` (pilot), `secret`, `status` (figure), `high-availability` (figure), `manage-models`, `constraint`, `space`, `user`, `lease` (added, 1 spot check) |
| Screened (every removed line passed through `removed.py`, flagged lines read, rest unread) | `charm`, `relation`, `machine`, `storage`, `database`, `telemetry`, `resource-charm`, `action`, `application`, `cloud`, `model`, `credential`, `agent`, `unit`, `placement-directive`, `client`, `zone`, `offer`, `tutorial/index`, `agents/*` |
| Addresses | All of `docs/**/*.md` and `.rst` |
| Not done | Per-statement truth of the 15 added pages beyond one spot check; reference pages with 0 to 10 removed lines (`ssh-key`, `controller`, `hook`, `log`, `juju-db-repl`, `subnet`, `index`, `model-defaults` and others) read only through the screen |

## Addresses (step 5)

- 1,000 base labels; 13 are gone from the head and none is referenced by any head page: `juju-ssh-proxy-architecture`, `juju-ssh-kubernetes-vs-machines`, `juju-ssh-proxy-authentication`, `juju-ssh-proxy-availability`, `cloud-types`, `other-hooks`, `machines-and-units`, `machines-and-system-containers`, `machine-customisation`, `machine-base`, `non-peer-relation`, `non-subordinate-relation`, `secret-backend-configuration-options`. (A first pass said 39; 26 were indented labels the first regex missed.) The last one was removed from `manage-secret-backends.md` in the same PR.
- Four labels moved: `juju-ssh` to `reference/ssh-server`, `metadata` to `reference/image-metadata`, `secret-backend` to `reference/secret-backend`, `machine-designations` to `reference/placement-directive`. Both removed pages have redirects (`explanation/juju-ssh`, `reference/metadata`).
- 91 `{ref}` targets are not local labels; all but about ten are `tfjuju:` and `ops:` intersphinx targets. The remaining ones (`binding`, `command-reference`, `entity-concept`, `cloud-appendix-example-workflows`, the `controller-config-object-store-*` keys) also appear in the base and are pre-existing.
- Deleted images: `status.png`, `high-availability.png`, nine tutorial files. No head page references any of them.
- Unresolved: external deep links to the 13 lost anchors (Discourse, charm docs). Resolves with: a link check of canonical.com and charmhub against the 13 anchors.

## Verdicts per page

| Page | Verdict | Trace | Class |
|---|---|---|---|
| `reference/metadata.md` | **Restore, corrected** (pilot) | Product ID formats and index layout are nowhere in the head. 4.1 default index is `streams/<version>/index2` (`environs/simplestreams/simplestreams.go:333`); the agent product ID `com.ubuntu.juju:<os>:<arch>` appears in `environs/simplestreams/testing/testing.go:140`, production use not confirmed. The index lists both `{ref}metadata` and `{ref}image-metadata`, so the same page appears twice under Clouds. | Open(Q1) |
| `reference/secret.md` | **Keep.** 195 lines removed, all classified | Backend options moved to `secret-backend.md:76-90` and corrected: the old `mount-point` is `mount-path` in source (`internal/secrets/provider/vault/config.go:21`). The old "secret names must match `^([a-z](?:-?[a-z0-9]){2,})$`" was wrong: the regex validates content keys (`core/secrets/createsecret.go:21,110`); `secret.md:125` says so. User-secret hook behavior moved to `hook.md:450`. Worked name/URI/label examples dropped; the three identifiers are defined. | Determined |
| `reference/charm.md` | **Keep, trim accepted.** 155 removed | Every taxonomy term (principal, subordinate, sidecar, podspec, workloadless, configurator, proxy, integrator, infrastructure-agnostic, channel guardrail) is still on the page. Dropped: the `tiny-bash` example link. Labels moved inside the page. | Determined for the terms; the 16 flagged lines are reference rewording |
| `reference/relation.md` | **Do not restore (a); restore (b) and (c) only after a source check** (updated after cold run 3) | Cold run 3 shows (a) was false in upstream: `--controller-external-ips` and `--controller-external-name` are valid only for Kubernetes controllers and bootstrap fails for other clouds (`cmd/juju/commands/bootstrap.go:664-670`). The corrected fact belongs with the bootstrap configuration and the cross-model section for Kubernetes controllers. (b) interchangeable roles is contradicted by the next sentence and by the firewaller (claimed). Original audit text: **Restore two facts** | (a) The old page said that with a non-flat network the controllers must be bootstrapped with `--controller-external-ips` or `--controller-external-name`, set at bootstrap only; the head states it nowhere (those keys appear only in the generated `bootstrap.md`). (b) The old page said the offerer and saas roles are interchangeable with provider and requirer, and that ports open on the provider side; the head states neither. (c) `remote-<token>` naming of related applications on the offerer is gone. | (a) T4 gap, (b) and (c) Open: source check of firewaller direction and remote names not done |
| `reference/status.md` | **Fix.** Figure removed, no replacement | `status.png` drew application-status transitions. The drawn transitions are not enforced by code; the app status is derived from its units by severity: `error 100`, `blocked 90`, `maintenance 80`, `waiting 70`, `active 60`, `terminated 50`, `unknown 40` (`domain/status/service/status.go:544-552`). The head says "highest-priority" and defines it nowhere. The page's meta description still advertises "status transition diagrams". | Determined: add the severity order; drop the sentence from the description |
| `reference/high-availability.md` | **Keep** | `high-availability.png` replaced by the ggarch view `Controller high availability`. The old caption said "database replicaset" (MongoDB era); the new one says Dqlite and Raft. | Determined |
| `reference/constraint.md` | **Restore one fact, corrected** (updated after cold run 3) | Old: a constraint is a minimum on a machine or VM and a maximum on a system container or Kubernetes container. The old statement is itself partly false: on Kubernetes the same value becomes both a request and a limit (`internal/provider/kubernetes/application/constraints.go:331-345`), and the struct comments say "at least" (`core/constraints/constraints.go:61-70`). Restore the corrected rule, not the old sentence. Head: stated nowhere. Key descriptions were rewritten; `allocate-public-ip`, `ip-family` and the 4.1 key list are present. | Open: confirm the Kubernetes limit semantics in source |
| `howto/manage-models.md` | **Keep** | The three troubleshooting dropdowns became links to the reference error entries. Migration errors (owner, credential, machine sanity) are at `model.md:215-223`, updated for 4.1. The upgrade error "some agents have not upgraded to the current model version" and its `--ignore-agent-versions` remedy are obsolete: no Go code raises that message, and the flag is sent but no server code reads it (`git grep IgnoreAgentVersions e5db99d585`). | Determined |
| `reference/space.md` | **Keep.** Binding and `default-space` text moved to `application.md` and `space.md:167-168` | The `juju deploy --bind` and `juju bind` sentence is dropped; both commands have generated pages. | Determined |
| `reference/user.md` | **Keep; minor trims** | Dropped: "users are unrelated to client system users", "one user logged in at a time per client", the JAAS `everyone@external` note, "no overarching administrator". The client-side "one user at a time" is a client-store fact; not checked. | Determined for the trims; one Open |
| `reference/storage.md` | **Keep** | Directive grammar, defaults, `rootfs`, `loop`, `tmpfs` and the pool text all remain (`storage.md`, grep). Dropped: two reference links. | Determined |
| `reference/database.md` | **Keep** | Dqlite properties and the `controller` / `model-<name>` namespaces are on the page and in `architecture.md`. | Determined |
| `reference/machine.md` | **Keep** | Designations table moved to `placement-directive.md`; example sessions dropped (outputs from 3.x). | Determined |
| `reference/resource-charm.md`, `telemetry.md`, `action.md`, `application.md`, `cloud.md`, `model.md`, `credential.md`, `agent.md`, `unit.md`, `zone.md`, `offer.md`, `client.md` | **Keep (screened)** | Flagged lines are reference rewording or intra-doc link targets. Telemetry tracing keys (`sample_ratio`, `stack_traces`) now appear as the `sample-ratio` field and the tracing config call. | Determined for the lines read; the unread remainder is Open |
| `reference/ssh-server.md` and `explanation/juju-ssh.md` | **Keep the reference, delete the explanation** | `method/evidence/ssh-documentation-decision.md`. Redirect and `juju-ssh` label resolve. | Determined |
| `tutorial/index.md` | **Keep** | Nine files of excalidraw and SVG replaced by four ggarch views with captions and alt text. | Determined; figure acceptance is TODOS 7 |
| `docs/agents/*` | **Keep** | Rule text changed to match the pages (inline cloud definitions; the entity page form). `reuse/machine/cloud-definition.md` and `credential-definition.md` are now included by no page. | Determined; orphan snippets are Open |

## What the audit shows about the procedure

1. **Refactor mode works and found things the new pages cannot show.** Real losses: the relation and constraint facts, the status priority order. Real corrections it confirmed as right removals: `mount-point`, the name regex, the agent-version troubleshooting.
2. **Step 3 of refactor mode should be mechanized.** The screen in `removed.py` (backticked terms and wording absent from the head corpus) cut 3,600 removed lines to about 100 flagged ones and found every loss above except the status figure. Add it as the first pass.
3. **The procedure does not treat a removed figure as a set of statements.** The `status.png` loss was found by listing deleted files, not by the line diff. Add to step 1: a deleted or replaced image is read, its content stated as sentences, and each sentence classified.
4. **"Obsolete" needs a source citation every time**, and the audit supplied one in each of three cases. The rule stands.

## Defects found outside the PR's pages

- The generated CLI pages `upgrade-model.md:20` and `upgrade-controller.md:22` document `--ignore-agent-versions` ("Don't check if all agents have upgraded") although the server ignores it in 4.1. This is a source help-text question; the fix is in the Go source, not the docs.
- The reference index lists `{ref}metadata` and `{ref}image-metadata`, which are one page.

## Unresolved and what resolves each

| Item | Resolves with |
|---|---|
| Simplestreams layout restore (metadata) | Q1 decision; read `environs/tools/simplestreams.go` and `environs/simplestreams` for the 4.1 layout and agent product ID |
| Relation (a), (b), (c) | Source: `worker/firewaller` ingress direction for CMR; offerer-side remote application naming; controller external addresses in `api` info |
| Constraint min/max | Source: `internal/provider/kubernetes` resource limits from constraints |
| User "one user at a time" | `jujuclient` store semantics |
| 13 lost anchors | External link check |
| Added pages' truth | A per-page trace; the `lease` spot check passed (types `singular-controller`, `application-leadership`, `backup-creation` in `domain/schema/controller/sql/0002-lease.sql`). The error contract has its own per-call verification (TODOS 4) |
| Unread removed lines on pages with 0 flags | Read them; the screen only flags missing terms and wording, so a dropped statement phrased in common words passes it |
