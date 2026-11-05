# Trace: `draft-relation.md` to the 4.1 source at 52e983a435

Paths abbreviate to `drs/` = `domain/relation/state/relation.go`, `drsv/` = `domain/relation/service/relation.go`, `uni/` = `apiserver/facades/agent/uniter/uniter.go`, `app/` = `apiserver/facades/client/application/application.go`, `sql/` = `domain/schema/model/sql/0024-relation.sql`. `UD` marks an upstream doc statement as the only support. `U` marks a statement I could not fully trace; it is listed again in `notes.md`.

## Lede and kinds

| # | Statement | Evidence |
|---|---|---|
| L1 | A relation connects an endpoint of one application to an endpoint of a different application | `core/relation/doc.go:7-9`; `domain/relation/types.go:226-232` (`ApplicationName !=`) |
| L2 | A peer relation has one endpoint and connects the units of one application | `core/relation/doc.go:7-9`; `sql/:59-63`; `core/relation/key.go:32-37` |
| L3 | Each relation has an ID unique in its model, a key, a life, a status | `sql/:84-103` (id, life), `:105-106`, `:238-249` (status); key `core/relation/key.go:32-37` |
| K1 | A non-peer relation has global or container scope; a regular relation can be cross-model | `drs/:292-298`; `drs/:4076-4090` (remote application) |
| K2 | Non-peer: same interface, opposite roles `provides`/`requires` | `domain/relation/types.go:226-232`; `domain/deployment/charm/meta.go:30-36` |
| K3 | Non-subordinate = regular = global scope; global unless an endpoint is container | `drs/:292-298`; `cmd/juju/status/formatter.go:342-348` ("regular" is the default) |
| K4 | Cross-model: a regular relation with a remote application | `drs/:4076-4090` (`cs.name = 'cmr'`), `:4126-4152` |
| K5 | Remote application = stand-in for an application of another model | `domain/crossmodelrelation/service/remoteapplication.go:236-257` (synthetic application "representing the application on the consuming model") |
| K6 | Offering and consuming model; can be on different controllers and clouds | `app/:1706-1712` (`OffererControllerUUID`, `OffererModelUUID`); UD `docs/reference/juju-cli/list-of-juju-cli-commands/integrate.md` ("models may be managed by different controllers and/or hosted on different clouds") |
| K7 | The consuming model holds one remote application per offer, under the name it gives | UD `docs/howto/upgrade-your-juju-deployment-from-36-to-41.md:452` ("a maximum of one SAAS per remote offer"); `app/:1706` (`applicationName`) |
| K8 | The offering model holds one remote application per relation with a consumer | `remoteapplication.go:236-257` (`AddConsumedRelation` creates a synthetic application per `RelationUUID`) |
| K9 | Name `remote-` + 32 hex digits from a generated UUID | `core/application/name.go:34-36`; `remoteapplication.go:240-256` (`NewUUID`) |
| K10 | Each remote application has exactly one endpoint | `remoteapplication.go` comment "only one endpoint per synthetic application" (near `synthCharmHasOnlyOneEndpoint`) |
| K11 | Peer endpoints cannot take part | `app/:1727-1728`; `domain/relation/errors/errors.go:38-41` |
| K12 | Both applications cannot be remote | `drs/:4126-4152` |
| K13 | Only cross-model relations can be suspended and resumed | `domain/relation/state/remoterelation.go:44-49` |
| K14 | Egress CIDRs only for cross-model | `drs/:117-128` |
| K15 | Units of a subordinate application cannot enter it | `domain/relation/errors/errors.go:43-46`; `remoterelation.go` doc of `SetRelationRemoteApplicationAndUnitSettings` ("the unit's application is a subordinate") |
| K16 | Kubernetes controller advertises the address of its `controller-external-name`/`-ips` setting; it must resolve from other controllers | `cmd/juju/commands/bootstrap.go:159-167`; keys `environs/bootstrap/config.go:60-77`; Kubernetes only `bootstrap.go:664-670` |
| K17 | Offering model opens access only when its endpoint is the provider | `internal/worker/firewaller/firewaller.go:1899-1918` |
| K18 | Consuming model publishes the networks it connects from | `firewaller.go:2129-2160` (`publishIngressToRemote`) |
| K19 | The offering model allows the networks `saas-ingress-allow` permits | UD `docs/reference/configuration/list-of-model-configuration-keys.md:839-843`; `firewaller.go:2175-2185` ("not permitted on the offering side") |
| K20 | Refusal gives the consuming relation status `error` with the refusal as message | `firewaller.go:2175-2185` (`SetRelationErrorStatus(..., err.Error())`) |
| S1 | Subordinate = non-peer with container scope | `drs/:292-298`; `cmd/juju/status/formatter.go:342-344` |
| S2 | Container scope when either endpoint has it | `drs/:292-298` |
| S3 | At least one application is a subordinate | `drs/:3661-3733` (`inferEndpoints` skips container pairs unless a subordinate); `domain/relation/state/doc.go:33-34` |
| S4 | The other can be principal or subordinate | `drs/:1994-1996` ("a relation between two subordinates, which is OK") |
| S5 | A subordinate application has no units when deployed | UD `docs/reference/charm.md:112` |
| S6 | A unit is created each time a principal unit enters scope, on the same machine | `drs/:1861-1866`; `drsv/` `EnterScope` doc and `makeSubordinateStorageArgs` ("machine net node of the principal unit") |
| S7 | The two applications must run on compatible bases | `drs/:3181-3210` (applies when an endpoint has container scope) |
| J1 | Every application has an implicit endpoint `juju-info`, `provides`, interface `juju-info`, global scope | `domain/application/state/metadata.go:468-475`; `core/relation/relation.go:6-10` |
| J2 | Juju adds it unless the charm declares one | `domain/application/state/state.go:367-373`; `metadata.go:505-513` |
| J3 | The units of the providing application run no hooks for it | `internal/worker/uniter/relation/relationer.go:61-64`, `:126-130` |
| J4 | A subordinate attaches by requiring `juju-info` with container scope | `core/relation/relation.go:6-9`; `domain/application/service/metadata.go:550-557` |
| J5 | The principal always provides `juju-info`, so no common interface is needed | `core/relation/relation.go:6-9` |
| J6 | The requiring endpoint's name is free; `juju-info` is the convention | `domain/application/service/metadata.go:550-557`; the convention is UD `relation.md:59` |
| J7 | More than one compatible pair gives "ambiguous relation" and the caller names the endpoints | `drs/:3726-3733`; `domain/relation/errors/errors.go:9-11`; UD `docs/howto/manage-relations.md:35-49` |
| J8 | The example with an explicit endpoint besides `juju-info` produces two pairs | `drs/:3661-3733` (no ranking of `juju-info`; I did not run a probe) |
| J9 | The `juju integrate <sub>:<req> <principal>:juju-info` call names the pair | UD `relation.md:67-71` and `cmd` help; `drs/:3492-3523` (endpoint name filter) |
| P1 | Peer endpoint has the `peer` role | `core/relation/key.go:59`; `domain/deployment/charm/meta.go:36` |
| P2 | Created at deploy when the charm declares a peer endpoint; no client adds it | `domain/relation/state/doc.go:11-13`; `domain/relation/types.go:230` (peer cannot be `CanRelateTo`) |

Line accuracy: line numbers that came from a `grep -n` are exact. The others I read off `sed` windows and can be off by a few lines; the function or constant named beside them is exact. A checker should resolve the function.

## Relation database schema

| # | Statement | Evidence |
|---|---|---|
| D1 | ID from a model sequence, unique, never reused | `domain/relation/state/doc.go:14-20`; `sql/:105-106` |
| D2 | Life `alive`, `dying`, `dead` | `domain/schema/model/sql/0000-life.sql:6-9`; `sql/:97-99` |
| D3 | A relation is dead only after all its units left scope | `domain/relation/state/doc.go:55-56` |
| D4 | Scope `global` or `container` | `drs/:4158-4170` (`encodeScope`); `sql/:94`, `:100-102` |
| D5 | Suspended flag and reason | `sql/:88-89` |
| D6 | Key: endpoints joined by a space, requirer first, each `<application>:<endpoint>`; peer key one endpoint | `core/relation/key.go:32-37`, `:46-52`, `:81-90` |
| D7 | Relation endpoint links relation to application endpoint; two or one | `sql/:59-77` |
| D8 | An application endpoint appears at most once in a relation | `sql/:76-77` (unique index) |
| D9 | Relation unit: a unit entered scope at an endpoint; at most one per endpoint and unit | `sql/:108-122` |
| D10 | Unit settings: keys and values never empty; key unique per relation unit | `sql/:144-154` (`chk_key_empty`, `chk_value_empty`, primary key) |
| D11 | Application settings: per relation endpoint; never empty; unique key | `sql/:194-204` |
| D12 | Departed settings copied when a unit leaves; kept until the relation is removed | `sql/:170-189` (comment "copy ... upon leaving scope"; "lifetime of a relation") |
| D13 | Status has message and update time; six values | `sql/:228-249` |
| D14 | `joined` normal; `broken` when life is dead; `suspended` temporarily broken until resumed | `core/relation/status.go:13-22` (comments) |

## Relation calls

| # | Statement | Evidence |
|---|---|---|
| C0 | A unit agent is logged in as its unit and acts only for that unit | `uni/:1656-1659`, `:1848`, `:2118` (`canAccess(unitTag)`); definition per `page-recipe.md` |
| A1 | Caller: client, write access, no change block | `app/:1416-1421`, `:271-273` |
| A2 | Exactly two endpoints; `<application>` or `<application>:<endpoint>` | `app/:1424-1426`; `drsv/:415-418` |
| A3 | Missing endpoint: pair all, keep relatable, require exactly one | `drs/:3661-3733`; `:3492-3523` |
| A4 | Relatable: different applications, same interface, opposite roles | `domain/relation/types.go:226-232` |
| A5 | Both applications alive | `drs/:235-282` |
| A6 | Not already related | `drs/:3826-3853`; `:251-253` |
| A7 | Endpoint limit | `drs/:3288-3307` (`Capacity > 0`) |
| A8 | Container scope: a subordinate application and compatible bases | `drs/:3661-3733`; `:3181-3210` |
| A9 | At most one remote application | `drs/:4126-4152` |
| A10 | CIDRs: cross-model only; each valid | `drs/:117-128`; `drsv/:427-441` |
| A11 | New relation alive, next ID, scope from endpoints, status `joining` | `drs/:106`, `:292-298`, `:3741-3771`, `:3802-3824` |
| A12 | Result: charm relation per application name | `app/:1455-1458` |
| AE1 | `a relation should have exactly two endpoints`, `bad request` | `app/:1425`; the suffix " bad request" that `errors.BadRequestf` appends is a library behavior I could not verify here (U) |
| AE2 | no candidates ... relation endpoint not found | `drs/:92-95` (wrapper), `:3681-3690`; `errors.go:55-57`; facade wrapper `app/:1449-1452`. Code empty by `apiserver/errors/errors.go` default branch (U) |
| AE3 | no compatible endpoints found between applications | `drs/:3720-3724`; `errors.go:21-23` |
| AE4 | ambiguous relation ... could refer to | `drs/:3726-3733`; `errors.go:9-11` |
| AE5 | `already exists`, code `already exists` | `app/:1441-1448`; `errors.go:59-61`; `rpc/params/apierror.go:191` |
| AE6 | quota limit exceeded, code `quota limit exceeded` | `app/:1433-1440`; `drs/:3301`; `apierror.go:210` |
| AE7 | unable to integrate two cross model applications together | `drs/:4151` |
| AE8 | application `<name>` is not alive | `drs/:253-282` (`application %s is not alive`), wrapper `drs/:102` |
| AE9 | no compatible bases found | `drs/:3181-3210`; wrapper `:236-250` |
| AE10 | integrating via subnets for non cross model relations | `drs/:122-124` |
| AE11 | CIDR not valid / cannot be empty | `drsv/:430-437` |
| R1 | Removing: caller, no remove block | `app/:1475-1481` |
| R2 | Takes the two endpoints or the ID | `app/:1483-1486` |
| R3 | After the call: not alive, removed or scheduled | `domain/removal/service/relation.go:76-82` |
| R4 | Force and maximum wait | `domain/removal/service/relation.go:76-82` (wait "ignored if force is false"); `app/:1495-1503` |
| R5 | A cross-model removal also removes the offer connection and remote application records | `domain/removal/service/relation.go` `relationScheduleRemoval` doc |
| RE1 | `relation with endpoints [a b] or id n not found`, `not found` | `app/:1488-1490` (`NotFoundf` suffix " not found" confirmed by `application_test.go:521`); `apierror.go:164` |
| RE2 | `endpoints "[a b]" are ambiguous, specify relation endpoints or id` | `app/:1490-1492`; suffix of `BadRequestf` unverified (U); the code is not stated in the entry |
| X1 | Suspending: caller, change block | `app/:1531-1537` |
| X2 | Takes IDs, flag, message; per-ID result | `app/:1530-1545`, `:1584` |
| X3 | Already in state: unchanged | `app/:1553-1556` |
| X4 | Only cross-model | `remoterelation.go:44-49`; `app/:1559-1561` |
| X5 | Suspending sets flag, reason, status `suspending` with message | `remoterelation.go:150-155`, `:182-196`; `app/:1564-1567` |
| X6 | Resuming sets `joining` with empty message | `remoterelation.go:156-158`; `app/:1568-1572` |
| XE1 | `relation <id> not found`, `not found` | `app/:1541-1549`; `apierror.go:164` |
| XE2 | `relation must be a remote relation to be suspended` | `remoterelation.go:46-48` |
| N1 | Enter scope: caller unit agent for its own unit | `uni/:1656-1659` |
| N2 | Unit and relation alive | `drs/:2057-2073` |
| N3 | Unit's application is in the relation | `drs/:2075-2122` |
| N4 | Already in scope: stays, call succeeds | `drsv/` `EnterScope` doc; `drs/:1813-1832` |
| N5 | Settings start with `ingress-address`, `egress-subnets` when available | `uni/:1711-1725` |
| N6 | Container scope, principal unit: subordinate unit on the same machine with storage from directives | `drs/:1861-1866`; `drsv/` `EnterScope` and `makeSubordinateStorageArgs` docs |
| N7 | A subordinate unit entering with a non-principal application is left out; call succeeds | `drs/:1991-2026` (`PotentialRelationUnitNotValid`); `uni/:1696-1701` |
| NE1 | `checking unit valid in relation: cannot enter scope, unit or relation not alive`, code `cannot enter scope` | `drs/:1805-1810` wrapper, `:2057-2073`; `uni/:1639-1643`; `apierror.go:174` |
| NE1r | Unit agent drops the relation from local state | `internal/worker/uniter/relation/statetracker.go:295-304` |
| NE2 | `cannot enter scope, subordinate unit exists but is not alive`, `cannot enter scope yet` | `errors.go:33-36`; `uni/:1644-1648`; `apierror.go:175`; prefix chain unread (U) |
| NE2r | Unit agent waits for the subordinate to be removed | `statetracker.go:202-204` |
| NE3 | `checking unit valid in relation: unit not in relation` | `drs/:2118-2122`; `errors.go:95-97` |
| G1 | Reading: caller unit agent for its own unit | `uni/:1775-1790`, `:1848` |
| G2 | A unit reads its own unit settings | `uni/:1843-1855` |
| G3 | Only the leader reads its own application's settings | `drsv/:284-292`; `uni/:1862` (doc "when invoked by the leader unit"), `:1949-1950` |
| G4 | Any unit reads any remote unit's or the remote application's settings | `uni/:1959-2022` (no leadership check) |
| G5 | Peer: same calls, remote side is own application | `uni/:1959-2022` (no peer branch); UD `relation.md:128-133` |
| G6 | Departed unit's settings readable until the relation is removed | `drsv/:925-960` (archive fallback); `sql/:170-189` |
| GE1 | `permission denied`, `unauthorized access` for these triggers | `uni/:1848`, `:1949-1950`, `:1796-1802`; `apiserver/errors/errors.go:36-37` map; `apierror.go:170` |
| W1 | Written in the call that commits hook changes | `uni/:2868-2975` |
| W2 | A unit writes only its own unit settings | `uni/:2957-2959` |
| W3 | Only the leader writes application settings | `domain/unitstate/types.go:321-326`; `domain/unitstate/service/commithook.go:177-190` |
| W4 | A key with an empty value is removed | `commithook.go:503-520`; `drsv/:372-386` |
| W5 | Juju alone writes `ingress-address`, `egress-subnets`; the unit's values are dropped | `commithook.go:432-434` |
| W6 | At most 16 MiB per set | `core/quota/fixed_limits.go:15-17`; `core/quota/kv.go:44-70`; `drs/:2431` |
| WE1 | `permission denied` for another unit's settings | `uni/:2957-2959` |
| WE2 | `... max allowed total size (16777216): quota limit exceeded`, `quota limit exceeded` | `core/quota/kv.go:69`; `drs/:2432`; `uni/:2882-2886` and `apiserver/errors/errors.go:234-235` |
| T1 | Set status: leader only, own unit | `domain/status/service/leaderservice.go:187-215`; `uni/:2118` |
| T2 | Leader's agent sets `joined` after entering scope | `statetracker.go:208-218` |
| T3 | Same value allowed; `broken` always; `suspending`, `joining`, `joined`/`suspended` restrictions; `error` needs a message | `domain/status/status.go:186-212` |
| T4 | `suspended` keeps the `suspending` message when new message is empty | `domain/status/state/model/modelstate.go:459-466` |
| TE1 | `cannot set status <new> when relation has status <current>: ...` | `domain/status/status.go:205-208` |
| TE2 | `cannot set status error without message` | `domain/status/status.go:198-200` |
| TE3 | `permission denied` | `uni/:2143-2159` (`RelationNotFound` and not-in-relation to `ErrPerm`), `:2118` |

## Dropped from upstream because the trace failed

"every relation results in ... databags" (F5); "peer relations ... mechanism behind high availability" (F6); "cannot be declared"; "does not appear in `juju info` or Charmhub"; "useful only for machine charms"; "explicit endpoints take precedence" (F10); "`--controller-external-ips` ... flat topology ... read-only thereafter" (F11); "interchangeable" (F12); "a local copy of all the databags" (F16); "used to persist charm data".

## Statements that remain partly untraced

- AE1, RE2: the suffix `errors.BadRequestf` appends. `NotFoundf` is confirmed by `application_test.go:521`; no test in the tree shows `BadRequestf`.
- AE2, AE3, AE4, AE7 to AE11, XE2, NE3, TE1: the client code. The entries omit a code because `ServerError` has no mapping for these constants (`apiserver/errors/errors.go:165-248`) and I did not trace the `Capture` chain that decides whether `params.ErrCode` finds one.
- NE2: whether a prefix precedes the message (`subordinateunit.go` read only by its doc lines).
- J8: by reading, no probe.
- W4: the empty-value rule shows in both `parseForSetAndUnsetSettings` copies, but I did not trace which copy `CommitHookChanges` uses for unit settings (`commithook.go:503` is the one in the unitstate service, and that service calls it).
- Access error for a user without write access, and the text of a change or remove block: not traced; the entries name the rule and omit the message.
