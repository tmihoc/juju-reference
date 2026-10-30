# The Juju documentation paradigm (consolidated draft, session 104)

Status: applied to the PR branch in `19f114a545` (`AGENTS.documentation.rules.md` and the cloud conventions); this file keeps the working draft, the bot's skill-set table (section 7), and the stale-claims table (section 8). Replaces the overlap and gaps across `docs/agents/AGENTS.documentation.rules.md`, `AGENTS.doc-dot-go-rules.md`, and `AGENTS.cloud-reference-documentation.md`, folding in the archive's working rules (`page-recipe.md`, `work/cq-rubric-103.md`). **Out of scope by the user's word (104): `AGENTS.documentation-landing-pages.md`** (set by a stakeholder, not by this work; it stays as it is).

Every claim below was checked against the 4.1 anchor (`/tmp/juju-41-tree`, `e5db99d585`) or the PR tree on 2026-10-30. Section 7 is the bot's skill set; section 8 lists what was found stale in the current files; section 9 lists conflicts that need the user's decision.

## 1. The charter

`docs/` is the top-most `doc.go`. It documents what the codebase exports, meaning everything projected onto a user interface (CLI, API wire, status, log lines, database tooling), and the cross-cutting mechanisms that no lower-level document can own, at mechanism level, in surfaced vocabulary. Everything else is implementation and lives in the code.

The `doc.go` Locality Principle (`AGENTS.doc-dot-go-rules.md`) is the parent rule: document everything at the smallest scope where it can be accurately documented; cross-package concerns go to the project-wide tier, which is `docs/`. The writing guidelines of that file therefore apply to `docs/` too: contracts, not implementation; verify every claim against the code and remove the unsupported; when in doubt, omit.

A package's `doc.go` gets two gates from the Go toolchain for free: godoc renders only exported identifiers (the visibility rule), and its readers are package users (the reader definition). Prose has no compiler, so `docs/` states both gates itself (section 2) and adds the one rule that locality implies and never says: one owning page for each fact.

## 2. What goes on a page: the inclusion test

A fact stays only if all three hold.

1. **It is true.** Traced to the code as it is now, and re-checked whenever the page is touched. Truth is a standing duty.
2. **A reader can meet it** on a supported surface: a command's output, an API call's reply, a status, an operator log line, or the database through `juju dump-db`, `juju-db-repl`, or backups.
3. **Someone is asking, and this page owns the answer.** The named audiences:

| Audience | Their questions |
|---|---|
| Operator (reads status and logs) | What is X? What can I do to X, and who may? Which states can X be in, and which follow which? Why did this fail, and what do I do? What happens to X during migrate, upgrade, destroy? Where do I see X, and what does its log line mean? |
| Client or tool developer (human or AI writing against the API) | Which calls read or change X, with what request, result, and errors? What access does a call need? What invariants must my tooling respect? Which watcher follows X, and what does each delivery carry? Which exact strings and codes can the wire return? |
| Charm developer (the client is the unit agent) | Which hooks fire for my charm and why? What may my charm read or change, with what rules and errors? Which statuses can it set or receive? Am I the leader? What happens to its world during maintenance? Bounded to Juju's behavior toward the charm, not the craft of writing one. |
| Storage or incident inspector (DB access) | Which records make up X's storage, in which database? What must always hold of them, so that a dump can be judged sane? What bookkeeping does the storage layer keep? |
| AI reader | The union of the above. It changes how pages are written (every term linked or defined, one home per fact), never what goes in. |

Juju developers are not an audience: the code is their documentation. The one exception is a how-to corner labeled "For Juju developers".

**When the tests disagree:**

- Meetable, but this page's reader is not asking: move the fact to the page whose reader is, or cut it.
- Someone asks, but cannot meet it: write only what they can meet, at the surfaced level ("the unit holding the lease", not how the leader is picked).
- Neither: it stays in the code.

**Ownership.** Every fact has one owning page and every other page links. The reader's question decides the owner, not the subject and not where the fact lives in the code. Mentioning is not restating: a page may name a fact with a link (context records ride as linked chips) and may not re-describe it. A mechanism with its own reference page (model migration, watchers, the database) keeps its machine there, and the call that starts it links it. A mechanism page is not exempt from the question test: it says what happens, who drives it, in what order, and where each step surfaces, in names a reader can trace to a command, an API, or a log line.

**Filter, never structure.** The test removes facts; it does not decide the form of a page (section 4).

## 3. The Diataxis sort

Content appears in one location only, and cross-references join the rest. Choose the single most useful location even when a fact could fit two types.

| Type | Holds | Does not hold |
|---|---|---|
| Reference (`docs/reference/`) | What things are: entities, tools, processes, mechanisms. The contract of each call: caller, rules, errors. | The procedure to follow. |
| How-to (`docs/howto/`) | The user's task flow through an entity's lifecycle, including automatic operations. | Attributes, field lists, error catalogs. |
| Explanation (`docs/explanation/`) | Why it works that way: design decisions and architecture. | Specifications. |
| Tutorial (`docs/tutorial/`) | End-to-end learning for beginners. | |

The old rule "reference is attribute-based, never operation-based" is refined here: an entity page documents each **call** as a contract (who may make it, what it checks, what it returns, what it refuses). The steps a person follows to reach a goal stay in the how-to, which the call links with `See also`.

Duplication is the failure this sort prevents. Link to upstream documentation (SQL, YAML, cloud APIs) and add only the Juju-specific guidance.

## 4. The entity reference page form

The form derived from the code and settled over the PR (`page-recipe.md`). The set of pages comes from the manifest, and a page's level (page or section) is derived from the code (own typed ID, own facade method, own lifecycle) and recorded in the commit.

**Section grammar.** Each section appears only when its facts exist, in this order:

| Section | Holds |
|---|---|
| Lede (no heading) | One definition sentence (the kind of thing, then what sets it apart), then at most two sentences on where it lives, who holds it, how it comes and goes. |
| `<Entity> database schema` | Figure first, then the records with their rules. Only what the database enforces or the schema fixes, and only what an interface shows. |
| `<Entity> change streams` | Only if a client, agent, or worker can follow the entity. "The changes that <holders> follow", delivered through a watcher. |
| `<Entity> calls` | An opener defining the set, then one `###` per call. |
| `<Entities> and model migration` | Only the exception to the generic export, in one paragraph. |

Never: an Identity section, an errors section, a section that announces itself. A mechanism page (model migration, watcher) leads with its machine (the phase or state diagram), then what happens in each state, then who drives it, then its records and streams.

**Top of page:** `See also:` an `ibnote` linking the Juju how-to and the Terraform Provider for Juju page.

**A call** is a `###` under a `## … calls` section and nowhere else. It is titled with a gerund and the entity (`Adding SSH keys`), opens with the gerund phrase as the subject saying what the call does, then gives, in order:

- `Caller:` who may make it. For a client, the user it acts for, with the linked access level ("A client, for a user with write access to the model") and the block that must not be on. For an agent, the identity ("A unit agent, for its own unit."). Levels attach to users, never clients.
- `Rules:` every rule of the call, nested under one bullet.
- `Errors:` the message the client sees, its code, a trigger, and a remediation. A remediation says what to do, never a consequence.

The count of calls and documented errors is checked mechanically (section 6).

**Database schema rules.**

- A rule stays only if the database enforces it (unique index, not-null or check constraint, trigger, foreign key) or the schema fixes the allowed values. Find the constraint in the **consolidated release DDL** (`domain/schema/*/4.0.15-*-release.ddl`), never in a per-table patch alone. A rule that a service, facade, or worker applies when a call runs goes in that call.
- A record, field, or sentence stays iff a reader meets it through a surface the page documents. Otherwise: **hide** it (internal bookkeeping), **contain** it (a record that explains a shown one rides as a linked context chip), or **relocate** it (prose for another page's reader moves there).
- No table names, column lists, or `.ddl` pointers in entity-page prose. The mapping lives with the database tooling and on the database page, whose subject is the storage layer.
- A status with allowed transitions has its values in the schema; its state diagram and transition table live in the call that changes it, or on the mechanism page when the mechanism has one.
- A kind that records decide (peer relation, cross-model relation) is described in the bullet of the record that decides it. The base case comes first.

**Text rules.**

- Every opening sentence is a definition. "X is how Y does Z" is not one.
- A bullet list is built up to: the paragraph before it ends in a colon and says what the list holds. A list of one item is prose. No counting intros.
- Say what is true, never what is absent. No unearned negations.
- One subject per sentence. Do not glue facts with ", and". Name the real relation (so, then, because, when). "And" stays for same-kind items and for two verbs of one subject.
- Oxford comma. American spelling.
- No version scoping of any kind: no "in 4.1", no `versionadded`, `versionchanged`, or `deprecated` directives, no "new in" or "since" notes. Version facts go stale and belong to the release notes and the per-version documentation, which carry them. The one exception is the how-to for the 3.6 to 4.1 upgrade, whose subject is the version transition.
- "Operation" is the domain word for one run of a script across units (`juju operations`). One documented API interaction is a "call".
- Hook commands, not "hook tools". Every specific hook or hook command links to its documenting section; a name with no page stays in plain code font.
- Never "databag": say settings.
- Link jargon at its first mention in each section, or define it in a parenthetical. Never link a CLI command page and never write "the CLI offers": reference pages are client agnostic.
- Define "unit agent" once, in the calls introduction: the process that runs the unit's charm, logged in as its unit, acting only for that unit.
- Sections named by what they hold: `X database schema`, never `X data model`. A file's name matches its title.

**Figures.** On reference pages only, never on how-tos. The first thing in its section. The caption carries the takeaway (what to read first, the rule the edges imply); the alt text carries the inventory, in plain English. A schema figure shows records only and a sequence figure shows software only; records that another page owns are context chips. A sequence figure appears only when a call crosses at least three actors, at least one outside the controller, and the order decides what the reader sees. Render figures from sources, never commit rendered SVGs.

## 5. Tool, concept, and cloud pages

**Tool references** (`juju-cli`, `juju-db-repl`, dashboard): the file is named after the tool a user invokes. Sections are by capability (Overview, Basic commands, Navigation, Query execution), never metalanguage ("Commands"). Command anchors are `<tool>-<command>`; commands that are alternatives share one heading.

**Cloud pages** follow `AGENTS.cloud-reference-documentation.md`: a machine-cloud and a Kubernetes template, organized by Juju entity (the cloud, Credentials, Controllers, Models, Machines, Storage) with `Limitations` and `Requirements` first when they exist. Constraint, placement, and storage-provider claims are verified against the provider code with the five-step audit in that file. Reuse snippets live in `docs/reference/cloud/list-of-supported-clouds/reuse/{machine,k8s}/`.

**Anchors:** lowercase, dashes, never underscores (the one exception is a tool's own name, `juju_db_repl`). A section anchor is the page anchor plus the section title.

## 6. How-to guides and mechanics shared by all types

**How-to guides.** The title names the entity and the verb ("How to manage <entity>"). Sections follow the entity's lifecycle: access or create, list, inspect, modify, use, remove. A section opens with "To <accomplish task>, <do action>". Each section is independently usable. No metalanguage sections ("Prerequisites", "Tips"): integrate, or use a labeled dropdown (`Tip:`, `Background:`, `Troubleshooting:`).

**Cross-references.** `See also` at the top of a page is lateral (entity or concept). `See more` after a command's output zooms in to the tool reference, once per tool. Concept, tool reference, and how-to link to each other, so that a reader can move between understanding, detail, and practice.

**Style.** Active voice. Consistent entity names. Em dash written ` -- ` (space, two hyphens, space), never the single em-dash character in prose. Quoted strings (error messages, CLI help) keep their own characters. Colon in a bullet term. `text` fences for commands, `sql` for SQL; a blank line before and after a fence. Realistic names in examples ("frontend", "backend"), not "default".

**Autogenerated pages** (CLI commands, hook commands, controller and model configuration keys) are never edited by hand: change the Go source and run `make regenerate-docs` from `docs/`. `make verify-docs` fails on any difference and is the merge-blocking CI job (`autogenerated-docs`); the full HTML build is informational.

**Diagrams.** One model for the whole doc set, `docs/juju.ggarch`, with one view for each figure. Everything that describes the system lives in the model; a view only selects, positions, and annotates. A node, record, or edge is declared once, so renaming it updates every figure, and model-driven authoring delivers the consistency and maintainability it promises only while there is one model. A page that needs a new entity extends the model; it never starts a model of its own, and it never re-declares another page's record. Embed a view with `{ggarch}`, validate with `ggarch check`, and render from sources (never commit rendered SVGs). Colour means ownership only. **The tree does not conform yet** (section 8, row 1; section 9, item 4).

## 7. The bot's skill set

Each skill names the test it runs and the tool that exists today.

| Skill | Question it answers | Tool today |
|---|---|---|
| Inclusion: truth and surface | Is every claim traced to the 4.1 tree, and can a reader meet it? | Manual against the tree; `tools/extract_facade.py` gives each call's access, block, and errors with file:line |
| Inclusion: audience | Which named audience asks this, and does this page own the answer? | Manual against the audience table (section 2) |
| Ownership | Is any fact restated rather than linked? | Manual; the duplicate-facts sweeps of sessions 99-102 |
| Schema enforcement | Is each schema rule enforced by the database? | Manual against the consolidated release DDL |
| Form | Section titles, forbidden phrases, spelling, list intros, Oxford comma, ", and" glue | `tools/check_page_rules.py` |
| Error contract | Is every documented error message raisable by the source? | `docs/scripts/check_error_contract.py` (in the PR); counts via `tools/count_errors.py` |
| Figures | Do the sources validate and render? | `ggarch check docs/juju.ggarch` |
| Builds | Do both builders pass without new warnings? | `sphinx-build -b dirhtml` and `-b latex` into fresh directories |

Gap: only `check_error_contract.py` ships in the repository. The other tools live in the archive (`~/git/misc/juju-reference/tools/`), so a bot running from the repository cannot yet run the form and facade skills.

## 8. Stale claims found in the current files (checked 2026-10-30)

| File and place | Claim | Tree says |
|---|---|---|
| Rules, Quick Reference "Diagrams" | "One model for the whole doc set: `docs/juju.ggarch`" | The rule is right and the tree is wrong: `docs/juju.ggarch` holds 14 models and 67 views (`ggarch check`: 14 models, 45 diagram views, 22 sequence views). Section 6 keeps the rule. Section 9, item 4 queues the merge. |
| Rules, Entity Reference Section Naming | `<Entity> architecture` and `Types of <entity>` as entity-page sections | No page under `docs/reference/` has an "architecture" section title. Entity pages use the section grammar in section 4. `status.md` keeps one `## Types of status`. |
| Rules, Quick Reference; Framework | "Reference is attribute-based, never operation-based" | Entity pages document calls as contracts. Refined in section 3. |
| Rules, example in Section Ordering | "Database implementation (Dqlite technical details)" | Applies only to the page that owns the mechanism. Bounded in section 2 (already done upstream by `7e73cace5a`). |
| Cloud file, lines 196 and 330 | Snippets under `docs/reference/cloud/list-of-supported-clouds/list-of-supported-clouds/reuse/k8s/` | That directory does not exist; the snippets are in `.../list-of-supported-clouds/reuse/{k8s,machine}/`. Fixed in section 5. |
| Rules, how-to pattern | Title "Manage \<entity\>" | The pages are titled "How to manage \<entity\>". Section 6 follows the pages. |
| Rules, Writing Style | Colon after the bold term: `**Term**: Definition.` | Entity pages write the colon inside the bold: `**Leader:** The unit …`. Left as the pages have it; not in section 4. |

## 9. Decisions and open items

1. **Em dashes: DECIDED (user, 104: "follow the rule").** The rule is ` -- `. Applied to the PR branch: 39 prose em dashes in 21 pages, all lines this PR added (no upstream line touched; quoted strings and code spans untouched). Committed as `2ca8b7e9e3`.
2. **Version scoping: DECIDED (user, 104: figure it out; the user's view is that such notes go stale and the release notes and per-version docs carry them).** The draft bans all version scoping (section 4, text rules). Applied to the PR branch: the four `versionadded` directives removed (`database.md` 4.0, `juju-db-repl.md` 4.0, `hook.md` 3.6 twice). The anchor already had the db-repl and hook ones; `database.md`'s was this PR's. Removing the two hook ones changes pages this PR did not author, so the commit says so. Committed as `2ca8b7e9e3`.
3. **File layout: DECIDED (user, 104: "ok with your assumption").** The paradigm becomes `AGENTS.documentation.rules.md`; the `doc.go` rules stay a separate file (the lower tier); the cloud conventions stay a page-type template; the landing-pages file is untouched. `CONTRIBUTING.md` needs no change.
4. **One ggarch model: OPEN, not started.** The user's rule is "one model" (draft, section 6). The tree has 14 (`Juju` 220 lines, `JujuSchema` 2,481, and 12 per-page models of 29 to 56 lines each: `SSHKeyImport`, `SSHConnect`, `MigrationPhases`, `MigrationSequence`, `ControllerBootstrap`, `MachineProvisioning`, `TaskStatusChanges`, `ActionRun`, `RelationStatuses`, `RelationSettingsSharing`, `UnitResourceFetch`, `UpgradeStateChanges`). What a regex scan of `docs/juju.ggarch` found, to be confirmed by the merge itself: all 67 view names are unique; of 293 node ids declared as `id [type: …]` only 6 collide, all between `Juju` and `JujuSchema` (`user`, `cloud`, `controller`, `model`, `application`, `charm`). So the 12 small models probably merge by concatenation, while the 6 collisions need a decision: one entity (the schema records extend the architecture node) or two (rename). The scan did not check edges or nested nodes written another way. The 49 `:file:` references in `docs/reference/` already point at the one file. The pin is `ggarch @ b9eb04d409`. This is the open TODOS item "ggarch: per-page models" (raised 2026-10-21), and the rule in section 6 is its decision. The merge is its own commit, with `ggarch check` and both builders before and after, and an identical render of every view as the acceptance test.
