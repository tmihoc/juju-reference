# Cross-page duplicate-fact discovery sweep (session 99)

Method: read-only scout clusters, waves of 2-3, over the 35 entity pages (universe = pr-description.md preview links); cluster 4 run in-session after its scout 402'd twice (binding rule). Figure text (`:caption:`/`:alt:`/`:slide-captions:`), quoted CLI/error strings, and See-also navigation excluded. Scout transcripts: `history://SweepMachineUnitApp`, `history://SweepModelCloudCredential`, `history://SweepRelationCharmOffer` (cluster 4 in-session, no transcript).

## Candidate list (facts stated on two or more pages; one page should own each)

| # | Fact | Stated on | Owner (proposed) | Class |
|---|---|---|---|---|
| 1 | Unit-agent definition ("the process that runs the charm of a unit; logs in as its unit") | unit.md:101; application.md:198; relation.md:93; secret.md:108 | unit.md (`unit-agent`) | near-verbatim duplicate, four pages |
| 2 | Existing storage attachable only when one unit is added | unit.md:121; application.md:318 (verbatim), :222, :317 | unit.md | verbatim duplicate |
| 3 | Charm deleted when no application or unit uses it | unit.md:213; application.md:458 (verbatim) | charm.md | verbatim duplicate |
| 4 | Leader = the unit holding the application's lease | unit.md:35, :145; application.md:260 | unit.md (`leader-unit`) | variant |
| 5 | Machine becomes dying when its last unit is removed | machine.md:279; unit.md:208; application.md:454 | machine.md | variant |
| 6 | Juju adds the implicit `juju-info` endpoint to every charm | relation.md:38; charm.md:256 | charm.md | variant |
| 7 | Endpoint role (`provider`/`requirer`/`peer`) and scope (`global`/`container`) vocabularies | charm.md:56, :58; relation.md:38; offer.md:236, :85 | charm.md (vocabulary); relation.md (container-scope↔subordinate semantics) | variant/partial |
| 8 | Model deployed into one cloud, optional credential; not all clouds accept none | model.md:14, :77; cloud.md:20; credential.md:14 | model.md | variant |
| 9 | Agents follow the model's credential / cloud spec | model.md:53; credential.md:47; cloud.md:54 | credential.md (credential stream); cloud.md (cloud spec stream — distinct mechanisms) | partial |
| 10 | Migration needs the credential on the target (cloud, owner, name) | credential.md:145; model.md:241 | credential.md | variant |
| 11 | Migration needs the model's secret backend (by name) on the target controller | model.md:236 (trigger prose); secret.md:320; secret-backend.md:200 | secret-backend.md (its dedicated migration section) | variant (same shape as #10) |

Weaker/shared-vocabulary overlaps (recorded, not fix candidates): status eight-value vocabulary (unit.md:42, application.md:53/:174 — each page's own status record); Kubernetes scale vs add-unit refusal (unit.md:110/:122/:199/:205 vs application.md:306/:319 — properly linked both ways); migration preconditions on units (unit.md:419 vs application.md:530 — disjoint condition lists by subject); `status-set` hook-command acceptance list (unit.md:284, application.md:498 — owner outside the entity pages); remote application / local proxy (relation.md:50, offer.md:14/:228 — offer links `{cross-model-relation}`, borderline); `<model>-local` backend naming (secret.md:164, secret-backend.md:123); "primary controller" gloss (secret-backend.md:54, linked to controller-workers).

## No-link sentences (other page's subject, no `{ref}`)

- application.md:220, :306 (unit gets machine), :318, :260 (leader), :454 (machine dying), :458 (charm), :530, :198
- unit.md:208, :213; machine.md:279
- relation.md:38 (charm fact), :41, :113
- offer.md:58, :85, :121, :183, :185, :228, :236-237, :264, :266
- cloud.md:42, :45 (model-side behavior), :54, :146, :147
- model.md:241 (credential fact)
- credential.md:47, :106, :130
- secret.md:108 (unit-agent definition links `{ref}`agent``, not `{unit-agent}`)
- storage.md:138 (machine-agent definition, no `{ref}` to `machine-agent`)
- lease.md:38, :47, :63 (controller/model facts, no links)
- ssh-key.md:60, :125 (change-block and remove-block inlined, no link)

5. storage/ssh-key/ssh-server/lease — scout `SweepStorageSshLease` completed at close-out (10 findings, all recorded-class): the machine-agent definition restated on storage.md:138 is recipe-compliant (agent identities are defined per calls-section intro, session 93 — no fix); the watcher sentence and the controller-API parenthetical are boilerplate that links its owner or has no owner page; the no-access-level rule is restated (lease.md:47/:63 vs agent.md:67, bare per-call glue); the change-block and remove-block are inlined on ssh-key.md:60/:125 where storage.md:221 links; the ssh-key↔ssh-server overlaps (Kubernetes sessions, the `ubuntu` account, key authorization) all link the owner. Pair coverage: storage↔ssh-key, storage↔lease, and ssh-key↔lease have no subject overlaps.

6. space/subnet/zone/link-layer-device — run in-session (session 100; the scout `SweepSpaceSubnetZone` 402'd twice in session 99 and never ran). Candidate additions to the table above:

| # | Fact | Stated on | Owner | Class |
|---|---|---|---|---|
| 12 | A subnet belongs to at most one space (a space has many subnets) | space.md:37 (context-record bullet, linked to `subnet`); subnet.md:30 (own record rule); captions excluded | subnet.md | near-verbatim, but the space.md copy is the recipe's context-record pattern (the bullet explains the figure's box; session-93/99 precedent) — no fix |
| 13 | A migration copies spaces and subnets except `alpha`; each subnet is linked to its space through the former ID; a Kubernetes model arrives with the two catch-all subnets | space.md:180-181; subnet.md:122-124 | split: `alpha` is a space fact (space.md); the former-ID link and the catch-alls are subnet facts (subnet.md) | variant/partial; each page keeps its own one-paragraph migration exception (recipe §1) — no fix |
| 14 | The Kubernetes catch-all subnets `0.0.0.0/0` and `::/0` | space.md:84 (reload rule), space.md:181, subnet.md:124 | subnet.md | variant, recorded only |
| 15 | Unit- and machine-agent definitions | link-layer-device.md:90 (calls intro) | unit.md (`unit-agent`) | recipe-compliant per the calls-intro rule (session 93) — no fix |
| 16 | The subnet↔zone link record | subnet.md:43 (linked to `zone`); zone.md:31-34 (owner, links back to `subnet`) | zone.md | properly linked both ways — no fix |

No-link sentences (recorded, not fixed — the linking sweep is the user's call): space.md:138, :167 (the constraint entity, no `{ref}` to `constraint`); subnet.md:108, :109 (same); link-layer-device.md:168 ("space constraints", no link). zone.md links its constraint and placement-directive mentions (`constraint-zones`, `placement-directive-zone`, zone.md:66-67). Pair coverage: all six pairs of the cluster checked; no subject overlaps beyond the recorded ones.

Checker baselines (session 100): agent.md 0 findings after the TITLES map gained "agent facades" and "agent kinds" (the two known unmapped-title findings resolved — `tools/check_page_rules.py`); space, zone, link-layer-device 0; subnet.md 1 pre-existing false positive at :125 (byte-identical to HEAD, last touched `824a5d8cd2`): the OXFORD heuristic matches "subnets, `0.0.0.0/0` and `::/0`", an appositive comma before a two-item list, not a missing Oxford comma (space.md's comma-free parallel sentence checks clean). No fix.

## Coverage

**21 of the 35 entity pages swept** (clusters 1-6): machine, unit, application, model, cloud, credential, relation, charm, offer, controller, user, secret, secret-backend, storage, ssh-key, ssh-server, lease, space, subnet, zone, link-layer-device (cluster 6 in-session, session 100). **Never swept (14):** action, agent-version, annotation, resource-charm, constraint, controller-upgrade, database, external-controller, high-availability, image-metadata, model-defaults, model-migration, object-store, telemetry. Strongest unswept pairs: constraint↔machine/application (constraint vocabulary), model-migration↔model/external-controller (migration stream), high-availability↔lease (the singular-controller lease). Several of the 14 are list or concept pages, not pair-dense entity pages.
## Session 102: the 14 never-swept pages (clusters A-C; A and B from read-only scouts, C in-session after two 402s)

Coverage: cluster A (constraint, action, agent-version, annotation, resource-charm — `SweepConstraintAction`), cluster B (model-migration, model-defaults, external-controller, controller-upgrade, database — `SweepMigrationStream`), cluster C (object-store, telemetry, image-metadata, high-availability — in-session). All 35 entity pages are now swept.

### Verified no-link rows (fixed by the linking commit)

- model-migration.md:43/:59 (offer), :46 (user, credential), :53 (user); controller-upgrade.md:14/:43/:88 (agent); action.md:40 (object store, gloss restates the owner's lede); resource-charm.md:57 (object store, wrong gloss "controller's store of blobs"); controller.md:118 (lease, gloss restates the owner's lede); high-availability.md:17 (controller, application), :94-98 (lease; "See the appropriate documentation" replaced by the link).

### Rejected rows (with evidence)

- database.md:119 "charm_<charm name>": the name is inside a code span (quoted-string exclusion); no link possible without breaking code font.

### Recorded only (duplicate-fact candidates, not fixed — record restructuring across pages, needs review)

Cluster B: model-migration.md owns the migration record set (export/migration-phase/minion/status/target-auth/redirect/redirect-user/exported+imported offer) vs model.md:41/:43/:225 restatements (near-verbatim/partial); controller-upgrade.md:75 stream values vs agent-version.md:31 (near-verbatim); model.md:162 cloud/region not-found errors vs model-defaults.md:57/:72-73/:87 (variant); model.md:147 superuser-defaults rule vs model-defaults.md:52/:66/:82 (partial).
Cluster A: constraint.md:134 merge rule vs machine.md:97-98 (near-verbatim); constraint.md:231-232 merge/precheck errors vs machine.md:112-113 (near-verbatim); constraint.md:186 whole-set replace vs application.md:337/:343 (variant); constraint.md:195 subordinate-no-constraints vs application.md:220/:237 (variant, application owns); action.md:40 vs resource-charm.md:57 object-store glosses (variant); action.md:135 change-block gloss vs restrict-commands anchor (variant).
Cluster C: controller.md:118 vs high-availability.md:94-98 singular-controller-lease holder restatement (variant; fixed the links, the fact keeps two homes — controller.md owns the primary-worker fact, lease.md the claim fact); image-metadata.md:38/:62 `image-stream` plain code (mixed key-linking convention; record); control-socket glosses plain on telemetry.md:10/:46, object-store.md:57/:64/:68, ssh-server.md links its key (no owner page; record).

### Pairs checked clean

external-controller↔offer/model (its record bullets link), telemetry↔log (log.md:103 links telemetry), object-store↔agent-version (mutually linked), image-metadata↔cloud/machine/model (lede links all), high-availability↔scaling (linked), annotation↔entity kinds (record bullets link model/application/charm/machine/unit/storage), agent-version↔machine/unit (links), database↔charm (record bullets cite pages), constraint↔space/subnet/zone (linked, session-100 record).
