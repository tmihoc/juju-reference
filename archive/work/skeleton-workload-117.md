# Proposed workload and relationship skeletons — session 117

**Proposal, not approved documentation.** Source paths are relative to `/tmp/juju-41-tree` at `e5db99d585`; prior `work/` artifacts supply source-traced evidence at that same anchor. The proposed section titles below are reviewable examples, not mandatory headings or a claim that every current statement is correct. Ordered sections follow the settled causal order: definition; applicable records; streams; actors; interactions; configuration and failure index where applicable. A vocabulary prerequisite can precede the records that use it. Migration exceptions link the process where relevant. `Verify` marks an unresolved question, not a statement to publish. Source traces are not live controller, charm or cloud evidence. No page, anchor or repository rule has been changed.

The exact home of each shared contract is a proposed stable semantic address (a link target, not necessarily a new file). Current files are compared only after the behavioral boundary has been derived. For each interaction, preserve caller, prerequisites, effects, per-call errors and asynchronous limitations in its own call subsection; a skeleton is not an exhaustive API or error inventory.

## action

**Subject and boundary.** A charm-declared named action is invoked for units of an application; it is distinct from the resulting operation and per-target tasks. The exec path creates the same kind of run records without being a charm action. `domain/deployment/charm/actions.go:16-122`; `apiserver/facades/client/action/operation.go:32-98,241-261`.

1. **Action definition and scope** — name, declaration/parameters; link charm declaration, application and unit.
2. **Action declaration records** — show relevant model records and invariants for the declaration; link the shared operation/task records rather than defining a second owner. Verify the record and its actual inspector relevance before moving the existing figure.
3. **Action interactions** — listing definitions; running an action; action-context commands and results. For the traced enqueue path, model-write authorization and same-application target checking precede enqueue; accepted task IDs are not completion. Link shared task inspection, cancel and logs rather than describing their entire generic contract here.
4. **Action-specific configuration and failures**, only where the declared action actually supplies it; link shared task status/output to `script` and its object store to `object-store`. Preserve action-specific errors at calls.
5. **Migration** — link shared operation/task migration exception from `script` rather than duplicate it; verify the action declaration's own migration exceptions.

**Comparison/change.** `action.md:20-60` currently carries generic operation/task records and streams. Propose their shared home at existing neutral `script` task/operation anchors, preserving incoming anchors and figures; action-specific views can link to them. This is a proposed relocation, not proof that a file move improves findability. Verify all existing incoming references, version-specific watcher behavior and per-call error placement before any edit.

## annotation

**Subject and boundary.** Annotation is entity-targeted metadata; neither the target's lifecycle nor the generic access grant. `apiserver/facades/client/annotations/annotations.go:46-96,103-136` demonstrates separately authorized get/set paths.

1. **Annotation and targets** — what a key/value annotation describes, model scope and links to annotated subjects; verify the complete supported target set before naming it.
2. **Annotation records** — target association and stored values, if relevant to supported database inspection; verify individual schema invariants.
3. **Annotation change streams** — include only after a supported holder and payload are traced; otherwise omit, without claiming no watcher exists.
4. **Annotation calls** — read and set, preserving the distinct model-read/model-write checks and per-entity handling. The traced `Get` returns results independently; do not assume `Set` returns the same result shape (`annotations.go:57-96`).
5. **Migration** — include only a traced exception; otherwise link the generic process.

**Boundary.** A single shared annotation contract links to subject-specific targets. Complete target eligibility and deletion/migration coupling are open.

## application

**Subject and boundary.** A model's application realizes a charm; its units and application endpoint realizations vary separately. Charm owns endpoint declarations, application owns its realizations/bindings and exposure, relation owns composition (`work/endpoint-boundary-111.md:5-24`).

1. **Application and endpoints** — application identity and model/charm relationships; define realized endpoints, bindings and the trust setting as application-scoped concepts, linking charm declarations and relation composition.
2. **Application records** — the application, its selected charm, endpoint/binding and settings records needed by an inspector; link unit, relation and storage records rather than reproducing their contracts. Verify each invariant and the contents of existing diagrams before relocation.
3. **Application change streams** — identify actual holders, watched changes and delivery only where individually traced; do not assert a stream for every setting.
4. **Application actors** — unit agent and, on the traced Kubernetes path, application provisioner; distinguish desired state from provider-applied state (`work/held-out-115.md`, trust case).
5. **Application calls** — deploy/read; configure and trust; bind/expose endpoints; refresh; add or remove units/application. `AddUnits` rejects CAAS on the traced path (`apiserver/facades/client/application/addunit.go:23-47`); do not generalize that to all scaling paths. Successful trust-setting storage is not proof a provider applied roles (`system-model-115.md:17`). Put per-call permissions, outcomes and failures here.
6. **Application configuration** — actual application values versus charm option declarations; link shared settings vocabulary and key-specific contracts. **Migration** links the process and any verified application-specific exception.

**Open.** A documented refresh scope rule may be too strict, but only a helper and partial refresh path were exercised (`endpoint-boundary-111.md:38-40`); do not claim a complete reverse-scope success. Exposure/provider and full update-status semantics are not proven.

## charm

**Subject and boundary.** A reusable charm contains declarations and executable logic; its endpoint declaration can be realized by multiple applications (`domain/deployment/charm/meta.go:195-204`; `work/endpoint-boundary-111.md:15-24`).

1. **Charm and declaration vocabulary** — identify archive/revision and declared options, relations, actions, resources and storage; link each separately addressable behavior. The charm declaration is not an application binding or a relation.
2. **Charm records** — relevant archive/declaration records, references and enforced invariants; verify per-record coverage and deletion scope before moving figures.
3. **Charm change streams** — include only a source-traced holder and observable payload; absence is not proven.
4. **Charm interactions** — acquiring/using a charm, refresh/replacement and removal as supported; retain conditions and result with the traced call, link application refresh and resource fetching. Verify lifecycle and all supported acquisition paths.
5. **Declared configuration and related contracts** — link application-specific values and trust, actions, resource and storage declarations; do not equate provider-specific behavior with arbitrary charm code. **Migration** only for a verified charm-specific exception.

## resource-charm

**Subject and boundary.** A charm resource's declared identity/content and application/unit fetch paths are distinct from compute resources and persistent storage (`apiserver/apiserver.go:895-916,971-985,1122-1134`).

1. **Charm resource and scope** — declaration, application/unit use, relationship to charm and object storage; distinguish it from a cloud resource or storage pool.
2. **Resource records** — relevant declared, application/unit and stored-content associations and enforced invariants; verify revision/content rules against the relevant resource source before publishing.
3. **Resource change streams and actors** — include only source-traced change deliveries; distinguish authenticated unit/application fetch actors and client upload where applicable.
4. **Resource interactions** — upload, fetch and inspect on supported paths, with distinct per-path auth and result, then cleanup/removal only when a reachable operation is traced. Link charm, application/unit and object store.
5. **Migration exception** — include only after verifying which data and stored objects move.

## offer

**Subject and boundary.** An offer publishes selected application endpoints for consumption by other models; an offer is not the consumer-side relation or the external controller connection (`cmd/juju/crossmodel/offer.go:55-83`; `work/subject-map-112.md:29-31`).

1. **Offer and participants** — source model/application endpoints, offer identity and consuming-model relationship; link application endpoint, relation and external controller.
2. **Offer records and access** — relevant offered endpoint and permission associations; per-target access vocabulary links to user/access rather than copied general grant rules. Verify record invariants.
3. **Offer change streams and actors** — include supported holder/payload only after tracing the exact path; no blanket remote delivery guarantee.
4. **Offer calls** — create and inspect; set/revoke access; consume and remove, each with proven caller, conditions and result. Do not carry a source registration as a completed behavior or generalize remote failure conditions.
5. **Cross-model consequences and migration** — link relation-specific ingress and external-controller handling; remote propagation and provider reachability remain unverified.

**Open.** Full consume and offer-removal authorization/lifecycle have not been audited; do not promise all offers disappear or all related applications are blocked on removal.

## relation

**Subject and boundary.** A relation composes participant application endpoints and has participant-specific unit/application data; neither a charm endpoint declaration nor an application binding is the relation (`domain/relation/state/relation.go:80-111,2045-2098`; `work/endpoint-boundary-111.md`).

1. **Relation and participants** — endpoint matching, scope and participant identity; link charm declarations, application realizations and offers for cross-model use.
2. **Relation records** — relation, endpoint and participant scope/settings records and proven invariants; application and unit data bags are distinct. Verify the existing record diagram against source before moving or changing it.
3. **Relation change streams** — relation-unit payload for the actually traced watcher (`apiserver/facades/agent/uniter/watcherrelationunit.go:104-139`); do not infer delivery of every update or ordering from its existence.
4. **Relation actors** — unit agent and hook context; lead into hook execution without asserting all hooks are watcher-driven.
5. **Relation interactions** — create/match and remove; unit entry/exit; read/write participant settings. Entry checks alive relation, alive unit and application membership; `relation-set` application data requires leadership (`domain/relation/state/relation.go:2045-2098`; `internal/worker/uniter/runner/jujuc/relation-set.go:163-200`). Add relation-specific cross-model ingress conditions as separately linked behavior, not a guarantee of firewall application (`domain/crossmodelrelation/service/relation_network.go:57-74,96-116`).
6. **Migration** — link the process and state only proven relation exceptions.

**Open.** Full propagation, provider firewall application and all relation lifecycle/errors remain unverified.

## secret

**Subject and boundary.** A secret has a model-scoped identity and revisions; the backend stores content and varies separately. URI/label references are used across calls, not merely in a database record (`domain/secret/service/service.go:268-321`; `work/surface-probe-111.md:26-30`).

1. **Secret and references** — define URI, name and label as shared vocabulary before any caller uses them; preserve the existing URI/name/label anchors. Link revisions and secret backend, not cloud credentials.
2. **Secret records** — relevant secret/revision and backend references, grants and enforced invariants; distinguish content storage from metadata. Verify migration and retention rules before publishing.
3. **Secret change streams** — list only actual supported watcher/holder and payload paths after tracing; no blanket delivery claim.
4. **Secret actors** — user client versus charm/agent where separately supported; distinguish permissions and secret ownership.
5. **Secret calls** — create/list; update; grant/revoke; remove. Put selector rules and errors at each call: the traced v2 update validates exactly one URI or existing label, while remove and grant/revoke choose URI first when both supplied; missing selector results have different scopes (`work/surface-probe-111.md:17-30`). Backend fallback or failure is conditional, not guaranteed remote availability.
6. **Migration** — link process and only verified secret-specific exceptions.

**Pending edit.** Relocate shared vocabulary out of a storage-only context; exact heading and anchor preservation require review. Verify missing-selector removal error before adding it; do not extrapolate the six-method client v2 slice to all secret surfaces.

## secret-backend

**Subject and boundary.** Backend configuration and availability vary independently of a secret's identity and revision; creation of a user secret tries the configured backend with a local fallback only for the traced not-supported result (`domain/secret/service/service.go:296-321`; `apiserver/facades/client/secretbackends/secrets.go:35-58,171-184`).

1. **Secret backend and model selection** — backend identity/configuration, relation to model and secret metadata/content; link `secret`.
2. **Backend records** — relevant configuration and model references for inspection, excluding unsupported claims about external backend durability.
3. **Backend change streams and actors** — include a supported holder and payload only when proven; distinguish operator configuration and background use.
4. **Backend calls** — add/list/update/remove/select where actually traced; keep type/provider-dependent validation and errors per interaction. State fallback only under its actual not-supported condition.
5. **Backend-specific configuration and migration** — link key-specific schemas; describe drain/removal and migration only after tracing conditions. Do not imply unconditional migration success or remote cleanup.

## unit

**Subject and boundary.** A unit belongs to an application but has its own lifetime, agent execution, relations and attachments. Removing a unit and its application are distinct paths (`domain/removal/service/unit.go:85-125`; `domain/removal/service/application.go:86-130`).

1. **Unit and application** — identity, membership, machine/CAAS context as applicable; link application, machine, charm and status.
2. **Unit records** — relevant life, state and associations; link relation participation, storage attachment and tasks rather than duplicating their full contracts. Verify platform-specific invariants.
3. **Unit change streams** — name holders and delivered data only for traced paths; a relation-units watcher is not a universal hook trigger.
4. **Unit actor** — unit agent executes hooks with context; link the hook mechanism and charm-supplied code (`internal/worker/uniter/runner/runner.go:320-344,381-388,546-561`).
5. **Unit interactions** — create/add, inspect, remove; action and storage attachment interactions link their own contracts. Apply IAAS/CAAS conditions per actual path and separate request acceptance from eventual job completion.
6. **Configuration and failure indexing** — link application configuration, unit status and hook/action error contracts without promising a universal failure state or timing. **Migration** links the process and verified unit-specific exception.

## Comparison with current pages, after derivation

These are comparison leads, not source evidence or a deletion list. An existing operation, stream, record, migration detail, diagram or anchor omitted from an outline must be traced and assigned before rollout; its omission here does not show it is absent or false.

| Page | Existing material and proposed treatment |
|---|---|
| `action.md:20-60,124-334` | Generic run records, streams, command execution, task/operation inspection and pruning currently share the action page. The common mechanism home under `script` is proposed; preserve and reconcile every action/task anchor, status diagram and untraced call before moving anything. |
| `annotation.md:13-64` | Schema, set/read and migration already have addresses. Retain the distinct read/write contract; key-deletion semantics, all targets and migration must be source-checked before carrying their detailed text forward. |
| `application.md:17-185,196-490` | Schema and calls cover identity, config, endpoints, exposure, scale and agent interactions. The endpoint split and trust path support the proposed chunks, but do not prove all figure, watcher, refresh or status claims. Preserve the endpoint anchor and trace those details. |
| `charm.md:17-167,170-422` | Schema, pending-charm stream and resolve/add/upload/download/reserve/remove/migrate calls contain more than the bounded declaration trace. Keep their addresses for review; do not omit their contracts or assume the trace validates them. |
| `resource-charm.md:17-77,80-296` | Schema, streams, activation, fetch, polling, removal and migration extend beyond the traced HTTP authorization paths. Reconcile each path before relocation; distinguish resource content from generic object storage. |
| `offer.md:17-56,68-275` | Current offer watcher, create/list/find/access/consume/remove and migration claims exceed the bounded offer/declaration trace. Preserve them pending specific authorization, lifetime and propagation checks. |
| `relation.md:17-93,96-348` | Current composition, streams, data bags, status, lookup and migration are more detailed than the selected entry/settings/ingress traces. Keep their distinct anchors and source-check each operation and delivery before choosing changes. |
| `secret.md:17-108,111-320` | Shared reference vocabulary is currently in the schema; propose a separately linkable vocabulary home with preserved anchors. Rotation, agent/charm paths and migration still require individual traces; the client-v2 selector result does not prove them. |
| `secret-backend.md:17-60,63-200` | Schema, backend/model watchers, configuration and migration require evidence beyond the bounded separate-backend and secret-write paths. Keep those sections pending verification rather than deducing absence. |
| `unit.md:17-101,104-419` | Existing streams and client/agent interactions include leadership, resolved markers, status, version, unit state and migration. Their complete contracts are not established by unit-removal and runner traces; keep their addresses for review. |
