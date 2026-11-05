# Trace: every statement of draft-relation.md to the 4.1 source (commit 52e983a435)

Paths are relative to the repository root. "UP" means an upstream doc statement at the same commit. Verdicts: **S** source-verified, **U** upstream statement kept (no source contradicts it, source cannot prove it), **I** inference stated in the note, **G** gap recorded in notes.md (statement avoided or hedged). No statement is Unverifiable and kept as fact; those were dropped (listed at the end).

## Lede and front matter

| Id | Draft statement | Evidence | Verdict |
|---|---|---|---|
| L1 | A relation connects two endpoints of two different applications | domain/relation/types.go:227-232 (`CanRelateTo` requires different `ApplicationName`); core/relation/key.go:32-44 (a key has two endpoint identifiers) | S |
| L2 | ... or an application to itself through a `peers` endpoint | core/relation/key.go:32-37 (one endpoint with role Peer); domain/schema/model/sql/0024-relation.sql:59-63 | S |
| L3 | Operator creates a relation with the integrate operation | apiserver/facades/client/application/application.go:1416-1459 (`AddRelation`); docs/howto/manage-relations.md:20-23 (UP) | S |
| L4 | ... and needs write access to the model | application.go:1417 and 271-273 (`checkCanWrite` is `WriteAccess`) | S |
| L5 | Juju creates the relation of an application to itself when it creates the application | domain/application/state/application.go:379-381; domain/application/state/peer_relation.go:55-73 | S |
| L6 | description meta | Same facts as sections below | S |

## Peer relation

| Id | Statement | Evidence | Verdict |
|---|---|---|---|
| P1 | A peer relation is a relation an application has to itself; one endpoint, role `peers` | key.go:32-37; 0024-relation.sql:59-63; peer_relation.go:21-49 (selects endpoints with role `peer`) | S |
| P2 | One peer relation per `peers` endpoint at application creation | peer_relation.go:55-73 (loop over peer endpoints); application.go:379-381 | S |
| P3 | IDs assigned in alphabetical order of endpoint names | peer_relation.go:36 (`ORDER BY cr.name`, comment "alphabetical order") | S |
| P4 | The remove operation refuses to remove a peer relation | domain/relation/service/relation.go:1059-1062 ("Peer relations cannot be removed by an end user"), 1091-1097 (`cannot remove a peer relation`); by endpoints, `InferRelationUUIDByEndpoints` selects only regular relations (domain/relation/state/relation.go:194-209) | S |
| P5 | Charm authors use application settings of a peer relation to store shared data | docs/howto/upgrade-your-juju-deployment-from-36-to-41.md:94 (UP: "store shared data in the peer relation application databag") | U |

## Non-peer relation

| Id | Statement | Evidence | Verdict |
|---|---|---|---|
| N1 | Between two different applications; one endpoint `provides`, the other `requires`; same interface | types.go:227-232; types.go:203-213 (`CounterpartRole`) | S |
| N2 | Scope is `global` or `container` | core: domain/deployment/charm/meta.go:37-38; 0024-relation.sql:90-94 | S |
| N3 | Scope is `container` when at least one endpoint is container-scoped, `global` otherwise | domain/relation/state/relation.go:292-300; 0024-relation.sql:90-93 | S |

## Subordinate relation

| Id | Statement | Evidence | Verdict |
|---|---|---|---|
| S1 | A subordinate relation is a non-peer relation with scope `container` | relation.go:292-300; domain/relation/state/subordinateunit.go:50-57 (units are created only when the scope is container) | S (definition chosen from the enforced discriminator; see finding F7) |
| S2 | At least one of its applications is a subordinate | relation.go:3714-3717 (container endpoints are skipped unless one application is a subordinate) | S |
| S3 | When a unit of the other application enters scope, Juju creates a unit of the subordinate application on that unit's machine | subordinateunit.go:43-122 (`addSubordinateUnit`: resolves the principal unit and its machine, calls `InsertIAASUnit`); apiserver/facades/agent/uniter/service.go:470-477 (`EnterScope`) | S |
| S4 | No second subordinate unit for a unit that already has one | subordinateunit.go:67-70 ("No subordinate unit is created if one already exists for the resolved principal") | S |
| S5 | So no unit until the first such unit enters, then one per unit of the other application | follows from S3, S4; docs/reference/charm.md:112 (UP: no units at deploy) | I |
| S6 | Link to the subordinate charm | docs/reference/charm.md:107 (label `subordinate-charm`) | S |
| S7 | A subordinate charm declares at least one `requires` endpoint with scope `container` | domain/deployment/charm/meta.go:777-793 | S |
| S8 | Rejection text `subordinate charm "<name>" lacks "requires" relation with container scope` | meta.go:791 | S |

## The implicit `juju-info` relation endpoint

| Id | Statement | Evidence | Verdict |
|---|---|---|---|
| J1 | Every charm has an implicit endpoint `juju-info`, role `provides`, interface `juju-info`, scope `global` | domain/application/state/state.go:367-375; domain/application/state/metadata.go:468-475; core/relation/relation.go:10 | S |
| J2 | Juju adds it when it records the charm, unless the metadata already declares an endpoint named `juju-info` | state.go:367-375 ("Add it if the charm author has not"); domain/crossmodelrelation/state/model/remoteapplication.go:1621-1629 (`hasJujuInfoRelation`) | S |
| J3 | The metadata needs no declaration of it | J2 | S |
| J4 | A subordinate charm consumes it with a `requires` endpoint, interface `juju-info`, scope `container` | domain/deployment/charm/meta.go:777-793; relation.go:3704-3721 (a match needs equal interface and opposite roles); relation.go:292-300 | S |
| J5 | Convention: name it `juju-info`; any other name works (`info`, `general-info`) | docs/reference/relation.md:59 (UP); domain/application/service/metadata.go:555-565 (a name check applies to `requires` names except container-scoped endpoints on subordinates); the interface, not the name, drives matching: types.go:227-232 | U |
| J6 | Juju rejects metadata declaring an endpoint named `juju` or `juju-*`; exempt: container-scoped `requires` endpoint of a subordinate charm, the implicit endpoint itself, any endpoint of a charm named `juju-*` | domain/application/service/metadata.go:518-568 (lines 521-523 charm-name exemption; 525-528 `implicitRelation` exemption on provides; 555-560 subordinate container exemption) | S |
| J7 | A relation through `juju-info` is a subordinate relation because the subordinate's endpoint is container-scoped | relation.go:292-300 | S |
| J8 | The endpoint is useful for machine charms, because subordinate charms are machine charms | meta.go:292-297 ("subordinate charms ... are machine charms by nature"); core/relation/relation.go:6-9 (the endpoint "facilitates relations between subordinate and other charms") | S |
| J9 | General-purpose subordinates that need no application-specific data use it, for example ntp, telegraf, nrpe, canonical-livepatch | relation.md:57 (UP, Charmhub links); charm.md:114-117 lists telegraf, livepatch, nrpe as subordinates | U |
| J10 | `juju integrate <subordinate> <principal>` relates when exactly one pair of endpoints is compatible | relation.go:3724-3736 | S |
| J11 | With an explicit matching endpoint also present, two pairs are compatible; Juju refuses with `ambiguous relation` | relation.go:3710-3734 (all matches are collected, no precedence); domain/relation/errors/errors.go:11; docs/howto/manage-relations.md:36-41 (UP: an ambiguity error with two candidate pairs) | S |
| J12 | Naming the implicit endpoint on either side selects it; command form | relation.go:3492-3517 (a named endpoint narrows the candidates), 3667-3674 | S |

## Non-subordinate relation

| Id | Statement | Evidence | Verdict |
|---|---|---|---|
| NS1 | A non-subordinate (regular) relation is a non-peer relation with scope `global` | relation.go:297-300; relation.md:76 (UP term "aka regular") | S |
| NS2 | It creates no units | subordinateunit.go:50-57 | S |

## Cross-model relation

| Id | Statement | Evidence | Verdict |
|---|---|---|---|
| C1 | A CMR is a non-peer relation where one application is a remote application | relation.go:4126-4152 (an application whose charm source is `cmr`); domain/crossmodelrelation/service/remoteapplication.go:146-149 | S |
| C2 | A remote application is a proxy in one model for an application of another model | remoteapplication.go:171-172, 236-240 ("synthetic application representing an offer from an external model"; "representing the application on the consuming model") | S |
| C3 | The two models can belong to different controllers | remoteapplication.go:217-225 (`OffererControllerUUID`); cmd/juju/commands/bootstrap.go:162-163 ("cross-model (cross-controller, actually)") | S |
| C4 | Example: databases on bare metal, applications on Kubernetes | relation.md:87 (UP example) | U |
| C5 | Offering side hosts the offered application; consuming side holds a remote application (saas) standing for the offer | remoteapplication.go:171-172, 236-240; relation.md:91 (UP term saas) | S |
| C6 | An offer cannot include a container-scoped endpoint | domain/crossmodelrelation/state/model/offer.go:100-102 | S |
| C7 | Consuming model: remote application has the saas name, for example `prometheus` | remoteapplication.go:173 (`applicationName` is the name in the consuming model); relation.md:95 (UP example) | U |
| C8 | Offering model: each consuming relation has its own remote application named `remote-` plus 32 hex digits, one endpoint | core/application/name.go:32-36; remoteapplication.go:254-256, 289-291 | S |
| C9 | Egress subnets can be set only on a cross-model relation | relation.go:116-124 (`integrating via subnets for non cross model relations`, NotSupported) | S |
| C10 | Requirer consuming application: its model publishes egress to the offering model; provider consuming application: its model opens ingress for the offering model's egress | internal/worker/firewaller/firewaller.go:1704-1707, 1780-1783 | S (offering-side requirer not traced; G) |
| C11 | Kubernetes controller: advertised addresses come from `controller-external-name` and `controller-external-ips`, set with `--config` at bootstrap | environs/bootstrap/config.go:71-77, 185-194; cmd/juju/commands/bootstrap.go:141-163, 199 | S |
| C12 | Other controllers must be able to resolve those addresses | bootstrap.go:162-163 | S |
| C13 | Juju reads these keys only at bootstrap | environs/bootstrap/config.go:100-113, 198-200 (`IsBootstrapAttribute`: "only relevant during bootstrap") | S |

## Rules for establishing a relation

| Id | Statement | Evidence | Verdict |
|---|---|---|---|
| R1 | Identifier form `<application>` or `<application>:<endpoint>` | domain/relation/service/relation.go:414-417 | S |
| R2 | Each identifier matches an endpoint, otherwise `relation endpoint not found` | relation.go:3677-3687; domain/relation/errors/errors.go:57 | S |
| R3 | Exactly one compatible pair; compatibility is different applications, same interface, opposite roles | types.go:227-232; relation.go:3710-3736 | S |
| R4 | No compatible pair: `no compatible endpoints found between applications` | errors.go:23; relation.go:3724-3725 | S |
| R5 | Several pairs: `ambiguous relation`, candidate pairs listed, operator names the endpoints | relation.go:3726-3733; errors.go:11; application.go:1490-1491 (UP how-to 36-47) | S |
| R6 | Container-scoped endpoint only if at least one application is a subordinate | relation.go:3714-3717 | S |
| R7 | ... and the bases of the two applications are compatible | relation.go:3179-3207, 280-282 | S |
| R8 | Not both remote | relation.go:4126-4152; errors.go:19 | S |
| R9 | Both applications alive, including a remote application | relation.go:253-277 | S |
| R10 | No relation exists yet; client code `already exists` | relation.go:3824-3851, 249-251; application.go:1441-1448; rpc/params/apierror.go:191 | S |
| R11 | Endpoint limit: a charm sets `limit`; a limit above zero caps the relations of that endpoint | domain/deployment/charm/meta.go:197-203, 697-712, 886; relation.go:3288-3306 (`ep.Capacity > 0 && count >= Capacity`) | S |
| R12 | Client receives `quota limit exceeded` with message `adding relation between endpoints "<a>" and "<b>": quota limit exceeded` | application.go:1433-1440; rpc/params/apierror.go:210; errors.go:27 | S |
| R13 | Egress subnets only for a CMR | relation.go:116-124 | S |

## Relation ID and key

| Id | Statement | Evidence | Verdict |
|---|---|---|---|
| K1 | Relation ID: number assigned from a model sequence at creation | relation.go:106 (`sequencestate.NextValue`); peer_relation.go:62 | S |
| K2 | The ID is unique in the model | 0024-relation.sql:105-106 (`idx_relation_id` unique) | S |
| K3 | Key of a non-peer relation: `<requirer-app>:<requirer-endpoint> <provider-app>:<provider-endpoint>`, requirer first | core/relation/key.go:32-37, 46-52, 64-73, 93-113 | S |
| K4 | Key of a peer relation: `<application>:<peer-endpoint>` | key.go:57-63, 94-101 | S |
| K5 | Every endpoint in a key carries its endpoint name | key.go:131-135 (`expected endpoint string of the form <application-name>:<endpoint-name>`) | S |
| K6 | The remove operation takes the two endpoints or the ID | relation.go (service):1069-1099; application.go:1475-1494 | S |
| K7 | Remove needs write access | application.go:1476 | S |
| K8 | With several relations between the two applications the endpoints are ambiguous; the ID is required | domain/relation/state/relation.go:220-232; application.go:1490-1491 (`specify relation endpoints or id`) | S |

## Relation status

| Id | Statement | Evidence | Verdict |
|---|---|---|---|
| T1 | Six statuses: joining, joined, broken, suspending, suspended, error | 0024-relation.sql:228-234; core/relation/status.go:13-26; core/status/status.go:209-210 | S |
| T2 | Juju sets `joining` at creation | relation.go:3802-3806; peer_relation.go:83 | S |
| T3 | `joining`: should become joined soon | core/status/status.go:209 | S |
| T4 | `joined`: alive and healthy | core/relation/status.go:14-15 | S |
| T5 | `broken`: life gone to dead | core/relation/status.go:17-18 | S |
| T6 | `suspended`: temporarily broken until an action resumes it | core/relation/status.go:20-22 | S |
| T7 | `error`: error state; setting it requires a message | status.go:24-25; domain/status/status.go:197-200 | S |
| T8 | Only the leader unit of an application in the relation sets the status | domain/status/service/leaderservice.go:187-189, 213-218; apiserver/facades/agent/uniter/uniter.go:2153-2159, 2174-2180 | S |
| T9 | Transition rules (same status accepted; broken from any; error from any; joined and suspended not from broken; joining not from broken or joined; suspending not from broken or suspended) | domain/status/status.go:186-212 | S |
| T10 | A refused change fails with `relation status transition not valid` | domain/status/errors/errors.go:17-19; status.go:205-208 | S |

## Relation settings

| Id | Statement | Evidence | Verdict |
|---|---|---|---|
| E1 | Two levels: unit settings per unit that entered, application settings per application endpoint | 0024-relation.sql:109-122, 144-157, 194-207 | S |
| E2 | Keys and values are non-empty strings | 0024-relation.sql:148-149, 198-199 | S |
| E3 | Setting a key to an empty value removes it | internal/worker/uniter/runner/jujuc/relation-set.go:193-199; domain/relation/service/relation.go:366-388 | S |
| E4 | A unit writes its own unit settings | apiserver/facades/agent/uniter/uniter.go:2954-2959 (`rus.Unit != changes.Tag` is ErrPerm) | S |
| E5 | Application settings are written by the leader | relation-set.go:176-182; domain/unitstate/types.go:316-325; domain/unitstate/service/commithook.go:174-189 | S |
| E6 | Every unit in the relation reads unit settings and application settings | relation-get.go:241-263 (non-leader own-app reads and all remote reads go to the controller); uniter.go:1976-2024 (`readOneRemoteSettings`: no leader check, unit or application tag) | S for the code path; intent open (finding F26) |
| E7 | In a peer relation the only application is the local one | 0024-relation.sql:59-63 | S |
| E8 | In a non-peer relation the other application's settings are read-only for every unit | E4, E5 (no write path for another application's settings) | I |
| E9 | Juju writes `ingress-address` and `egress-subnets` in unit settings and drops charm-set values | domain/unitstate/types.go:19-20; commithook.go:430-434; uniter.go:2944-2951 | S |
| E10 | A leaving unit's last settings are kept and stay readable until the relation is removed | 0024-relation.sql:170-189 | S |
| E11 | A non-leader that writes application settings receives `cannot write relation settings` | relation-set.go:176-182 | S |

## Upstream statements dropped, and why

| Upstream line | Statement | Reason |
|---|---|---|
| 36 | "peer relations are also the mechanism behind high availability" | Unverifiable in source; docs/reference/high-availability.md:54-58 names a peer relation of one charm only |
| 36 | "every relation results in the creation of unit and application databags in Juju's database" | Mirrors implementation; rows exist per unit that entered scope and per key set (0024-relation.sql:109-218), not per relation |
| 53 | "cannot be declared" | False: domain/application/service/metadata.go:525-528 exempts the implicit endpoint; state.go:367-375 expects authors may declare it |
| 53 | "does not appear in `juju info <charm>` or on Charmhub" | Unverifiable (Charmhub, CLI rendering not traced) |
| 53 | "supported on every kind of charm" | Unverifiable (no source statement) |
| 67 | "explicit endpoints take precedence over the implicit `juju-info` one" | False: relation.go:3724-3734 |
| 89 | "bootstrapped with `--controller-external-ips`, `--controller-external-name`, or both" when the topology is not flat | False as written: these are `--config` keys for Kubernetes controllers (bootstrap.go:141-163, 199); the non-flat-topology trigger has no source |
| 91 | "does not make a difference which side ... interchangeable" | Unverifiable |
| 91 | "ports are opened on the provider side" | Reworded to the traced behavior (C10) |
| 104-106 | "Each unit involved in a relation gets a local copy of all the databags" | Unverifiable; settings live in the controller database (0024-relation.sql:144-218) and the unit reads non-local ones from the controller |
| 81-83 | second `See also: manage-relations` | Duplicate of lines 10-12 |
| 96-98 | "Non-cross-model relation" section | Fragment; a negation of the previous definition, folded into the CMR definition |
| 16-29 | taxonomy figure | A figure is optional; the prose now holds every fact and the figure's `regular*` definition contradicted the prose |
| 108-120 | databag permissions figure | Same; the table holds the facts |
