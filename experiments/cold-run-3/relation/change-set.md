# Change set: `docs/reference/relation.md`

Format: `action | file and section | category | requirement | confidence`. Every line cites a finding. A change with no finding does not appear.

| # | Action | Section | Category | Requirement | Finding | Confidence |
|---|---|---|---|---|---|---|
| 1 | Rewrite lede: definition, endpoint multiplicity, ID, life, status | Lede | Reference | R18, R22 (definition first) | F1 | Determined |
| 2 | Correct: define subordinate by container scope; two subordinates allowed; scope set by endpoints | Relation kinds, Subordinate relation | Reference | R6, R12 | F2 | Determined |
| 3 | Delete HA claim | Peer relation | Reference | R16, Quality | F6 | Determined |
| 4 | Correct and move: bootstrap keys are Kubernetes `--config` keys; one sentence and a link | Cross-model relation | Reference | R12, R17 (owner is bootstrap configuration) | F11 | Determined |
| 5 | Correct figure text "regular"; state in prose which kinds a client calls regular | Relation kinds | Reference | R26, Quality | F3 | Determined |
| 6 | Drop both figures in this draft; restate each fact in prose. Rebuild with ggarch as a records view for the schema and a kinds view, with alt text carrying the inventory on both theme variants | Relation kinds, Relation database schema | Reference | R26 | F4 | Determined (figure dropped); open for the rebuilt view |
| 7 | Correct "every relation creates databags" | Relation database schema | Reference | R20, Quality | F5 | Determined |
| 8 | Correct precedence claim to the ambiguity rule | Implicit `juju-info` endpoint | Reference | Quality | F10 | Determined by reading; probe pending |
| 9 | Correct firewall rule; name `saas-ingress-allow` by link | Cross-model relation | Reference | Quality, R17 | F12 | Determined / open (consuming side) |
| 10 | Add cross-model rules: peers excluded, both-remote refused, only these relations suspend, `via` egress, one endpoint per remote application | Cross-model relation, Relation calls | Reference | R6, R19 | F13 | Determined |
| 11 | Merge "Relation identification" into the relation record; correct key format and ID facts | Relation database schema | Reference | R10 (two measures), R18 | F15 | Determined |
| 12 | Delete "local copy"; replace with the read calls | Relation calls | Reference | Quality | F16 | Determined |
| 13 | Add settings rules: Juju-written keys, empty values, 16 MiB cap, archive, leader-only application settings | Reading relation settings, Writing relation settings, schema | Reference | R19, R20 | F19 | Determined |
| 14 | Add status values (schema) and transitions (call) | Relation database schema, Setting the relation status | Reference | R21 | F22 | Determined |
| 15 | Add life values and relation scope | Relation database schema | Reference | R20 | F22 | Determined |
| 16 | Add calls with caller, rules, errors: add, remove, suspend/resume, enter scope, read and write settings, set status | Relation calls | Reference | R18, R19, R25 | F23 | Determined; codes open for six wrapped errors (notes, failure 4) |
| 17 | Add removal rules | Removing relations | Reference | R6 | F24 | Determined |
| 18 | Add relation migration | n/a | Reference | R18 | F24 | Open(T5): not read |
| 19 | Reduce `juju-info` section: keep subordinate attachment and ambiguity rule; link `application.md` for the endpoint | Implicit `juju-info` endpoint | Reference | R16, R17 | F9 | Tie on the home of the endpoint definition |
| 20 | Delete "cannot be declared", "not in `juju info` or Charmhub", "useful only for machine charms" | Implicit `juju-info` endpoint | Reference | Quality | Batch | Determined |
| 21 | Delete the persist-data advice, the example charms, the bare-metal scenario, the duplicate `ibnote` | Peer relation, Cross-model relation | Reference | R6 (minimality), R16 | Batch | Determined |
| 22 | Apply text rules: drop "Note that", "(i.e.,)", "+/-", "aka"; "settings" for "databag" | all | Reference | R22 | Batch | Determined; conflict with genre row (notes, conflict 1) |
| 23 | Keep labels `relation`, `peer-relation`, `non-peer-relation`, `subordinate-relation`, `non-subordinate-relation`, `cross-model-relation`, `the-implicit-juju-info-relation-endpoint`; add `relation-databag` and `permissions-around-relation-databags` as labels on the settings call sections | all | Reference | R15 | Batch (address check) | Judged: a label is invisible text, the heading words are not (notes, conflict 2) |

## Backlog (predates any development; not part of the change set)

- Rebuild the two figures (item 6) with ggarch. Cold run cannot build them.
- Probe item 8 on a 4.1 controller.
- Read `domain/relation/modelmigration` for item 18.
- Decide Q5 for errors that several calls raise (permission denied, change block).

## Examined and left unchanged

- L34 peer definition and L41 non-peer conditions: true; restated at their new homes.
- L93-95 remote application names: true; kept.
- L124-131 permission rules: true; kept as call rules.
