# Placement triples for the facts in the draft

Triple: source artifact class | owner entity | audience question | home chosen. "Decided by": R = the rules decided; J = I judged.

Source classes used (the contract and the recipe name DDL, watchers, facade; this page has none of those as owner, see notes.md): service rule (domain service), worker behavior (uniter), hook command definition, client rendering (cmd), status constants (core/status).

| Fact (draft #) | Source class | Owner | Question | Home | Decided by |
|---|---|---|---|---|---|
| Status = value, message, time (1) | status constants | status (value type) | T1 | Lede | J (no rule for a value type; R18 grammar assumes an entity with DDL) |
| One app status, two unit statuses (2, 3) | service rule | application, unit | T1 | Lede | J |
| App status set vs derived (5) | service rule | application | T6 | Application status | R17 (the reader's question: what do I see for my application) |
| Leader sets app status (6) | hook command definition | hook command status-set; subject: application | T1 (who may) | Application status, with link | R12/R17: the command syntax belongs to the hook command page; the "who may" to the status page |
| Severity order, ties, message, no-units (7-12) | service rule | application | T10 | Application status | R17 |
| Two parts of a unit status (13) | service rule | unit | T6 | Unit status | J |
| Charm-settable set of four; juju sets three (14, 15) | hook command definition + uniter | workload status | T1 | Workload status lede and "Set by" column | J: the same fact is partly the hook command's (accepted values). I state it once here and link the command. R16 says one source; the hook help text also carries it (F29). Not decided |
| Meanings of the seven values (16-25) | status constants + hook help + uniter | workload status | T6 | Workload table | J (F29) |
| New-unit startup sequence (26-29) | uniter + domain/application | unit | T2 | Workload status of a new unit | J: could be in the unit page (lifecycle). Chose the status page because the question is "which statuses follow which" (T2), R21 says transitions live in the call that changes them, but there is no call; the startup is a worker behavior |
| Kubernetes pod override (30-33) | service rule (domain/status) | unit | T6 | Workload status of a Kubernetes unit | J |
| Meanings of six agent values (34-40) | status constants + uniter + presence | unit agent | T6 | Agent status | R17 |
| Hook failure shown as idle + error (41) | service rule (display) | unit | T6 | Agent status (last sentence) | J: crosses both statuses. It could sit under Workload `error`; it is stated in both places (row for `error` states the trigger, this sentence states the agent side). A repeat of one fact; I accept it because a reader entering from one section needs it (R16 exception for an isolated reader) |
| Columns in juju status (42) | client rendering | client (juju status) | T6 | Status in client output | R24 (CLI as example, after the platform fact) |

Summary: of 13 rows, the rules decided 5 (R17 three times, R12/R17, R24); I judged 8. The recipe's entity grammar (R18) has no slot for a value type or for a worker behavior (Q3 says the same). This is the contract's main placement gap for this page.
