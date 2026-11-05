# Placements

Columns: fact; source artifact kind; owner entity; audience question; chosen home; decided by (rules = a stated rule decides; judged = I chose).

| Fact | Source kind | Owner entity | Question | Home | Decided by |
|---|---|---|---|---|---|
| A unit has workload and agent status; an application has one | status constants, domain service | unit, application | T1 | Lede | rules (Text: definition as opening sentence) |
| Status = value + message + time | core/status StatusInfo | status record | T1 | Lede | judged (could sit in Workload status) |
| Charm sets four values via `status-set` | hook-tool definition | unit workload status | T1 (who may) | Workload status | rules (Str: a call states its caller) |
| Juju sets error, unknown, terminated; waiting and maintenance at fixed points | uniter, domain service | unit workload status | T1, T2 | Workload status | judged |
| Meaning of each of seven workload values | status constants, hook-tool doc | workload status | T6 | Workload status table | rules (one home per fact) |
| error causes (hook, upgrade) and message form | uniter | unit workload status | T3 | Workload status table, `error` row | judged (the cause is a uniter fact; the display rule is a domain fact; both placed with the value) |
| unknown has two causes | uniter, domain service | workload status | T6 | Workload status table, `unknown` row | judged |
| Kubernetes pod can replace displayed workload status | domain service | unit display status | T6 | Workload status | judged (Q: own section) |
| Message shown and kept in history | hook-tool definition | status record | T1 | Workload status | judged |
| Agent values and meanings (six) | status constants, uniter | unit agent status | T2, T6 | Agent status table | rules |
| Agent status set by Juju; `status-set` sets only workload | hook-tool definition, domain service | agent status | T1 | Agent status | rules (Str: caller stated) |
| `lost` is controller-derived; effect on displayed workload | domain service | agent status, workload display | T3, T6 | Agent status, `lost` row | judged (effect crosses two owners; placed with its cause) |
| Hook failure shows workload `error` + agent `idle` | domain service | unit display status | T6 | Agent status (sentence) | judged (also touches the `error` row; one home, row links by wording) |
| Creation, init, install, start, stop, remove statuses in order | domain application, uniter | unit | T2, T5 | Unit life subsection | judged (T2 favors time order; Q: duplicate of table facts) |
| `status-set` call replaces status at any point | hook-tool definition | workload status | T2 | Unit life subsection | judged |
| Derived application status from unit severity | domain service | application display status | T10 | Application status | rules (chunk answers one question; Str one home) |
| Severity order of seven values | domain service | application display status | T10 | Application status (ordered list) | rules (a list needs an enumerated order; the literal reader reads silence as nonexistent) |
| Tie rule: leader then lowest number | domain service, release note | application display status | T10 | Application status | rules |
| No units gives unknown | domain service | application display status | T10 | Application status | rules |
| Leader sets via `status-set --application`; displayed in place of derived | hook-tool definition, domain service | application status | T1 | Application status | rules |
| Non-leader error text | hook-tool definition | `status-set` call | T3 | Application status (sentence) | judged (Str: error nests under the call that raises it would put it in the hook-tool page; the hook-tool reference page already holds the text in docs/reference/hook-command/list-of-hook-commands/status-set.md; this page repeats one clause) |
| Which tables and columns show statuses | client output | `juju status` | T6 | `juju status` section | rules (Text: client-agnostic, client as example) |
| Leader asterisk | client output, unit doc | `juju status` | T6 | `juju status` section | judged (the leader page unit.md:33 owns it; one clause repeated) |
| Sample output | client output | `juju status` | T6 | `juju status` section | rules (R24 as quoted in the contract's T6 row) |
| Machine, model, relation, storage statuses | status constants | other entities | T1 | none | open(Q1) |
| Old transition figure facts | none enforced | | T2 | dropped | rules (Fig: only enforced arrows) |
