# Red team: the five-kind reference theory

Scope read: `~/git/misc/juju-entity-ref/docs/reference/` (status, removing-things,
scaling, watcher, log, telemetry, subnet, hook-command, machine, access,
relation, juju-cli, constraint, secret, hook, high-availability, unit, model,
agent, database, user, space; headings of all 51), Go doc comments in
`~/git/misc/juju-v2-preview` (`internal/worker/{deployer,unitless,charmrevisioner,
operationpruner,lease}`, `domain/{removal,blockcommand}`), and the scratchpad
evidence (`e8_*`, `e9_*`, `rater2.txt`, `rater9_*.txt`).

## 0. Problems with the evidence before any counter-example

1. **The e8 sample pre-sorts the content it tests.** All 126 corpus-A
   statements come from 18 entity pages already written in the
   declaration/persistence/execution layout (7 each from relation, action,
   access, storage, offer, model, space, charm, application, ssh-key, user,
   subnet, cloud, unit, secret, machine, credential, zone). Those pages were
   authored by the same people, to a closely related skeleton. Agreement on
   them measures how faithfully the pages follow the skeleton, not whether
   Juju knowledge has five kinds. None of status, log, telemetry, juju-cli,
   hook, hook-command, removing-things, high-availability, juju-dashboard,
   metadata or juju-db-repl was sampled in e8.
2. **The layer predicts the label.** Cross-tab of corpus A, rater A:
   persistence -> state 36/48; execution -> agent 8/8 of all agent labels,
   observation 9/10 of all observation labels. Agent and observation are
   identified by the section they came from (formulaic "Every watcher fires
   once..." paragraphs), not by a concept the raters discovered.
3. **The two contested kinds are tiny.** Agent: 8 both-agree / 10 either;
   observation: 10 / 12 (out of 206). Kappa 0.88 overall is carried by
   state (67) and identity (46). The theory's novel claims (agent as its own
   kind, observation as its own kind, their position) rest on ~10 items each.
4. **Identity absorbs package-purpose sentences.** Much of corpus B's
   "identity" is "The package provides ..." (ids 3, 4, 87): that is the
   identity of a Go package, not of a user-facing entity. It inflates identity
   and agreement.
5. **The rule about errors was given to the raters.** `rater2.txt` and
   *both* `rater9_rule.txt` and `rater9_norule.txt` contain "Rules and error
   conditions take the class of what they constrain". (The "norule" variant
   only drops the state/dynamics boundary paragraph.) So no experiment has yet
   tested the claim that errors need no dimension; it was an instruction.
6. **Units are line fragments.** Items such as "completed), and its
   completion time is stamped only when the last" (id 7) or "levels and the
   abilities they confer are defined in the user" (id 8) are rated. Fragments
   inflate agreement on vocabulary and deflate none.
7. **Agreement drops off the entity pages.** e9 (status, hook, constraint,
   bundle, high-availability, removing-things, controller, placement-directive,
   configuration, scaling) without the boundary paragraph: 74/90 = 82% primary
   agreement, versus 91% on e8. Disagreements cluster on removing-things, HA
   and bundle, and the "none" reasons there are **user-facing**: "rationale
   for force option", "command option support", "version-specific command
   option survey" (e9 ids 21, 54, 58, 65).

## 1. The ten hardest counter-examples

1. **Read-time derived values.** unit.md: "At read time, an agent with no
   presence record displays as `lost`, and a lost agent's workload displays as
   `unknown` unless the workload itself is in `error` or `terminated`." machine.md:
   "`down` is never written, only read when the agent has not been seen
   recently." The value is in the allowed-values list (state), exists only
   in a read (observation), and appears without any write (so no dynamics,
   but it changes over time). Filing it under state tells the reader it is
   stored; filing it under observation hides it from the status vocabulary
   where users look up `lost`.

2. **Visibility semantics of a step.** hook.md, "Writes are all-or-nothing":
   "Relation data, secrets, charm state and opened or closed ports are
   buffered and sent to the controller in a single commit when the hook exits
   with code 0 ... `status-set` is the exception: It takes effect
   immediately." It is about the agent (who buffers), dynamics (the commit
   step) and observation (when others see the change), and the accompanying
   table spans configuration, relation data, secrets, charm state, ports,
   action results, status and leadership. No single entity owns it. The
   theory wants one kind and one entity; the content needs a transactional
   consistency model, which is neither.

3. **State that decays with time.** hook.md: "A successful leadership check
   holds for about 30 seconds, so the answer can change during a longer
   hook." unit.md: leadership "is a lease in the controller database ... held
   by a unit until it expires". `internal/worker/lease/doc.go`: the manager
   "pin[s]" the lease during an application upgrade "so the application unit
   does not lose leadership". The truth value of "unit/0 is leader" is a
   state fact, its staleness is an observation fact, its expiry is a
   time-triggered dynamics fact, and pinning couples it to another entity's
   dynamics (refresh). Any one label is arbitrary, and readers who split it
   across three sections lose the 30-second warning, which is the point.

4. **Cross-entity verb semantics.** removing-things.md: "`unregister`,
   `detach`, `remove`, `destroy`, and `kill`. These commands are ordered such
   that their effect increases in severity". It is a comparative claim
   across operations on every entity. It is dynamics with no entity, so the
   theory's page model has nowhere to put it except by repeating it on
   every entity page. The `--force`/`--no-wait` matrix in the same file is
   the same problem in table form.

5. **A rule reified as an entity.** `domain/blockcommand/doc.go`: "Command
   blocks are model-scoped guard rails that temporarily prevent classes of
   user operations and API calls from proceeding." A block has identity and
   state (type, message), and users add, list and remove it, but its whole
   meaning is a precondition on *other* entities' dynamics. "Rules are not a
   dimension" fails because here the rule is the entity. Its error
   (`operation blocked`) nests with the block (state) or with every gated
   operation on every page (dynamics); both answers are bad.

6. **Allowed values whose meaning is delegated.** status.md: "Except for
   `error`, `terminated` and `unknown`, which are set by Juju, the workload
   status is generally speaking set by the charm. As such, its semantics is
   ultimately up to the charm author. The meanings listed below represent
   just the ideal case". The state kind assumes allowed values have fixed
   meanings. Here the value list is state, who sets it is agent, and the
   meaning is a convention aimed at a third party (the charm author). That
   last part is guidance, which the theory has no kind for (see section 2).

7. **Obligations with a consequence of not acting.** secret.md: "Charms that
   create secrets should _always_ handle the `secret-remove` event ... if a
   charm does not remove them, they accumulate indefinitely." hook.md:
   "Handlers must not assume that the underlying applications or services
   have been started". These are norms addressed to a reader role, plus the
   dynamics of *inaction*. The raters can call them dynamics only by
   ignoring the "should".

8. **The request language.** machine.md target designations: "`lxd`: a new
   container on a new host; `lxd:25`: on machine 25 ... `3,0/lxd/2,lxd:5`".
   constraint.md: "integers with M/G/T/P suffixes"; secret.md:
   "`secret://<source-uuid>/<id>` ... a local secret's URI is just
   `secret:<id>`". A designation can name a machine that does not exist yet,
   so it is not state of a machine. It is not a step either: it is the
   grammar of the request that triggers the dynamics. e8 raters split such
   items between state (ids 9, 13: "Rule: The name is not reserved") and
   dynamics.

9. **Deferred, layered evaluation of a value.** constraint.md: "a minimum on
   machine clouds, a maximum on system and Kubernetes containers";
   "Precedence: ... the more specific level wins: an application's over the
   model's, a machine's over the application's"; "Whether the cloud can
   honour it is discovered later, at provisioning time". The meaning of a
   constraint depends on the substrate, on resolution across three owners,
   and on another entity's later dynamics (machine provisioning). It is state
   of no single owner and dynamics of a different entity.

10. **Agents that do not map 1:1.** agent.md: the model agent is "a
    `jujuagentd` process running workers responsible for all the models
    associated with a given controller". `internal/worker/deployer/doc.go`:
    "the deployer worker, which deploys and recalls unit agents on a
    machine". high-availability.md: single-instance workers run where the
    `singular` worker holds the `singular-controller` lease. Each model's
    agent is one process shared across all models, hosted on the controller. The unit agent's
    "what makes it run or stop" is another entity's agent. Where a worker
    runs is decided by a lease (state of a third subsystem). The agent kind
    and the "1:1 lifecycle shares the page" rule both need the coupling to
    be simple, and it is not.

Honourable mentions: `subnet.md` "The unused surfaces: ... neither has a
non-test caller ... The surfaces are stated, not narrated" (a statement
about code reachability, which is developer-facing but now on a user page);
`telemetry.md` "No user information is gathered" (a privacy guarantee:
negative state about data leaving the system); agent.md says the unit agent
learns of changes "by always polling the controller agent" while watcher.md
says "nothing polls". The observation kind assumes a single push/pull
story. The docs contradict each other on it, and the skeleton gives no slot
to reconcile them.

## 2. Content that needs a sixth kind

The strongest candidate is **Interface (addressing and syntax)**: the
names, handles, grammars, locations and invocation surfaces a reader uses to
refer to and reach the entity. It is not a fact about the entity at an
instant, and it is not a change.

- machine.md target designation grammar (`0/lxd/4`, `lxd:25`, empty = new
  machine) and naming rules (no leading zeros, one container level).
- secret.md identifiers: URI vs name vs label, `secret://<uuid>/<id>` vs
  `secret:<id>`, and the example triple; log.md file locations
  (`/var/log/juju/...`, `logsink.log`, `kubectl logs -c ...`); juju-cli.md
  directory (`~/.local/share/juju`, Windows `AppData\Roaming\Juju`).
- telemetry.md `JUJU_CHARM_TRACE_CONFIG_*` env vars and the
  `control.socket` `POST /workload-tracing-config` endpoint; hook.md
  environment variables; constraint value syntax (`^` negation, M/G/T/P).

Today these land in state by default ("the name is ..."), which mixes them
with stored attributes. The e8 rater A's none reasons "terraform resource
reference" (id 89) and "hook environment variables" (id 101) are this kind.

Two more recurring kinds, either of which may need a slot:

- **Guidance (obligations and advice for a role).** secret.md "should
  _always_ handle `secret-remove`"; removing-things.md "`--force` and
  `--no-wait` ... should be regarded as tools to wield as a last resort";
  hook.md "Hooks should ideally be idempotent"; juju-cli.md "it is always
  recommended to be up-to-date"; the whole of juju-dashboard.md "Common
  questions and problems". 36 lines across the reference contain
  should/recommended/last resort/best practice.
- **Applicability (support and version scope).** constraint.md "Not
  supported by all providers", "EC2 and MAAS are the only providers that
  currently support the spaces constraint", `versionadded 4.1.0`; space.md
  "Support for spaces in Juju providers"; high-availability.md "supported for
  controllers on machine clouds"; telemetry.md "Relationship to previous
  releases"; removing-things.md "As of `v.2.6.1`". The theory calls history
  out of scope as developer content, but version and provider applicability
  are user-facing, and e9 raters marked them none (ids 21, 58).

## 3. Pages the skeleton empties, bloats or misleads

1. **Value and vocabulary pages: constraint, placement-directive,
   configuration, status.** constraint.md already says "A constraint is a
   value, not an entity: it has no life, no status, and no watchers of its
   own" and "has no machinery of its own". Agent and observation are
   empty, and dynamics belongs to the owner. The useful part, "List of
   constraints" (80 of 132 lines), is a key catalogue with per-provider
   notes that fits under none of the five headings. status.md is a
   vocabulary shared by five entities. Splitting it into the state sections
   of application, unit and machine pages would destroy the one place a user
   looks up `blocked` or `lost`.
2. **Cross-cutting mechanism pages: watcher, removing-things, hook (execution
   guarantees), high-availability, scaling, telemetry.** watcher.md is
   observation-only by nature. Identity is "a controller API object",
   with no state a user reads and no dynamics a user triggers. Under the
   skeleton it is four empty sections around one full one. scaling.md (19
   lines) is a definition that routes to constraint, unit and HA. Forced
   into the skeleton it becomes either empty or a duplicate of three pages.
   telemetry.md is two unrelated mechanisms (business metrics, OTel), joined
   by a common purpose rather than an entity.
3. **Program pages: juju-cli, juju-db-repl, juju-dashboard, hook-command,
   jujuc, jujuagentd.** The "entity" is itself an agent. Identity and agent
   collapse, state is "a directory" (juju-cli.md), and the real content is
   compatibility, environment, command lists and an FAQ. The skeleton would
   mislead by presenting `~/.local/share/juju` as the CLI's "state".
4. **Measured filler on entity pages.** Of the entity pages, 17 contain
   explicit negations that exist only to fill a skeleton slot ("no machinery
   of its own", "exposes no watch surfaces", "has no state machine",
   "nothing transitions"), 29 sentences in all. Examples: access.md (3),
   subnet.md, space.md, zone.md, offer.md, cloud.md, ssh-key.md,
   resource-charm.md (2 each). A reader learns nothing from "the access
   domain exposes no watch surfaces" that the missing section would not tell
   them.
5. **Entities whose kind is derived: relation, unit, machine.** relation.md:
   "The kind is not a stored discriminator: it follows from the relation's
   own records". The four-kind taxonomy (peer, subordinate, cross-model,
   regular) carries most of the page's user value, including the
   `juju-info` endpoint. It is identity (what kinds exist), state (derived
   attribute) and dynamics (peer relations "created automatically at
   deployment time") at once. Today it sits under persistence, where readers
   do not look for it.

## 4. Attack on the order identity, agent, state, observation, dynamics

- **It serves a question few readers ask first.** Reference readers arrive
  with an error string, a command, a status value or a "what happens if I
  ..." question. Those answers are in dynamics (operations, removal,
  preconditions, errors) and in the state vocabulary. The order puts
  dynamics last, after the database record and the watcher list. On
  machine.md under the old skeleton, reprovisioning and removal start at
  line 86 of 127. Under the new one they would come after agent and
  observation too.
- **Agent before state has no support in the data.** In e8 presupposition
  data, agent statements presuppose state (A: 3, B: 2) about as often as
  state statements presuppose agent (A: 3, B: 3). Agent statements also
  presuppose dynamics and observation. "What events it reacts to" is
  dynamics vocabulary, and agent statuses (`idle`, `executing`, `lost`) are
  state vocabulary. The only ordering the data supports is identity < state
  < dynamics (B: state->identity 57, dynamics->state 20). Rater B has 16 of
  138 presuppositions pointing to a later kind.
- **Observation before dynamics inverts cause and report.** A watcher
  reports a change, and the reader needs the change first. relation.md's
  "A unit's counterparts in one relation ... which is what turns a settings
  write on one side into a `relation-changed` on the other" is unreadable
  before the reader has seen the settings write (dynamics) and the hook
  (agent).
- **Agent as a general second section misleads for most entities.** Of
  the pages read, only unit, machine, controller (and arguably secret and
  model) have an agent. For the rest, the second section is either empty
  or "has no machinery of its own", which puts the weakest content in the
  second most prominent position.

## 5. Attack on "errors need no dimension"

1. **Many errors violate no rule.** Lookups that miss (`machine not
   found`, `secret not found`, `relation not found`, `permission not found`,
   `subnet not found` with three distinct triggers in subnet.md) fail an
   existence presupposition of a request, not an invariant or a stated
   precondition. Race errors (`machine cloud instance changed`: "a
   replacement appeared in between", machine.md) report a conflict. Transient
   errors (`leadership claim denied`, `unit life predicate failed`:
   "Remediation: None; the agent re-runs") are normal control flow, not
   violations. `grandparent machine are not supported currently` guards a
   layout that name validation already makes impossible (machine.md).
2. **One string, many rules.** `force required for removal job` covers both
   the controller model and an offer with connections (model.md).
   `permission denied` belongs to every gated operation on every page.
   `subnet not found` comes from three different lookups. Nesting by rule
   either duplicates the error or picks an arbitrary home. The reader's key
   is the string, and the theory has no index by string.
3. **Errors become state, with their own dynamics.** A hook error puts the
   unit's agent status in `error`. Resolving it (`retry-hooks`/`no-hooks`) has its
   own preconditions and errors (`unit is not in error state`, unit.md), and
   `--force` exists to bypass error-blocked teardown (removing-things.md).
   Error recovery is a lifecycle, not a footnote to a rule.
4. **The evidence never tested it.** Every rater prompt, including the
   "norule" one, told raters to file errors with what they constrain (see
   0.5).
5. **The error is the reader's entry point.** Users search the docs with an
   error message. Nesting under rules is a sound way to author errors, but
   the reader needs a way to look them up. The repair is an index, not a
   sixth kind (see section 6).

## 6. Verdict and ranked repairs

**Likely to survive:**
- identity < state < dynamics as a definitional backbone. It is supported
  by both raters' presupposition data and by 91% agreement on entity pages.
- The state/dynamics boundary as a writing rule (values and invariants vs.
  triggers, guards and steps). The 35% secondary rate is mostly this pair,
  and the e9 boundary paragraph is a reasonable fix.
- "An invariant is state, a precondition is dynamics" as an authoring rule
  for **rule-bearing** errors.
- Moving developer structure, code layout and rationale out of user pages.
  The corpus-B none rate (26-28%) is real.

**Unlikely to survive:**
- Exhaustiveness. Interface, guidance and applicability recur on user pages.
  e9 none reasons include user-facing rationale and version scope.
- Agent and observation as general top-level kinds of every entity page.
  The evidence for them is about 10 items each, it is predicted by source
  section, and most entities fill them with negations.
- The 1:1 lifecycle rule as stated: the model, unit-on-machine and
  singular-worker agents break it.
- The claim that errors need no dimension, as a reader claim.
- The fixed order as a reader order.
- One skeleton for every reference page.

**Ranked repairs:**
1. **Restrict the theory to entity pages and name the other page types.**
   Vocabulary/catalogue pages (constraint, placement-directive,
   configuration, status, list of hooks), mechanism pages (watcher, hook
   execution, removal semantics, HA, telemetry) and program pages
   (juju-cli, juju-db-repl, dashboard). Give each its own short template.
2. **Make agent and observation conditional subsections, not kinds every
   page must carry.** Include them only when non-empty, and drop the
   "has no machinery of its own" filler (29 sentences).
3. **Add an Interface slot** (names, identifiers, syntax, locations, env
   vars) next to identity. Treat **applicability** (provider support,
   `versionadded`) as an annotation on any statement, not a section.
4. **Add an error index by string** that links to the rule each error nests
   under. Add a separate class for errors with no rule (lookup miss,
   conflict, transient), filed under the operation that raises them.
5. **Reorder for readers:** identity, interface, state (vocabulary first),
   dynamics (operations, preconditions, errors), then agent and observation
   as "how it runs". Keep definitional order *within* sections, not across
   them.
6. **Allow guidance as marked admonitions** (`should`, last resort,
   best practice) attached to the statement it qualifies.
7. **Write a cross-entity home for shared semantics:** the hook commit and
   visibility table, leadership-as-lease, the removal verb ladder, and
   read-time derived status. Entity pages link to it and do not copy it.
8. **Re-run the experiment fairly:** sample whole sentences from all 51
   pages and the how-to/explanation corpus. Remove the error rule from the
   prompt. Report kappa per class and a layer-blind control (strip the
   section context), and test the claimed order with a reader task (time to
   answer an error-string or "what happens if" question), not only with
   presupposition labels.
