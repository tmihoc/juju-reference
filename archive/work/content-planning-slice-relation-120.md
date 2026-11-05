# E69: relation, settings and execution context — focused planning slice

**Status:** Research proposal, not an approved page, skeleton, rule or generated
command edit. E69 was registered in `structure-discovery-plan.md` before new
source inspection. Source paths below refer to `/tmp/juju-41-tree` at the
established Juju 4.1 anchor `e5db99d585`. This is a bounded reuse and check of
previously investigated paths, not a held-out challenge.

## Verdict

**E69 passes its bounded behavioral and planning checks, with the explicitly
blocked command scope excluded.** Relation identity and participation, scoped
settings, hook-event metadata, command invocation and leadership conditions
are distinguishable on the traced paths. One home per fact is a proposed
maintenance policy, not a result proved by source: equally qualified linked
physical arrangements remain possible. In particular, E69 does **not** settle
whether leadership deserves its own page, prove reader benefit or complete any
individual hook-command reference. `HookCommandPages`, `WorkloadModel` and
`KubernetesCloudAttributes` remain 402-denied; none was relaunched or replaced.

## Evidence: participants, conditions and clocks

1. **Relation and scope.** `domain/relation/state/relation.go:80-111` infers
   two endpoint candidates, obtains a relation sequence ID and adds their
   relation in a transaction. This is a regular-add path, not the creation path
   for every relation type. Prior E51 (`work/endpoint-boundary-111.md:15-24`)
   separates charm declaration, application-specific endpoint/binding, and
   relation composition; it already exercised an endpoint helper, not a live
   deployment.
2. **Unit entry is its own state transition.** In `relation.go:1797-1856`,
   `EnterScope` checks for existing membership *before* retrieving the unit and
   checking its eligibility, then inserts membership and initial unit settings
   and invokes subordinate creation as applicable within the transaction. The
   code returns `RelationUnitAlreadyExists` first for an existing member; the
   alive check is not a universal first error. `:2045-2106` checks relation and
   unit are alive, that the unit's application participates, and applies an
   additional subordinate check on the two-application branch. This is a state
   path, not a demonstrated API error string or a live entry. A successful state
   transaction is not itself hook execution or proof of remote delivery.
3. **Settings have relation and participant scope.** Application settings are
   queried using relation UUID and application UUID through the relation endpoint
   (`relation.go:403-422`); unit settings are queried by unit name and relation
   UUID through relation-unit and endpoint (`:1604-1623`). The write SQL keys
   application settings by relation endpoint and key (`:2506-2529`) and unit
   settings by relation-unit and key (`:2579-2605`). Runner context separately
   holds unit and application settings for its relation (`internal/worker/uniter/
   runner/context/relation.go:42-73,96-134`). These paths distinguish the two
   relation-local kinds from ordinary application configuration; they do not
   establish every reader, authorization rule or cross-model propagation path.
4. **Local changes, commit and observation are different stages.** The relation
   context returns separate final unit and application settings
   (`context/relation.go:126-134`). The generic hook-context flush adds changed
   relation settings to a commit request and, if there are changes, calls
   `CommitHookChanges`, returning an error if the call fails (`context/context.go:
   1588-1608,1745-1760`). The relation-units watcher separately fetches and emits
   unit, application and departure change information (`apiserver/facades/agent/
   uniter/watcherrelationunit.go:65-101,104-139`). These separate paths do not
   establish their full ordering, every flush trigger, delivery guarantees or
   that a particular other unit runs a hook.
5. **Hook-event metadata is not the relation.** `internal/worker/uniter/hook/
   hook.go:81-99,121-123` validates different fields for different hook kinds:
   `relation-changed` accepts an application without a remote unit;
   `relation-joined` requires both remote unit and application; `relation-created`
   returns successfully without those fields. This is validation of `hook.Info`,
   not a complete hook-command context/availability matrix, a relation selector
   contract, or proof that any hook executes.
6. **Leadership is a separate condition.** The already-traced example
   `internal/worker/uniter/runner/jujuc/relation-set.go:163-183` checks
   `IsLeader` before selecting application settings, returning `cannot write
   relation settings` for a nonleader. This confirms only that local branch;
   it does not prove a universal leadership rule for all writes or all readers.
   The lease manager binds a claim to namespace and model and can deny a claim
   (`internal/worker/lease/manager.go:242-263,284-316,331-338`); a generic
   lease is not identical to application leadership. No election, expiry, lease
   loss or subsequent commit enforcement is established here.

## Executable smoke

A temporary Go program in the source-anchor module called the actual
`hook.Info.Validate` helper on synthetic inputs, then was removed:

```text
changed, no remote: "relation-changed" hook requires a remote unit or application
changed, application only: <nil>
joined, application only: "relation-joined" hook requires a remote unit
joined, unit and application: <nil>
created, no remote: <nil>
```

This demonstrates only the validator with these inputs; it does not launch an
agent, charm, hook, command, controller or database. It does not validate
relation IDs or prove that application-only contexts can arise in every model.

## A66 plans

**Terminology.** A *semantic address* is a linkable location for a contract;
its physical location may be a page or an anchored section. An *owner* below is
an editorial proposal to state the full scoped fact once, not an assertion that
the code uniquely determines a file. A *context* is the execution-specific
information used to interpret an event or invocation, not the identity of the
relation itself.

| Subject and reader-visible contract | Classification and proposed address/action | Conditional form and links | Open checks / do not claim |
|---|---|---|---|
| **Relation:** identity, endpoint composition, life and participant entry | Managed relationship with its own identity and lifecycle; maintain `relation` as the proposed page, not an application endpoint. | Definition/participants → identity/records → applicable streams → actors → create/enter/leave/read/write interactions and bounded errors. Link charm declaration, application endpoint, unit, offer and hook. | Full relation lifecycle, all entry cases, migration and cross-model propagation remain untraced; add path above does not prove peer creation. |
| **Relation settings:** application- and unit-scoped relation data | Relation-owned shared contract; proposed stable settings address within `relation`, with read/write interaction links. Not a separate generic application configuration contract. | Relation + participant scopes → distinct unit/application values → readers/writers and qualifying leadership checks → state/observation boundaries. Link application, unit, hook and relevant interfaces. | Trace complete read permissions, allowed keys, limits, concurrent changes and commit/propagation paths before making comprehensive claims. The known scoped SQL alone is not the whole contract. |
| **Hook-event context:** data attached to a particular hook | Execution/event context, proposed under `hook` with links from `hook-command` and relation-specific hooks. | Event kind → available/required event fields where traced → agent execution/observation limits. Link relation identity and execution interface. | `Info.Validate` is only one validation layer; it neither proves command availability nor covers actions or every hook. |
| **Hook-command interface:** command execution in a unit context | Shared tool/interface, proposed `hook-command` address; link hook/action context and affected subjects. | Execution environment and command dispatch → known shared context contracts → links to command entries and target semantics. | Keep per-command applicability, errors and selection unclaimed until derived; family registration does not prove success. Hook-event metadata and command execution context overlap but are not interchangeable. |
| **Application leadership:** leader-dependent behavior across relations and other consumers | Shared coordination concept; propose a linkable leadership address associated with application/unit and linked to `lease`, with an unresolved page-versus-section tie. | Identity and scope → how leadership is observed/held when traced → consumer-specific guards and failures. | The bounded lease trace is not proof of election algorithm, timing, global exclusivity or all consumer rules. The physical address and full contract require investigation. |
| **`relation-set`:** invocation capable of changing relation settings | Generated command/interface entry, **partial and blocked**. Proposed command address owns syntax and command-local context/validation; it links semantic relation settings and leadership. | An invocation plan is only a placeholder for future evidence: target/context, inputs, local result/errors and subject links. | Reuse only the recorded application-settings leadership example. No individual command derivation, full context matrix, option precedence, error enumeration, flush timing or generated-publication solution is claimed. |

## Combined checks

### Semantic ownership and entry points

The proposed division has one **full-statement home per named fact**, with links
from other relevant entries: relation composition and membership at `relation`;
relation participant settings at its settings address; event-kind validation at
`hook`; shared invocation context at `hook-command`; general application
leadership at its as-yet-unlocated leadership address; and the traced nonleader
command refusal at the individual command interaction. The last has a partial
address, not a completed contract. Claiming that the command gate alone is the
platform's full authorization rule would conflate layers; making the command the
only home for relation data semantics would make the semantic page client-specific.

Every named entry point has either a proposed semantic address or an explicit
unresolved physical location/blocked command scope. This is a routing plan, not
a check that a deployed documentation anchor or generated link already exists.
The leadership address and generated publication mechanism are open.

### Errors and diagrams

- The already-in-scope result and alive/membership failures belong to the
  **entry interaction**, with API representation checked before publication;
  their precedence must not be lost in a generic error bucket.
- Hook-event validation failures belong to the **event validation interaction**;
  they are not established user-facing hook-command error messages. The
  previously traced nonleader refusal belongs to the **command-local branch**;
  commit, lease and remote failures require separate traces.
- A relation/endpoint/unit/settings diagram belongs with the relation's
  **structure**. An entry-to-observation sequence, if warranted and fully
  traced, belongs with the relevant **interaction/dynamics** and must distinguish
  state commit, watcher event and hook execution. A hook context diagram belongs
  with **execution context**. Existing figures and anchors are not changed.

### Equal-facts alternatives and algorithm limit

Take the same fully qualified settings-scope statement and the same two incoming
links from an application and the command interface. Alternative A places it in a
`relation` section; B places it in a standalone relation-settings page. Both
retain one copy and two links, and both can express the participant and context
conditions; B introduces a separate page. Source distinguishes the contracts
but cannot choose between these files. This is an editorial tie, not a measured
reader-performance result. Similarly, one copy with links and two qualified
copies can express the same fact, though they have different maintenance costs;
unique semantic ownership is a policy rather than a logical consequence.

A66 usefully exposes the distinction but its character/leg criteria have no
source-derived threshold for when a separate file is mandatory. The model slice's
"no duplicate owner" pass therefore verifies that its *proposed assignment*
is consistent, not that source proves one unique owner or that a link actually
exists. This is a qualification to the candidate algorithm, not authorization to
change the global skeleton or documentation rules.

## Preregistered results and limitations

| E69 prediction/check | Result | Basis |
|---|---|---|
| Settings are scoped to relation and participant, not ordinary application configuration | Supported on named paths | Relation/app and relation/unit query predicates and scoped writes; no complete authorization audit. |
| Event context differs from relation identity | Supported, bounded | Separate `Info` validation branches and relation composition; probe exercises only the validator, not a full interface. |
| Scope entry is not itself hook execution or remote delivery | Supported, bounded | State transaction and separate watcher/flush paths; no live controller or remote observer. |
| Plans preserve contracts, conditions and clocks; errors/diagrams retain homes | Supported as a plan | Table and routing checks above, subject to explicitly blocked command details and untraced commit/delivery paths. |
| Physical location uniquely follows from code | Not predicted; unresolved | Equal-facts alternatives above preserve the same scoped statement and links. |

No negative finding here asserts that an untraced behavior is absent. No docs
page, generated output, source implementation, rule, PR link or selected error
counter was changed. A full relation-set or other hook-command derivation remains
blocked, as do the two other named 402 scopes.
