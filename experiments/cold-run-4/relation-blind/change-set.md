# Change set for docs/reference/relation.md (52e983a435)

The separate findings file was refused by the Write tool, so the findings are carried here in the same fields (Where, Quoted, Type, Evidence, Fix, Severity, Confidence, Addressee). Part 1 lists findings, part 2 lists changes. Every change cites a finding. Rule names cite the rule-derivation.md ledger by its row text. No prescribed section template exists in either input; the contract says it "fixes no section structure for a page".

## Part 1: Findings

### High

| Id | Where | Quoted | Type | Evidence | Fix | Sev | Conf | Addressee |
|---|---|---|---|---|---|---|---|---|
| F7 | 46 | "A subordinate relation is a non-peer relation where one application is principal and the other subordinate." | False (conditional truth stated flat) | domain/relation/state/relation.go:292-300 sets scope `container` only when an endpoint is container-scoped; domain/relation/state/subordinateunit.go:50-57 creates units only for container scope. A subordinate related to a regular application over global endpoints gives a global relation that creates no unit. | Define by scope; reference page, entity relation | high | determined | Operator |
| F13 | 67 | "explicit endpoints take precedence over the implicit `juju-info` one when Juju resolves the relation" | False | relation.go:3704-3734 collects every compatible pair and returns ambiguous when more than one; docs/howto/manage-relations.md:36-41 shows the same error | Replace by the ambiguity statement | high | determined | Operator |
| F18 | 89 | "bootstrapped with `--controller-external-ips`, `--controller-external-name`, or both ... read-only thereafter" | False and conditional truth stated flat | cmd/juju/commands/bootstrap.go:141-163, 199 (`--config` keys, Kubernetes controllers); environs/bootstrap/config.go:71-77, 185-194, 198-200 | Restate for Kubernetes controllers; link a bootstrap page | high | determined for facts, tie for home | Operator |

### Medium

| Id | Where | Quoted | Type | Evidence | Fix | Sev | Conf | Addressee |
|---|---|---|---|---|---|---|---|---|
| F9 | 53 | "does not need to be (and cannot be) declared" | False | domain/application/service/metadata.go:525-528; domain/application/state/state.go:367-375 | "needs no declaration" | med | determined | Charm author |
| F9b | 53 | "does not appear in `juju info <charm>` or on ... Charmhub"; "supported on every kind of charm" | Unverifiable | none | delete | med | determined | Charm author |
| F10 | 48-55 | subordinate charm rules | Not enough (T4) | domain/deployment/charm/meta.go:777-793 | add rule and text | med | determined | Charm author |
| F12 | 59 | "any name can be used" | Conditional truth stated flat | metadata.go:518-568 | state exemptions | med | determined | Charm author |
| F15 | 76, figure | "(aka 'regular') ... both principal" vs figure footnote "Regular: Non-peer, non-subordinate, non-cross model" | Ambiguous; Contradicts (figure vs prose) | relation.go:297-300 | one definition by scope | med | determined | Operator, browser reader |
| F19 | 91 | "interchangeable ... ports are opened on the provider side" | Unverifiable; Ambiguous ("saas" undefined) | internal/worker/firewaller/firewaller.go:1704-1707, 1780-1783 | restate traced behavior | med | determined (traced part), open (offering-side requirer) | Operator |
| F20 | 93-95 | "remote + token" | Ambiguous | core/application/name.go:32-36 | state name form | med | determined | Operator |
| F23 | 102 | "`application1:[endpoint] application2:[endpoint]`" | False / Ambiguous / Not enough | core/relation/key.go:32-37, 46-52, 131-135 | order, peer form, endpoint always present | med | determined | Operator, client developer |
| F24 | 104-106 | "Each unit ... gets a local copy of all the databags"; "per application, and can be application-scoped or unit-scoped" | Unverifiable; Ambiguous; Mirrors implementation | domain/schema/model/sql/0024-relation.sql:144-218; internal/worker/uniter/runner/jujuc/relation-get.go:241-263 | name the two levels; drop local-copy claim | med | determined | Charm author |
| F26 | 122-131 | non-peer "leader units can also read ... the local application databag" vs peer "all units can read" | Relies on implicature; conditional truth stated flat | relation-get.go:241-263; apiserver/facades/agent/uniter/uniter.go:1976-2024 (no leader check on non-leader own-application reads); service.go:491-496 comment says leader only; writes need leadership: relation-set.go:176-182, domain/unitstate/types.go:316-325 | writer and reader table; ask owner about intent | med | open(intent) | Charm author |
| F26b | 122-131 | permissions text | Gap (T3, T4, T5) | domain/unitstate/service/commithook.go:430-434; 0024-relation.sql:170-189; relation-set.go:181 | add three facts | med | determined | Charm author |
| F28 | whole page | relation status absent | Gap (T2) | domain/status/status.go:186-212; 0024-relation.sql:228-234 | add status and enforced transitions | med | determined; placement open(Q1) | Operator |
| F29 | whole page | creation rules absent | Gap (T3, T4) | relation.go:80-128, 235-322, 3661-3737, 4126-4152 | add conditions; error entries belong to the call page | med | determined; error home open(Q5) | Operator |

### Low (batch)

F1 "databag" for "settings" (ledger: one term for one meaning); F2 caption text duplicated in light and dark blocks, and "applications are identical" is ambiguous; F3 title "Relation taxonomy" is uninformative; F3b peer definition omits creation, ID order, removal; F4 "persist charm data ... in Juju's database" mirrors implementation; F5 "mechanism behind high availability" unverifiable (docs/reference/high-availability.md:54-58 names one charm's peer relation only); F8 subordinate-charm definition and "no unit at deploy" duplicate docs/reference/charm.md:107-112; F11 "standard mechanism used by general-purpose machine subordinates" unverifiable, kept as upstream statement; F14 two `juju integrate` blocks are procedure in a reference page (category mix); F16 "+/- controllers, +/- clouds" ambiguous notation, cloud difference unsourced; F17 second "See also" duplicates lines 10-12; F21 "Non-cross-model relation" is a fragment; F22 list and heading without blank lines (lines 93-96); F25 light and dark figure blocks differ, alt text names a topic; F27 "turned inwards" metaphor; F30 juju-info is an endpoint of every charm filed under a relation heading (only the reading-path measure and source-owner measure disagree with the current home, application.md:36 links to the label; boundary left, see notes); F31 definition at line 14 names one application and one endpoint for a two-ended record; F32 labels must survive (R15).

## Part 2: Changes

| # | Action | Home | Category | Requirement | Finding | Confidence |
|---|---|---|---|---|---|---|
| 1 | Rewrite lede: two endpoints of two applications, or a peer endpoint; who creates, who may | relation page | reference | T1 | F31 | determined |
| 2 | Delete section title "Relation taxonomy" and its figure; headings become the type names | relation page | reference | T1 | F3, F2, F15, F25 | determined |
| 3 | Peer: add creation time, ID order, removal refusal; delete HA claim and database framing | relation page | reference | T1, T5 | F3b, F4, F5 | determined |
| 4 | Non-peer: add different applications, scope rule | relation page | reference | T1 | F7, F15 | determined |
| 5 | Subordinate: define by container scope; unit creation; charm rule and text | relation page | reference | T1, T4 | F7, F8, F10 | determined |
| 6 | juju-info: correct "cannot be declared", state name exemptions, replace precedence with ambiguity, drop unverifiable lines | relation page (label kept) | reference | T1, T3, T4 | F9, F9b, F11, F12, F13, F14 | determined |
| 7 | Non-subordinate: define by scope global; fold "Non-cross-model" away | relation page | reference | T1 | F15, F21 | determined |
| 8 | CMR: remote application definition, names, offer limit, egress, firewall, Kubernetes controller keys; drop interchangeable claim and duplicate ibnote | relation page | reference | T1, T4, T6 | F16, F17, F18, F19, F20 | determined; offering-side requirer open |
| 9 | Add "Rules for establishing a relation" with the verified conditions and the two client codes | relation page; call-level error entries stay with the integrate call | reference | T3, T4 | F29 | determined; home of error entries open(Q5) |
| 10 | Rewrite "Relation identification" as ID and key | relation page | reference | T6, T8 | F23 | determined |
| 11 | Add "Relation status" | relation page | reference | T2 | F28 | determined; `suspending` meaning has no source |
| 12 | Rewrite "Relation databag" as settings: two levels, writer and reader table, Juju-owned keys, archive; drop figure | relation page | reference | T1, T3, T5 | F1, F24, F25, F26, F26b, F27 | determined; non-leader local read intent open |
| 13 | Fix blank lines around list and heading | relation page | reference | Manner | F22 | determined |
| 14 | Keep all labels | relation page | reference | R15 | F32 | determined |
