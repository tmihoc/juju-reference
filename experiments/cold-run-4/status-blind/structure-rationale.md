# Structure rationale

Inputs gave no section template. I looked for one in the contract and the ledger: the contract says "The contract fixes no section structure for a page" (Page form). No template found, none followed. The list of source artifact kinds used below: SK1 domain/application status constants and docstrings (core/status); SK2 domain service code (derivation, severity, decode); SK3 uniter worker code (hook-time statuses); SK4 hook-tool definition (jujuc status-set doc and validation); SK5 client output code (cmd/juju/status); SK6 initial-state code (domain/application unit creation); SK7 upstream docs and release notes.

Resulting structure (unusual points marked):

```
# Application and unit status          (lede, no subheading)
## Unit status                         (anchor kept)
### Workload status                    (anchor kept)
### Agent status
### Status of a unit from deployment to removal
## Application status                  (anchor kept)
## Status in `juju status`
```

| Section | Questions | Facts held | Source kinds | Why not merged or split |
|---|---|---|---|---|
| Lede | T1 (what is it) | A unit has two statuses, an application one; a status is value, message, time | SK1, SK2 | A lede states the whole answer to T1; merging into "Unit status" would hide the application status from the first sentence |
| Unit status (parent) | T1 | Workload reports on software, agent reports on the unit agent | SK3, SK4 | Exists because the anchor `unit-status` is linked from the how-to on units (docs/howto/manage-units.md:111) and the link reads as "unit status values". Split from the lede because the two subsections need one parent. This section's existence is driven by an address (R15), not by a question; the questions alone would have left it out |
| Workload status | T1 (who may set, which values), T2 (which values), T3 (error, blocked: what to do), T6 (meaning; Kubernetes override) | Four accepted values; Juju sets the rest; 7-row meaning table; message; Kubernetes pod rule | SK1, SK3, SK4, SK2 | Different owner (charm via hook tool, plus Juju) and different reason to change than the agent table; split from Agent status. Kept in one section: values, setter, and override rule all change when workload status code changes (change coupling is not measurable here; judged by source owner: SK2 decode and SK4) |
| Agent status | T2, T3 (lost, failed), T6 | Six values; who sets; effect of `lost` on workload display; display of agent `error` | SK1, SK2, SK3 | Owner is the unit agent and controller; different from workload. Not merged into Workload status because a reader looking up `idle` or `lost` asks a different question than one looking up `blocked`. Not split into one section per value (Over-fine split) |
| Status of a unit from deployment to removal | T2 (which follow which), T5 (removal) | Ordered list of statuses Juju sets from creation to terminated | SK3, SK6 | The facts come from several artifacts (creation code, uniter init, hook runs) and one question ("which follow which"). They are not merged into the two value tables because a value table is indexed by value and this list is indexed by time; each answers a different lookup. A figure was considered and dropped: the list states every fact and a figure would be redundant (contract: figure earns its place only by clarity; no relation here beyond order) |
| Application status | T1 (who sets), T10 (order when several compete), T2 | Derived default; severity list; tie rule; no-unit case; leader-set override; non-leader error | SK2, SK4, SK7 (release note) | Owner is the application display status (DSV 353-396), different from the unit values. Placed after the unit sections because it uses their values (Crossed-wire test). Not split into "derived" and "set" subsections: 5 sentences, a Fragment otherwise |
| Status in `juju status` | T6 (where do I see it) | Which table and columns show each status; leader mark; a sample | SK5, SK7 | Owner is the client output code, not the platform status; separate so that the platform statements above stay client-agnostic (Text: client-agnostic) and the client section is the example the contract asks for (T6 note). Not merged into the lede: the lede answers T1 |

## Where the question list and the maxims did not decide

1. The unit-status parent heading is forced by an anchor (R15), not by T1 to T10. Without the anchor I would have used two top-level sections for workload and agent. The method does not say whether an inbound anchor may shape structure; I let it.
2. Order of the two top-level sections. Maxims (Manner: orderly; Relation: depends on neighbor facts) say unit before application because the application derives from unit values. T10 and T1 would equally support application first (it is the simpler concept, and upstream has it first). I chose by dependency; judged.
3. Lifecycle list as its own section versus rows inside the two tables. The question T2 ("which follow which") favors a time-ordered list; T6 ("what does it mean") favors per-value rows. Both are real. I kept both and accepted that the lifecycle list repeats five messages already named in tables (Duplicate risk). Judged.
4. Kubernetes pod rule: Workload status section or `juju status` section. It changes the displayed workload status (platform fact, SK2), so Workload status; the question list does not say whether a model-type specific rule gets its own section. Judged.
5. T3 ("what can fail and what do I do?") has partial answers only: for `error` the remedy is a person acting; the only source-verified remedy text is the hook-tool doc for `blocked` messages. I could not add "run `juju resolved`" from my allowed sources without a traced statement of its effect (the command page exists at docs/reference/juju-cli/list-of-juju-cli-commands/resolved.md but I did not read its details). Open: link from the `error` row to the resolved command page.
6. Machine, model, relation, storage statuses: the question list has no entity-scope question, so nothing decides whether this page owns them. Open(Q1).
