# Placements: one line per fact

Columns: fact | source artifact class | owner entity | audience question | chosen home | decided by. "Rules" means the cited requirement or ledger row decided it alone. "Judged" means I chose between layouts that the rules leave open (R14 tie, or two rules that conflict).

Source artifact classes used: DDL (schema file), facade (apiserver method), service (domain service or state code), worker (internal worker), core type (core package), config (bootstrap or model configuration), doc.go or help text, upstream doc.

| # | Fact | Source class | Owner entity | Audience question | Home | Decided by |
|---|---|---|---|---|---|---|
| 1 | A relation connects two endpoints of different applications; peer has one | core type (`core/relation/doc.go`), DDL | relation | T1 | Lede | Rules (R18 lede; definition first, ledger "Definition as the opening sentence") |
| 2 | ID unique, from a model sequence, never reused | DDL (unique index), doc.go | relation | T1, T8 | Schema, Relation bullet | Rules (R20: a unique index stays in the schema) |
| 3 | Key format: requirer first, provider second; peer one endpoint | core type (`key.go`) | relation | T8 | Schema, Relation bullet | Judged: the key is derived, not stored, so R20 does not place it; "a fact about a record goes in its bullet" (recipe) |
| 4 | Life alive/dying/dead | DDL (`life` table) | relation | T2 | Schema, Relation bullet | Rules (R21: allowed values in the schema) |
| 5 | Transitions of the relation status | service (`status.go`) | relation | T2 | Setting the relation status | Rules (R21) |
| 6 | Status values and meanings | DDL, core type comments | relation | T6 | Schema, Relation status bullet | Rules (R21) |
| 7 | Who sets `joined` | worker (`statetracker.go`) | unit agent, relation | T2 | Setting the relation status, Caller line | Judged: the setter is a worker, not a facade (contract "Not settled" (c): no single call changes statuses); I placed it with the call that stores the status |
| 8 | Kinds: scope container or global | service (`addRelation`), DDL | relation | T1 | Relation kinds | Judged: recipe says a kind decided by records goes in the schema bullet; R15 and the inbound links (`subordinate-relation`, `non-subordinate-relation`, `cross-model-relation`) keep a section for each kind. Two rules conflict (recipe against R15); I followed R15 |
| 9 | Subordinate units are created per principal unit entering scope | service (`EnterScope`) | relation | T1, T2 | Relation kinds (subordinate) and Entering a relation scope | Judged: the consequence is a kind's meaning (kinds) and the mechanism is the call; I stated the consequence once in each, in different words, which R16 allows only when an isolated reader needs it (unproven). Duplicate risk recorded |
| 10 | Two subordinates can be related | service | relation | T1 | Relation kinds (subordinate) | Rules (R7: a charm author can meet it) |
| 11 | Compatible bases for container-scoped relations | service | relation | T3, T4 | Kinds (subordinate) and Adding relations rules | Judged: same as 9 |
| 12 | Relation unit | DDL | relation | T1 | Schema | Rules (R20) |
| 13 | Unit and application settings rules (non-empty, unique keys) | DDL (checks, PK) | relation | T8 | Schema | Rules (R20) |
| 14 | Settings total size 16 MiB | service/quota | relation | T9 | Writing relation settings | Rules (R20: a service check goes to the call) |
| 15 | `ingress-address` and `egress-subnets` set by Juju | service/facade | relation | T1 | Entering a relation scope and Writing relation settings | Judged: written at enter scope and protected at write; two calls state two different facts, so it is not a duplicate |
| 16 | Leader-only application settings: read and write | service (`LeadershipService`), facade | relation | T1, T3 | Reading and Writing relation settings | Rules (R19, R21): the rule constrains each call |
| 17 | Departed unit settings kept until relation removal | DDL comment, service | relation | T1 | Schema (record) and Reading relation settings (observable effect) | Judged: R20 test "reader meets it through a documented read" holds for the read call; the record holds the lifetime |
| 18 | Implicit `juju-info` endpoint definition (name, role, interface, scope) | service/state (`encodeJujuInfoRelation`) | application endpoint | T1 | Relation: one subsection; `application.md` defines the endpoint too | Judged, tie (R14, R16). Upstream states it on both pages; I kept the facts on the relation page because the subordinate attachment depends on them, and linked `application.md`. A reviewer could also say "one home: application.md" |
| 19 | How a subordinate attaches through `juju-info` | core type comment, service | subordinate relation | T1 | Relation kinds, `juju-info` subsection | Rules (R17: the reader's question decides) |
| 20 | Ambiguity when several pairs match | service (`inferEndpoints`) | the Adding relations call | T3 | Adding relations (error) and `juju-info` subsection (the case where it occurs) | Judged: Q5 (multi-place error); the entry is single-call, so R19 puts it at the call; the subsection keeps the cause as a rule of the subordinate attachment |
| 21 | Cross-model: remote application, offering and consuming model | service (`crossmodelrelation`) | relation, offer | T1 | Relation kinds, cross-model subsection | Judged: `offer.md` owns offers (R17); the relation page owns what a remote application is in a relation. Layout tie (R14) |
| 22 | Remote application names `remote-<uuid>` | core type (`name.go`) | remote application | T1 | Cross-model subsection | Rules (R7: visible in status of the offering model) |
| 23 | Cross-model restrictions (no peers, not both remote, suspend only, CIDRs, subordinate units) | facade, service | relation | T1, T3 | Cross-model subsection (as rules) | Judged: each also appears as an error or rule in a call (suspend rule at suspending; both-remote at adding). The subsection states them as properties of the kind, the calls as preconditions. Duplicate risk recorded (R16) |
| 24 | Controller bootstrap keys and their effect | config (bootstrap) | controller / bootstrap config | T4 | One sentence in cross-model subsection, link to the bootstrap configuration | Rules (R12: an interface's selector belongs to the interface; R17) |
| 25 | `saas-ingress-allow` | config (model) | model configuration | T4 | One sentence, link | Rules (R12, R17) |
| 26 | Firewall behavior of provider and requirer | worker (`firewaller`) | relation, firewall | T4 | Cross-model subsection | Judged: the firewaller worker is an actor; R18 has no actor slot (Q3). I wrote the behavior in the kind section |
| 27 | Adding relations: rules and 12 errors | facade, service | relation | T3, T8 | Adding relations | Rules (R19) |
| 28 | Removing relations | facade, removal service | relation | T3, T5 | Removing relations | Rules (R19) |
| 29 | Suspending relations | facade, service | relation | T3 | Suspending and resuming relations | Rules (R19) |
| 30 | Permission denied for a user without write access, change and remove blocks | facade | relation, model | T3 | Not written | Judged and open (Q5: multi-call, multi-facade). The Caller line states the rule |
| 31 | Unit agent definition | doc recipe | unit agent | T1 | Calls opener | Rules (recipe) |
| 32 | What happens to relations in model migration | modelmigration code | relation | T5 | Not written | Open(T5): not read |
| 33 | Peer relation created at deploy | doc.go, service | relation | T1 | Peer relation subsection | Rules (R7) |
| 34 | Hooks that peer, subordinate and regular relations fire | worker, hook docs | hook | T1 | `hook.md` (link only; not on this page) | Rules (R17) |
| 35 | HA through peer relations | none | high availability | T1 | Dropped | Rules (Quality) |
| 36 | `juju integrate` command syntax | CLI help | `juju integrate` page | T1 | One example in the `juju-info` subsection; syntax stays with the CLI page | Rules (R24: platform first, client as an example) |
| 37 | The status column "regular/peer/subordinate" | CLI formatter | `juju status` page | T6 | Not written (client output; R24) | Rules (R24, T6 note in contract) |
| 38 | Relation status shown by a client | CLI/facade | status page | T6 | Not written; the relation page states values and meanings only | Judged: contract T6 sends client output to the client page; the platform meaning is on the relation page |
