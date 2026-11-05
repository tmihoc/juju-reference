"""Ledger rows for E40 (pre-registered in structure-discovery-plan.md).

Each row: id, claim, skel (skeleton-v5.md line numbers that state or rely on
it), plan (inclusive line ranges of structure-discovery-plan.md that carry the
evidence), nums (strings that must occur in those plan lines), status, basis
(code, judge, precedent, user, convention), strength (what the basis is, as
recorded), crit (registered criterion and outcome; post hoc readings are
labelled), dep (claim ids), verified (code checks made while building the
ledger, with file and line), note.

status: supported | partial | falsified | open | withdrawn | convention | user
"""

ROWS = []


def R(id, claim, skel, plan, nums, status, basis, strength, crit="", dep=(),
      verified="", note=""):
    ROWS.append(dict(id=id, claim=claim, skel=list(skel), plan=list(plan),
                     nums=list(nums), status=status, basis=list(basis),
                     strength=strength, crit=crit, dep=list(dep),
                     verified=verified, note=note))


# ---------------------------------------------------------------- spine
R("C01",
  "Over 36 domains only state is present everywhere, and the domains have 28 "
  "distinct part sets, so a page prints a part only when its artifact class "
  "is non-empty (parts are conditional, not typed templates).",
  [7, 56], [(1095, 1095)], ["28 distinct part sets", "9 of 11"],
  "supported", ["code"], "census over 36 domains of 4.1 (E19)",
  "E19 registered bands: met 9 of 11 (dynamics 89% just under the 90% spine "
  "line, status 17% rare, not conditional)")
R("C02",
  "Typed templates fit poorly: the schema typing that predicts the removal, "
  "watch and migration parts best needs 10 types for a mean leave-one-out "
  "accuracy of 81%.",
  [7], [(1084, 1084)], ["10 types", "81%"],
  "supported", ["code"], "36 domains, leave-one-out (E17b)",
  "E17b registered: accuracy criterion (85%) and parsimony (8 types) both "
  "failed; the claim is the description of that failure, not a pass")
R("C03",
  "For topics that earn a page, interface is present in all and dynamics and "
  "failure in 93%; observation, agent, removal, status, configuration and the "
  "migration exceptions are conditional; the spine (identity, state, "
  "interface, dynamics, failure) was non-empty in 15 of 15 topics of three "
  "pre-registered fit tests on unseen topics.",
  [8], [(1128, 1128), (1165, 1165), (1196, 1196), (1308, 1308)],
  ["interface 100%", "5 of 5", "pass, 5 of 5"],
  "supported", ["code", "judge"],
  "E19b census n = 15 (post hoc cut, chosen after seeing E19 and E21); "
  "replicated by three registered agent fit tests (E21b, E21c, E21d), each "
  "one agent, findings spot-checked",
  "E19b not registered (post hoc)")
R("C04",
  "A life column in the model schema implies a removal job in 6 of 6 domains, "
  "and a watched table predicts Watch* methods in 89% against a 58% "
  "baseline; scope (controller, model or both) and life together are "
  "readable from the schema.",
  [8, 47], [(1075, 1078), (1084, 1084)], ["89%", "6 of 6", "75%"],
  "partial", ["code"], "36 domains (E17, E17b)",
  "E17 R1 pass (89%); R2 as registered FAILED (6 of 8 = 75%, limit 90%); the "
  "6 of 6 reading by schema scope is POST HOC; E17b: B beats A on removal and "
  "migration, accuracy and parsimony criteria failed")
R("C05",
  "Table-level typing (life, status, watched, immutable, lookup) is a "
  "version-stable function of the net schema, exact in both directions; "
  "domain typing is stable with schema-topic ownership.",
  [8], [(1028, 1033), (1089, 1089)],
  ["62 of 65", "11 own no changed or added table"],
  "partial", ["code"], "4.0.15 against 4.1 DDL, replayed in SQLite (E15, E15b)",
  "E15 registered criterion FAILED as a whole (a, b, c pass; d and e fail, "
  "d ill-posed, e is Go ownership); E15b passed")
R("C06",
  "Model tables migrate by a generic export; an entity names only the data "
  "that is filtered, remapped or prechecked; presence of a modelmigration "
  "package measures the legacy import, not a migration facet.",
  [8, 33, 42, 50], [(1125, 1125)], ["215"],
  "partial", ["code"],
  "spot-check of domain/export/state/model/export.go: at least 215 of 250 "
  "model tables appear as FROM targets; the other 35 were not checked",
  "E17b migration target (64% against 61%) measured a legacy package")
R("C07",
  "The page unit is a noun of the exposed interface.",
  [9, 54], [(1100, 1100), (1116, 1116), (1170, 1170), (1342, 1342)],
  ["15 of 15", "20 of 21", "14 of 15"],
  "falsified", ["code", "precedent"],
  "E20 and E20c count nouns of existing pages (precedent); E20b a weak test; "
  "E33 I3 uninformative",
  "E20 passed, then its exposure measure was shown to undercount (E20 "
  "correction); E33 R1 (first-token page unit) FAILED I2 (37% flagged) and "
  "E33b (writer domain) failed; superseded by the reviewed manifest and the "
  "weak-table rule (C50, C51, C58)", dep=["C50", "C51", "C58"])
R("C08",
  "A page may draw on several domains and a domain may carry several pages; "
  "tables with several owners are associations whose name picks one owner.",
  [9, 36], [(1225, 1225), (1167, 1167)], ["11 of 11"],
  "supported", ["code"],
  "E29 C2 pass, 11 of 11 multi-owner tables (name picks an owner); ssh keys "
  "span four domains, space/subnet/zone share one table set (E21b)")
R("C09",
  "Topics with only internal artifacts (no client, cross-process, CLI, "
  "hook-tool or HTTP artifact) get no page.",
  [9, 54], [(1155, 1155), (1269, 1269), (1342, 1342), (1359, 1360)],
  ["24 of 24"],
  "open", ["code", "user"],
  "E33 I3: by call graph every group of at least 3 tables is client-reached "
  "(24 of 24), so the rule cannot exclude anything",
  "the rule is consistent but non-discriminating with the measures built so "
  "far; the db shell was ruled user-facing (user, 2026-10-20)",
  dep=["C60"])
R("C10",
  "Statements on a page must come from the code through a gate: 94% of the "
  "claims of four hand-written pages are code-decidable, 29% of the "
  "conceptual ones fail scrutiny, the failing share of eleven unseen pages is "
  "28% among decidable claims.",
  [10, 53], [(1003, 1004), (1202, 1203)], ["94%", "41 of 148", "29%"],
  "partial", ["judge"],
  "E14 five judges with a larger budget (61 of 61 citations resolve); E27 "
  "four judges, 142 of 142 citations resolve, 5 of 12 failing verdicts "
  "re-read and held",
  "E13 registered criterion (80% derivable) FAILED; the 94% decidable is a "
  "re-count after E14 (depth artifact, labelled); E27 criterion 1 (8 to 25%) "
  "FAILED upwards")
R("C11",
  "Human-written entity reference pages carry almost no code identifiers, so "
  "an identifier-reach generator test is underpowered.",
  [10], [(1059, 1059)], ["18 atoms"],
  "partial", ["precedent"], "counts over existing pages (E16)",
  "E16 gave no verdict (fewer than 40 atoms in the code)")
R("C12",
  "Statements fall into separable kinds (identity, interface, state, "
  "dynamics, agent, observation, failure) with blind inter-rater kappa "
  "0.87 to 0.93.",
  [11], [(893, 893), (936, 937)], ["kappa 0.87", "kappa 0.93"],
  "partial", ["judge"],
  "two LLM raters of the same family (E7 to E10); measures reliability of "
  "the labels, not that readers need them",
  "E7 to E10 criteria met; caveat recorded: same model family, CLI pages "
  "inflate interface")
# ---------------------------------------------------------------- parts
R("C13",
  "Identity states how an entity comes into being and goes away; over 36 "
  "domains four kinds recur (life column 8, deleted by an operation 19, "
  "expired 7, append-only or cascade 9), and E29b adds a fifth (deleted when "
  "its last referrer goes).",
  [17, 30], [(1146, 1146), (1234, 1234)],
  ["life-column 8, deletable 19, pruned 7, append-only 9", "fifth lifecycle kind"],
  "partial", ["code"], "regular-expression census (crude by design)",
  "E24 prediction held; class membership needs a manual read before it goes "
  "on a page. Skeleton line 17 says four kinds, line 30 five: internal "
  "contradiction")
R("C14",
  "Topic labels (entity, facet, mechanism, vocabulary) are not inputs to any "
  "rule: facets have interface, dynamics and failure, and the label cannot be "
  "derived from facts for credentials and charm resources.",
  [30], [(1284, 1287)], ["3 of 3", "3 of 5", "0 of 36 empty"],
  "supported", ["code", "judge"],
  "T1 from agent counts (E21b, E21c), T2 fact rule against hand types from "
  "one agent round plus the author, T3 weak by selection",
  "E31 registered: T1 pass, T2 confirmed (the label is not a function of the "
  "facts), T3 pass but weak")
R("C15",
  "Identity names the entities it attaches to ('applies to') when at least "
  "three entities carry tables of its noun or a table attaches by foreign key.",
  [30], [(1178, 1178), (1183, 1183), (1330, 1330)],
  ["4 of 7", "22 tokens"],
  "partial", ["code"],
  "E26 failed (foreign-key fan-out cannot see facets: annotation rank 14 of 36)",
  "E26b passed (4 of 7 candidates real); E33 R4 as registered did not "
  "discriminate (22 tokens, about 4 real) and R4-prime was added POST HOC; "
  "the rule has no validated implementation")
R("C16",
  "State lists tables, lookups with allowed values, views, derived "
  "attributes, invariants tagged by enforcement site, and explicit transition "
  "tables, which exist only for migration phase and relation, volume and "
  "filesystem status; life moves are guarded by a monotonic trigger on 11 of "
  "the 15 life tables that forbids only backward moves.",
  [18, 40], [(975, 975), (1309, 1309)], ["11 of the 15 life tables"],
  "supported", ["code"],
  "E11 and E21d; trigger count re-verified here against the 4.1 DDL",
  "", verified="experiments/e11/model.ddl: 15 tables with life_id, 11 "
  "trg_*_guard_life triggers (14 guard triggers in all), each "
  "`WHEN NEW.life_id < OLD.life_id`")
R("C17",
  "State prints the spelling of each lookup value per surface (storage, API, "
  "CLI), allowed values first.",
  [18], [(1136, 1136)], ["0 of 5"],
  "convention", ["convention", "precedent"],
  "E18b: where existing pages enumerate values they agree with the code, and "
  "they rarely enumerate",
  "E18b criterion FAILED (0 of 5 inaccurate against one third); no evidence "
  "either way for the per-surface spelling")
R("C18",
  "Each channel type (API facade, HTTP route, CLI, hook tool, local socket, "
  "charm metadata) has its own artifact source; HTTP routes are generated, "
  "not enumerated.",
  [19], [(1118, 1118), (1197, 1197), (1267, 1267), (1309, 1309)],
  ["13 HTTP routes", "19 HTTP handlers", "about 28"],
  "partial", ["code", "judge"],
  "route counts disagree across entries: 13 (E20b census), more than 6 more "
  "(E21c), about 28 (E21d red team), 19 handlers found (E30)",
  "'generated, not enumerated' is the supported part; 'at least 19' in the "
  "skeleton is not established. Whether channel types share one entry shape "
  "is untested (stated in E20b)")
R("C19",
  "Hook kinds (25 events delivered to charms) and the availability of hook "
  "tools by context (46 uses of ErrRestrictedContext) recur across topics and "
  "have no row in the skeleton.",
  [], [(1304, 1304), (1310, 1310)], ["25 events", "46 sites"],
  "partial", ["code", "judge"],
  "E21d agent, spot-checked; re-verified here",
  "E21d criterion 2 FAILED on exactly these; accepted as rows to add",
  verified="domain/deployment/charm/hooks/hooks.go: 25 hook kinds; "
  "internal/worker/uniter/runner/jujuc: 46 non-test uses of "
  "ErrRestrictedContext",
  note="Gap: skeleton v5.5 has not added these rows. Partial by the E40 rule (a registered criterion in the row was missed); the finding itself was checked against the code.")

R("C20",
  "A mutating method that writes an entity can live in another domain's "
  "service (the writer is not the owner); a table's writing domain does not "
  "give its page.",
  [20], [(1353, 1353), (1357, 1357)], ["22 of 35"],
  "partial", ["code", "judge"],
  "E33b: 22 of 35 audit-flagged tables land where the judge said (63%); "
  "application is credited with 61 tables",
  "E33b criterion 1 FAILED; the finding that the writer is not the owner is "
  "the reading",
  note="Partial by the E40 rule (a registered criterion in the row was missed); the finding itself was checked against the code.")

R("C21",
  "Observation in 4.1 has almost no client-facing content: Client.WatchAll "
  "and ControllerAPI.WatchAllModels answer not implemented and the model "
  "summary watchers answer not supported; its content is cross-process.",
  [21, 48], [(1149, 1150)], ["5 of 195"],
  "supported", ["code"], "census of client facades (E25)",
  "descriptive",
  verified="apiserver/facades/client/client/client.go:76-77 and "
  "apiserver/facades/client/controller/controller.go:550-554 return "
  "NotImplemented")
R("C22",
  "Streams are tiered by exposure (T1 client, T2 cross-process, T3 internal, "
  "T0 unreferenced) computed from the code; only T1 and T2 appear on a page.",
  [21, 48], [(972, 973)], ["T1/T2"],
  "partial", ["code"],
  "name and import based (E11), later a call graph (E30); both "
  "approximate",
  "E20 correction: the import measure undercounts. The machine and model "
  "tier findings were read by the author from watcher lists")
R("C23",
  "The Agent row ('manifold or worker keyed to the entity; consumers belong "
  "to the consumer's page') gives a right answer or a clearly flagged "
  "ambiguity in only 1 of 5 topics.",
  [22], [(1124, 1124), (1164, 1164), (1194, 1194), (1305, 1305)],
  ["clear in 1 of 5"],
  "falsified", ["judge"],
  "four agent fit tests (E21, E21b, E21c, E21d), single agent each, "
  "findings spot-checked in part",
  "E21d criterion 3 FAILED; ambiguous in four topics of E21, again in E21b "
  "and E21c; the row as written is not usable")
R("C24",
  "Whether an entity page has a failure part is undecided; errors are "
  "authored once under the rule or operation that raises them, and the "
  "lookup by message is one generated index keyed by what the client sees "
  "(facade code and message), not the Go constant text.",
  [23], [(1111, 1111), (1209, 1209), (1306, 1306), (1345, 1345)],
  ["386", "367 distinct strings"],
  "open", ["code", "user"],
  "E22 census (95% of strings map to one constant); E33 I5 finding; user "
  "instruction not to add error sections",
  "E21d criterion 4 FAILED as measured (proxy stricter than the rule; "
  "ambiguous criterion)")
R("C25",
  "Authority is stated for every operation as a value with a kind: required "
  "level (72% explicit), caller-scoped, owner by tag, none beyond login, "
  "inherited, or parameter-dependent; and the error-code mapping is optional "
  "and may repeat (SecretNotFound is mapped in at least 8 places).",
  [32, 41, 51], [(1141, 1141), (1306, 1306), (1198, 1198)],
  ["140 (72%)", "17 of 20", "at least 8 places"],
  "partial", ["code"],
  "E23 census of 194 methods and a sample of 20 read in full; E21d",
  "E23 criterion 1 (90%) FAILED, criterion 2 passed (17 of 20)",
  verified="apiserver/facades/client/cloud/cloud.go:529-533 ('Only "
  "controller admins can ask for an update to be forced'): authority "
  "depends on the Force parameter",
  note="Partial by the E40 rule (a registered criterion in the row was missed); the finding itself was checked against the code.")

R("C26",
  "Operation entries state the block kind chain: RemoveAllowed also checks "
  "the change block, DestroyAllowed checks destroy and remove (and change); "
  "block kinds are asymmetric (storage removal and detach, secrets and "
  "offers check none).",
  [32, 41, 52], [(1198, 1198), (1309, 1309)], ["RemoveAllowed"],
  "partial", ["code", "judge"],
  "the chain is the E21c agent's finding (plan line 1198), re-verified in "
  "the code here; the asymmetry (which operations check none) is the E21d "
  "agent's and not re-verified",
  "",
  verified="apiserver/common/block.go:59-90: RemoveAllowed checks "
  "RemoveBlock then ChangeBlock; DestroyAllowed checks DestroyBlock then "
  "RemoveBlock (the third check was cut off in my read, the E21c finding "
  "says it ends at the change block)")
R("C27",
  "A configuration key has one home, the entity it configures; per-key flags "
  "come from the key's own schema (that a missing flag is not printed is a "
  "convention, not a finding).",
  [24, 31], [(1123, 1123), (1163, 1163), (1166, 1166), (1309, 1309)],
  ["3 of the 5 topics"],
  "partial", ["code", "judge"],
  "no Mandatory, Secret or Immutable flag in controller/configschema.go "
  "(spot-check, E21b); keys without an owner recur in 3 of 5 topics (E21)",
  "E21d red team: the home rule needs a tie-break (storage pool "
  "attributes, the model secret backend setting, storage-default-block-source); "
  "the rule is untested on topics with keys (TODOS); registered criterion 2 "
  "FAILED in E21 (keys with no home recur in 3 of 5 topics) and in E21b "
  "(keys of a shared config)")
R("C28",
  "Provider and version scope are stated on the statement they qualify "
  "(applicability annotation), because hand-written pages state provider- "
  "or mode-dependent behaviour as universal.",
  [25], [(1202, 1203)], ["41 of 148"],
  "convention", ["convention", "judge"],
  "E27 reading (post hoc): failing share highest on provider-dependent pages",
  "E27 criterion 1 FAILED upwards")
R("C29",
  "Hard ordering constraints: identity first; state before dynamics and "
  "failure; dynamics before failure.",
  [27], [(941, 941), (1153, 1153)], ["44 presupposition pairs"],
  "partial", ["judge"],
  "44 presupposition pairs from LLM raters (E10); reader test cannot "
  "separate orders (E9)",
  "no registered criterion on order; closed as a convention")
R("C30",
  "Beyond the hard constraints, the order is the causal chain: records, "
  "change streams, agent, operations, then configuration and the failure "
  "index.",
  [27], [(1153, 1153)], [],
  "user", ["user"], "decision of the user, kept as a convention",
  "the evidence neither supports nor contradicts it")
R("C31",
  "The generic export has an exclusion list (at least 15 tables are excluded "
  "from the generic import, among them charm hashes, agent binaries and "
  "object store tables moved by HTTP), the legacy 3.6 import registers one "
  "operation per domain, and import operations have ordering dependencies.",
  [33, 42], [(1164, 1164), (1198, 1198), (1309, 1309)], ["at least 15 tables"],
  "supported", ["code", "judge"],
  "E21b and E21d: legacy registrations and generate/modelimport/main.go:86-100 "
  "spot-checked",
  "")
R("C32",
  "State lists seeded rows and synthetic keys (the alpha space, the reserved "
  "key comment, view-added keys).",
  [34], [(1163, 1163), (1518, 1518)], ["alpha"],
  "supported", ["code", "judge"], "E21b agent and E39 Z5 (space has a seeded alpha row)",
  "")
R("C33",
  "Removal takes one of three paths (life column and removal job; removal "
  "job without a life column; deletion by cascade or operation), and every "
  "entity states it.",
  [35, 49], [(1075, 1078), (1197, 1197), (1447, 1447), (1451, 1452)],
  ["6 of 6", "subnet and zone have no remove operation at all"],
  "falsified", ["code"],
  "E17 post hoc, E21c, E37",
  "'for every entity' is contradicted: in 4.1 subnet, zone and storage pool "
  "have no removal operation (C48), and E29b adds a fifth kind (deleted when "
  "its last referrer goes)", dep=["C13", "C48"])
R("C34",
  "Operation, task and action are one table set (ten operation tables; the "
  "action declaration is the charm's) and one noun reached by the Action "
  "facade; the page unit spans two table groups.",
  [36], [(1241, 1241), (1271, 1271)], ["10 tables"],
  "supported", ["code"], "E29d and E30 K4",
  "")
R("C35",
  "The parts are closed and the entries are open: the exposed artifacts fit "
  "a part in 94.5%, about 95%, 98.6% and 96.9% over four rounds; sub-kinds "
  "that recur across topics appeared in rounds 1, 2 and 4 and not in round 3.",
  [39], [(1121, 1121), (1161, 1161), (1191, 1191), (1302, 1302), (1310, 1310)],
  ["94.5%", "98.6%", "96.9%"],
  "partial", ["judge"],
  "four agent fit tests, 20 topics, one agent each, findings spot-checked",
  "fit thresholds: E21 pass, E21b borderline FAIL, E21c pass, E21d pass; the "
  "no-recurring-gap criterion FAILED in rounds 1, 2 and 4 and passed in "
  "round 3")
R("C36",
  "Invariants carry an enforcement tag (schema constraint, trigger, service "
  "check, facade check, comment only), and a comment is never evidence of "
  "enforcement.",
  [40], [(1198, 1198)], ["last_polled"],
  "partial", ["judge", "convention"],
  "E21c agent, cited in its text and not re-verified",
  "")
R("C37",
  "A table shared by two topics (relation_status, status and relation) has "
  "one stated home with a pointer on the other page; the home of a table "
  "whose key contains a foreign key is its owner's page.",
  [43], [(1377, 1377), (1493, 1493), (1498, 1498)], ["142 of 153"],
  "supported", ["code", "judge"],
  "E38c weak-table rule plus E34 revised home-and-pointer rule",
  "",
  verified="experiments/e11/model.ddl: relation_status has relation_uuid as "
  "its PRIMARY KEY",
  dep=["C58"])
R("C38",
  "Facades whose methods all answer not implemented or not available are "
  "listed as unavailable, never as operations.",
  [43, 55], [(1149, 1150), (1445, 1445)], ["5 of 195"],
  "supported", ["code"], "E25 liveness census and E21d, E37",
  "",
  verified="apiserver/facades/client/storage/pool.go:218-226: RemovePool and "
  "UpdatePool return CodeNotYetAvailable")
R("C39",
  "Status is three things: per-entity status tables (12 tables ending "
  "_status, nine value lookups), a history log store (not a table), and the "
  "full-status read model.",
  [44], [(1194, 1194), (1242, 1242), (1191, 1191)], ["nine value lookups"],
  "supported", ["code"], "E21c, E29d",
  "",
  verified="experiments/e11/model.ddl replayed in SQLite: 12 tables named "
  "*_status in the model schema; domain/status/service/statushistory.go "
  "holds the history")
R("C40",
  "Controller-scope lifecycle entities have no removal job type: the "
  "controller node is deleted as a step of removing the controller "
  "application's unit, and the object store backend's life column drives its "
  "drain while blobs are removed by path.",
  [49], [(1078, 1078)], ["domain/removal/service/unit.go:338"],
  "supported", ["code"], "E17 post hoc, checked against the code",
  "",
  verified="domain/removal/service/unit.go:338 deleteControllerNodeForUnit; "
  "domain/objectstore/service/service.go:402 RemoveMetadata(path)")
R("C41",
  "A guard that one entity imposes on other entities' operations (block "
  "commands) is stated once, on the page that owns it.",
  [52], [(1284, 1284)], ["3 of 3"],
  "convention", ["convention"], "E21, E31 T1",
  "")
R("C42",
  "The claim gate trusts code and never code comments; 'five contradictions "
  "found, E21'.",
  [53], [(1120, 1127)], [],
  "user", ["user"],
  "the principle is the user's (HANDOFF rule 6)",
  "the number five is NOT found in the plan, SESSIONS or the summary: "
  "unsourced, removed from the next skeleton",
  note="Number unsourced")
R("C43",
  "Skeleton v5.5 lists open questions: order of interface, observation and "
  "agent; the placement map page; the error index; the claim-gate prototype; "
  "whether the part inventory is shown to readers.",
  [58, 59], [(1153, 1153)], [],
  "open", ["convention"], "list of open items",
  "superseded in part by TODOS (queue and 'Needs the user')")
# ---------------------------------------------------------------- E29-E39
R("C44",
  "No mechanical grouping rule reaches 10% misplaced tables: first word "
  "(37% flagged, 71 of 192), writer domain (22 of 35 land right), schema "
  "file (26 of 33 strictly); the failures cluster in a few families.",
  [], [(1341, 1341), (1353, 1356)], ["71 of 192", "22 of 35", "26 of 33"],
  "partial", ["code", "judge"],
  "E33 I2 judge used 12 tool calls; flags verified in code by sampling (all "
  "held); the schema-file probe was unregistered",
  "E33 I2 and E33b criterion 1 FAILED; the 26 of 33 is a POST HOC probe",
  note="Partial by the E40 rule (a registered criterion in the row was missed); the finding itself was checked against the code.")

R("C45",
  "A reviewed manifest (39 pages, 264 tables, one home each plus pointers) "
  "is the working page list: blind placement 255 of 264 with shallow judges "
  "and descriptions, 243 of 264 (92.0%) with page names only and deep "
  "judges; adversarial audit 7 of 264 misplaced after verification; 22 of "
  "23 existing pages map.",
  [], [(1374, 1375), (1376, 1376), (1379, 1380), (1571, 1579)],
  ["255 of 264", "7 misplaced tables of 264", "12 of 16", "22 of 23",
   "243 of 264", "263 of 264"],
  "partial", ["judge", "code", "precedent"],
  "E34 M1 judges used 4 and 8 tool calls; E42 two judges cite file and line "
  "for 264 of 264 placements (263 mechanically found near the table name); "
  "M2 flags and the 4 open E42 cases verified in code; M5 is agreement with "
  "precedent",
  "E34: M1, M2, M5, M6 pass; M3 below one partition (explained); M4 FAILED "
  "(12 of 16, new nouns need review); E42 (registered) met: agreement above "
  "85%, one manifest error (0.4%) by the weak-table rule, 17 of 21 "
  "disagreements decided by that rule for the manifest",
  verified="application_remote_offerer_relation_macaroon has "
  "PRIMARY KEY relation_uuid (a weak table of relation, manifest home "
  "offer); block_device is referenced by storage_volume_attachment "
  "(0011-storage.sql:327); model_namespace is deleted with its model "
  "(domain/removal/state/controller/model.go:424)",
  note="One manifest error by the key rule remains (the macaroon table); "
  "two tables have two defensible homes (block_device, model_namespace)")

R("C46",
  "Association tables have one home and are shown on the other page by a "
  "pointer; 18 such tables were found by the audit.",
  [], [(1377, 1377)], ["18"],
  "partial", ["code", "judge", "precedent"],
  "the audit judge's 18 association tables, adjudicated against the code; "
  "the home follows the table name where it picks an owner (E29 C2) and the "
  "existing page structure otherwise (precedent)",
  "E34 H ('exactly one home per table') was NOT met and was REVISED after "
  "M2 (home plus pointer); the revision is post hoc and untested")
R("C47",
  "A mechanical definition of 'character' (own address, identity, "
  "referenced elsewhere) is falsified; a reader's rubric (own address, "
  "identity, own create and remove operation, referred to by name) labels "
  "22 of 39 pages characters and 10 legs, and a second reader with the "
  "metaphor removed agrees on 38 of 45 items (84.4%).",
  [], [(1397, 1407), (1586, 1591)],
  ["21 of 32", "27 of 32", "31 tool calls", "38 of 45", "6 of 6"],
  "partial", ["judge"],
  "two judges, same model family as the author: E35 31 tool calls with the "
  "user's metaphor and my page descriptions in its prompt; E43 names and "
  "tables only, four neutral labels, cites code for every item",
  "E35: predictions 1 and 3 FAILED, falsifier 21 of 32 (66%) FAILED; the "
  "27 of 32 (84%) variant is POST HOC. E43 registered criteria (1) 84.4% "
  "and (2) 6 of 6 controls met; the `own` definition excludes side-effect "
  "removal, the one place the two instruments are not independent",
  note="Level labels now rest on a judge pair, not on a judge alone; see "
  "C63 for the level agreed by three instruments")

R("C48",
  "In 4.1 subnet and zone have no remove operation, and a storage pool can "
  "be created but not removed through any interface.",
  [], [(1447, 1447), (1451, 1452)], ["subnet and zone have no remove operation at all"],
  "supported", ["code"],
  "E37 robust failures (absent paths are strong evidence under an "
  "over-approximating graph)",
  "",
  verified="storage/pool.go:218-226 (RemovePool not yet available); "
  "domain/network/service/subnet.go:70 RemoveSubnet has no non-test caller "
  "(grep of the tree); no DELETE FROM availability_zone outside the "
  "availability_zone_subnet link rows (grep)",
  note="Documentation corrections (TODOS 5): verify per page before use")
R("C49",
  "A unit's participation in a relation (EnterScope and LeaveScope create "
  "and delete relation_unit without touching the relation) and an "
  "application's endpoints (SetCharm) have lifecycles of their own, "
  "contradicting the judge's 'leg' verdict.",
  [], [(1444, 1444), (1450, 1450)], ["EnterScope"],
  "supported", ["code"],
  "E37 reading by operation name; passes may be side effects",
  "E37 negative controls: 4 of 6 failed the definition (needed 5)")
R("C50",
  "Kind, not size, decides the level of a primitive (page or anchored "
  "section): mass separates characters from legs with AUC 0.86, correlates "
  "with page length at 0.53 (mixed bands), and 20 of 22 characters have a "
  "lifecycle how-to against 0 of 10 legs.",
  [], [(1419, 1423)], ["0.86", "0.53", "20 of 22"],
  "user", ["user", "judge", "precedent"],
  "user position; kind labels from the E35 judge; how-tos are precedent, "
  "which the 2026-10-20 correction counts as weak",
  "E36: H1 survives by the registered rule because H2 was not supported; "
  "(1) and (2) are mixed, not H1-side")
R("C51",
  "The registered primitive definition (own key, independent creation, "
  "independent removal) holds for 27 of 39 groups; positive controls 9 of 9; "
  "passes are weak because side effects count, failures are robust.",
  [], [(1442, 1447), (1523, 1523)], ["26 of 39", "27 of 39"],
  "partial", ["code"],
  "call graph (1,817 roots) and schema keys",
  "E37 registered criterion NOT met (negative controls 4 of 6); 26 became "
  "27 after the E39 lead-table fix")
R("C52",
  "A table whose primary key contains a foreign key is a weak table and a "
  "section of its owner's page: 142 of 153 weak tables are homed with their "
  "owner, and a judge agrees on 17 of 20.",
  [], [(1492, 1498)], ["142 of 153", "17 of 20"],
  "partial", ["code", "judge"],
  "key parse verified against SQLite (E39 Z1, 0 of 344 differ); judge 10 "
  "tool calls",
  "E38c: predictions (1), (3), (4) and the judge criterion passed; (2) FAILED "
  "as registered (six annotation tables have a foreign key that the schema "
  "comments out)",
  verified="domain/schema/model/sql/0013-annotations.sql: the foreign keys "
  "of annotation_application, annotation_machine, annotation_storage_instance, "
  "annotation_storage_volume and annotation_storage_filesystem are commented "
  "out",
  dep=["C37"],
  note="Registered criterion (2) was missed, so partial by the E40 rule; the principle itself passed (1), (3), (4) and the judge check.")

R("C53",
  "A group whose lead table has a mandatory reference into exactly one other "
  "page and which no table of another page references is an anchored "
  "section of that page (12 of 45 chunks); the same key shape with "
  "dependents is a page.",
  [], [(1499, 1499), (1481, 1482), (1550, 1556)],
  ["port_range", "13 of 13", "12 sections and 33 pages"],
  "partial", ["code"],
  "E41 on the replayed 4.1 DDL; stable on 4.0.15 (13 of 13); no judge",
  "E41 registered predictions 5 of 5 and 10 of 10 met; check (b) questions "
  "four sections (permission, resource, ssh-key, model-migration); the "
  "association-dependent variant that fixes three of them is POST HOC and "
  "untested on held-out data; the rule cannot place telemetry, agent-version, "
  "zone, link-layer-device, external-controller, object-store (no mandatory "
  "owner)",
  verified="lead-table DDL of 12 section groups opened (permission.grant_on "
  "is an untyped string; port_range.unit_uuid NOT NULL; resource.charm_uuid "
  "NOT NULL but three other pages reference resource)")
R("C54",
  "The two storage directive tables belong with their owners (application "
  "and unit) by the weak-table rule, against the E34 audit that moved them "
  "to storage because the existing storage page documents them.",
  [], [(1375, 1375), (1495, 1495), (1497, 1497)], ["storage directives"],
  "partial", ["code", "judge", "precedent"],
  "E34 move rests on precedent (the existing page); E38c rule and judge "
  "(storage directives on application and unit) rest on keys",
  "by the 2026-10-20 correction, precedent does not decide; the E38c table "
  "moves are proposed, not applied (manifest v3); E38c criterion (3) passed "
  "with 2 tables flagged, both of them these",
  dep=["C52"])
R("C55",
  "The instruments are sound at the level the results use them: foreign-key "
  "parse 0 of 344 differ from SQLite, flags 0 of 1,032, write classification "
  "0 differ in insert, delete or update sets, call-graph recall 15 of 15 and "
  "precision 19 of 25, address match 4 of 38 wrong strictly.",
  [], [(1517, 1523)], ["0 of 344", "0 of 1,032", "19 of 25", "15 of 15", "4 of 38"],
  "partial", ["code", "judge"],
  "checks against SQLite, SQL text and a 135-tool-call judge; tests in "
  "experiments/e39/test_instruments.py",
  "E39: Z9 FAILED its 10% limit strictly (11%) and passed at 7.9% after the "
  "author's own truth error was corrected; not fixed because E35 is "
  "superseded",
  verified="python3 -m unittest -v test_instruments in experiments/e39: 8 "
  "passed, 0 failed",
  note="Z9 missed its registered limit strictly (11%), so partial by the E40 rule; the other instruments passed.")

R("C56",
  "The call graph over-approximates, and reach is mostly context: 14 of 19 "
  "confirmed pairs are reads and 13 incidental; it tells what a channel can "
  "touch, not what the channel is about.",
  [], [(1267, 1272), (1521, 1521), (1342, 1342)],
  ["24 of 26", "24 of 24", "135 tool calls"],
  "partial", ["code", "judge"],
  "E30 K1 to K4 passed but eight tuning changes were made after seeing "
  "results (criteria fixed before, choices not); the 14 reads and 13 "
  "incidental figures are one judge's (135 tool calls)",
  "E30 K2 passed with a reading; E33 I3: the measure does not discriminate "
  "at group level (a supplementary noun-addressing signal was added after "
  "seeing this)",
  dep=[])
R("C57",
  "Machine's generated ggarch data model matches the hand-written one "
  "(recall 11 of 11, precision 11 of 11 over shared nodes) and five more "
  "groups parse, so the model block of a diagram can be generated from the "
  "page's tables.",
  [], [(1335, 1337)], ["11 of 11"],
  "supported", ["code"], "one hand-written model, one ggarch tool (E33 I4)",
  "E33 I4 passed")
R("C58",
  "The weak-table rule gives the home of a table (weak tables go to the "
  "owner); the level of strong tables is not settled: C53 gives a rule that "
  "leaves six groups undecided.",
  [], [(1498, 1499)], ["manifest version 3"],
  "partial", ["code"],
  "follows from C52 and C53 (E41 gives the section rule for strong tables)",
  "E38c proposed table moves are 'proposed, not applied' (manifest v3)",
  dep=["C52", "C53"])
R("C59",
  "The ssh-key page written with the pattern fails 5 of 49 claims (10%, at "
  "the limit), four of the five by the author's own errors (two carried over "
  "from the old page unchecked, two generalisations across operations).",
  [], [(1297, 1299)], ["5 of 49", "47 of 49", "23 tool calls"],
  "partial", ["judge"],
  "one judge, 23 tool calls for 49 claims; true share probably higher",
  "E32 passed narrowly (limit 10%) against 28% on old pages (E27)")
R("C60",
  "The docs inclusion test counts the database shell (juju-db-repl) as "
  "user-facing, so data-model sections stay in docs/ (user decision).",
  [], [(1344, 1344), (1360, 1360)], ["2 of 49"],
  "user", ["user", "judge"], "user decision, 2026-10-20; the counts (2 of 49 "
  "claims of the ssh-key page internal only, 12 more shell-only) are one "
  "judge's, 24 tool calls",
  "E33 I5 passed under that instruction")
R("C61",
  "Candidate documentation corrections from the code: relation.md:89 (the "
  "bootstrap options are --config keys), the three E13 contradictions, the "
  "E27 failing list, pool removal, subnet and zone removal.",
  [], [(995, 995), (1108, 1108), (1203, 1203)], ["relation.md:89"],
  "open", ["code", "judge"],
  "each verified once by the author or a judge; none re-verified as a "
  "batch",
  "TODOS: verify each against the code before it goes into a page")


# Rule-(b) contradictions: a later entry changes a skeleton rule.
# (skeleton line, row id that changes it, what is wrong with the line)
CONTRA_B = [
    (9, "C07", "page unit by interface noun: E33 and E33b falsified the "
               "mechanical forms; the reviewed manifest and the weak-table "
               "rule replace it"),
    (54, "C09", "'no exposed artifact, no page' cannot exclude anything: "
                "every group of 3 or more tables is client-reached (24 of 24)"),
    (22, "C23", "Agent row is ambiguous in 4 of 5 topics (E21d) and has no "
                "replacement rule yet"),
    (35, "C33", "'removal is stated for every entity by one of three paths': "
                "subnet, zone and storage pool have none in 4.1; a fifth "
                "kind exists"),
    (49, "C33", "same rule repeated in the identity-gains list"),
    (17, "C13", "'four recurring kinds' against line 30's five"),
    (44, "C14", "uses the label 'facet' that E31 removed as an input"),
    (19, "C18", "'at least 19' HTTP routes: counts range from 13 to about 28 "
                "across entries; only 'generated, not enumerated' is supported"),
    (53, "C42", "'five contradictions found, E21' has no source in the plan"),
    (8, "C04", "'life column in the model schema implies a removal job, 6 of "
               "6' is a post hoc reading of a failed registered criterion"),
    (43, "C54", "one home for shared tables conflicts with E34's storage "
                "directive move; the weak-table rule decides it (owner page)"),
]


R("C63",
  "Of 33 page groups that have a page-or-section level in all three "
  "instruments (E35 judge, E43 judge, E41 rule), 23 agree (6 sections: "
  "machine-placement, application-scale, port, unit-state, model-defaults, "
  "cloud-instance; 17 pages); 10 split; 12 more are mechanisms, processes "
  "or concept pages with no level.",
  [], [(1586, 1591)],
  ["23 of 33", "10 split"],
  "partial", ["code", "judge"],
  "schema rule E41 plus two judges; concordance computed by "
  "experiments/e43/concord.py under the reading rule registered before the "
  "run",
  "E43 reading rule met by construction (agreement defined as the three "
  "labels equal); the 10 splits are two-way cases for the user",
  verified="subnet: RemoveSubnet has no caller outside tests (grep); "
  "zone: availability_zone is inserted only in the subnet upsert "
  "(domain/network/state/subnet.go:242) and no DELETE FROM availability_zone "
  "exists; charm: DELETE FROM charm only when no application or unit uses "
  "it (domain/removal/state/model/application.go:850-875); resource: own "
  "removal job (domain/removal/service/resource.go:25-60)",
  dep=["C53", "C47"])
R("C64",
  "permission is a concept page across entities (one access vocabulary "
  "attached to controller, model, cloud and offer, by user and untyped "
  "target), not a section of user.",
  [], [(1553, 1553), (1590, 1590)],
  ["grant_on"],
  "partial", ["code", "judge"],
  "E41 check (b) read the DDL (grant_on is an untyped string); E43 judge "
  "labels it across with high confidence and cites grant, revoke, "
  "modify-offer-access, cloud access; E35 judge said character (low)",
  "E41 rule says section of user and is blind to the second owner (the "
  "reading is labelled in E41); E37 shows independent create and remove "
  "operations",
  verified="experiments/e11/model.ddl permission: grant_to references user, "
  "grant_on is TEXT with no foreign key")
