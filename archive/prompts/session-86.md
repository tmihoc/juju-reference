# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 85, 2026-10-20. The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

---

You are continuing two linked jobs: (1) a research project on the structure of Juju reference documentation (`~/git/misc/juju-reference`), and (2) **epic JUJU-9635, illustrate the docs, due 2026-10-21, delivered as ONE PR**. Code under study: `~/git/misc/juju-v2-preview` (4.1; branch `wip-entity-reference-pilots` must never be pushed). Never touch the main checkout `~/git/juju`.

## Read first, in this order
1. `HANDOFF.md`, the block "State at the end of session 85 (final)".
2. `page-recipe.md` and the end of `skeleton-v6.md`.
3. `TODOS.md`, `pr-epic-notes.md`, `WORKING-RULES.md`, `memory-export/MEMORY.md`.

## State of the epic PR
- Branch `4.1-docs-illustrate-docs-juju-9635`, worktree `~/git/misc/juju-tutorial-diagrams`, off `upstream/4.1` at `e5db99d585`. **Pushed to origin: tip `86f6de80c2`** (twelve commits). **Local only, not pushed, three signed commits on top** (ask the user before the push; plain push, no force): `4eb6086a56` subnet and zone back on their own pages, `529c7448af` credential page, `72f9a4f8d8` serial commas on the cloud and SSH key pages.
- The PR is still a draft, with no comments or reviews as of the last `curl` check. The PR text was updated in this session (the user has it); it must be updated again for any page added after the push.
- Pages done (reference): ssh-key, cloud, model, ssh-server, controller, secret-backend, machine, space, subnet, zone, credential, plus the tutorial and the high availability figure. Counted by script: **18 figures (24 views) outside the tutorial, on 12 pages**. The epic's 10 new diagrams are met.
- **Level decision (user, session 85):** `subnet` and `zone` are separate pages, not parts of `space`. I had folded them without a derivation; the code says a subnet has its own typed ID, listing and how-to, and a zone is named by constraints and placement directives and is listed live from the cloud. Zones are also in `placement-directive` and `constraint`: those pages now link to `zone-requesting`.
- Both builders (`dirhtml`, `latex`) were clean after the last commit (baseline `unknown node type <meta>` and two duplicate-target warnings aside). Build into a fresh `/tmp/<x>-*` directory each time and never run two builds on the same directories at once.
- ggarch pin unchanged (`000384e250377b3f57d7b4f75bb8ec14c66ec31e`, `hide-fields`).

## The Grice check (asked for by the user at the end of session 85)
- The nine subagent reviews (one per page, prompt in `local://` is gone: see the SESSIONS entry) **all failed with a 402 credit-limit error before producing a finding**. That is not a clean result. What was done by hand: label resolution on all eleven reference pages (every `{ref}` resolves, `kubernetes-cloud` is defined inside a list item), American spelling, serial commas in three-item lists, lists introduced by a colon, the primary-only worker list, the 24-hour intervals, the retry numbers, the cloud compatibility table against `cloud/whitelist.go`, and the credential tag format by running the names library. **Not done:** a per-claim trace of every error message and access level on the model, SSH server, SSH key, cloud, controller, machine, secret-backend and space pages by an independent reader. Redo it when credits allow, one page per agent (`agent: task`, read-only), with the prompt in `HANDOFF.md`.

## Your task, in order
1. **Ask the user to push** the three local commits and to confirm the PR text.
2. **Rerun the Grice reviews** (above), fix what they find in separate commits.
3. **Next page candidates, by inbound links and missing structure** (counted from `docs/`): `user` (30 inbound, 4 operations, 5 tables, the most likely next), `storage` (29 inbound, 20 tables: needs a section split first), `application` (65 inbound, 21 tables, 36 lines: needs the Agent question answered for its provisioner), `unit` (43 inbound, process-centric), `offer` (7 tables, 2 inbound), `relation` (133 lines, 12-table ERD already drawn on the held-back branch).
4. **Verify the unverified claims** listed under weak spots, by running the code where a unit test or a call can settle them.
5. If the user asks: a contributor page for the form under `docs/agents/`.

## What the skeleton does not cover yet (for the PR text)
- Process-centric entities. The controller page's workers section is plain prose tied to `juju_engine_report` and `/depengine` because E47 found no rule that assigns a worker to an entity; the form held on the controller, machine and secret backend pages only because their data models and operations are record-centric.
- A failure part for operators: the pages list errors per operation, but not what to check when a phase stalls or how to recover (migration phases, a machine stuck in provisioning, a controller node that does not rejoin).
- Entities without pages: block commands (the `change`, `remove` and `destroy` blocks are described in every operation that checks one), model defaults, the object store, leases, the controller charm.
- Storage, backup and restore, relation databag flow, and cross-model relations have no new figures.

## Known weak spots, do not hide them
- **Read from the code, not run** (session 85, additions): updating a credential checks each model that uses it but `validateModelCredential` returns no errors (`domain/credential/service/service.go:370-373`, a `TODO - implement`), so a forced and an unforced update behave alike for models; a placement directive `zone=` beating the `zones` constraint was read for EC2, GCE, OpenStack and MAAS only (`DeriveAvailabilityZones`), not for LXD, OCI or vSphere; credentials are removed from models by setting their key to null (`RemoveCloudCredential`); the secret-backend, machine, space and controller claims already listed.
- E44: the pattern is not shown to help AI readers; E47: no Agent rule.
- **Claims from reading the code that nobody ran** (session 85): the second `reload-spaces` does not store new subnets for known cloud IDs (the space page says so; read from `domain/network/service/space.go:197-208` and `state/subnet.go:47-79`, mock-tested only); `RemoveSpace` forced with an application exposed to both the space and `alpha` fails on a key collision; renaming a space that a constraint names fails on the foreign key; the HA page's statement that a new controller node joins the database cluster after the controller charm writes the node's database address (the charm source is not in the tree, and no Dqlite member removal call was found); `add-unit` on the controller creating a controller node on machine clouds; the machine page's provisioning order (ten attempts, ten seconds apart); the `reprovision-machine` refusals; the vault and kubernetes provider key lists; the secret backend rotation timing (0.75 of the interval, at most 24 hours); `ListSecretBackends` status for `vault` only; error texts that reach the client with an empty code (read from `apiserver/errors/errors.go`, not run).
- Unverified from earlier sessions: block definitions, import for another user, Kubernetes session identity, cloud spec contents, removal rule, the model page's remediation advice, migration status strings as a client sees them, the upgrade dry run, machine host keys after a migration, the SSH server page's relay endpoint and error statuses, the port set over the control socket by the controller charm.
- The controller page's configuration key list was resolved by script from `controller/config.go`; the controller page says `HighAvailability.EnableHA` is refused, from `highavailability.go:44-48`.
- A question for the Juju developers about key import is in `TODOS.md` and in the PR text.

## Rules the user gave in sessions 83 to 85 (all in `page-recipe.md`)
Per operation `Required access:`, `Rules:` (one bullet), `Errors:`; gerund plus entity titles (the entity stays in the title: "Connecting to machines through the SSH server"); openers say what the operation does; the data model keeps only DDL-enforced invariants; remediations say what to do, never a consequence ("Remove the models first"); Oxford comma; link or define jargon at first mention in each section; no metalanguage in captions; no sentence that anticipates the next block; no repeated fact; slideshows tell a narrative (a coarser copy of a later slide is dropped); name every participant the same way across a slideshow (SSH tunnel server, target SSH server, machine SSH server) and keep orientation left to right; grey nodes are software outside Juju; a figure is the first thing in its section and a lede has none; a "See also" link to the how-to goes directly under the operation heading (clear scope), only where a how-to section exists; the old page's purpose and benefits must survive a rewrite (audit the old text); do not state a claim that no code shows (the "inspect" claim was dropped).

- Added in session 85: **diagrams belong on the reference pages only; how-tos get text and "See also" links, never figures** (the user, twice). A lede is a definition plus at most two sentences (where it lives, how it comes and goes); the user shortened the space lede, so check every lede against the model, SSH key and SSH server pages before showing a page. Every list is introduced by a paragraph that ends in a colon and says what the list holds (the user's rule; the checker flags the rest). Do not claim a render looked right without opening the PNG under a new file name (the viewer cached an old image once).

## Standing directives (binding)
- First principles; nothing random; pre-register before running an experiment; report fails as fails; compute numbers by script; the code is the source of truth (comments are not evidence: the SSH port's "controller charm owns it" rests on a comment). Readers are human and AI. Reference pages are client agnostic.
- Never ask for verdicts or option menus when the code can decide. Ask before any push to juju (origin only, never upstream). Run git network, Go, Sphinx and shell commands with the sandbox disabled. Use `python3`. Check both docs builders. Every PR targets 4.1; branch starts `4.1-`. `gh` is not installed: use `curl` against the GitHub API for read-only checks. PR text in fenced blocks, never hard-wrapped, Jira JUJU-9635 line kept.

## Mistakes to avoid
- Pushing before checking CONTRIBUTING.md (two commit bodies failed the rules and needed a force-push): read the commit rules first.
- Scripted string edits of shared files: check `git diff` after each. `pkill -f` kills your own shell. A `latex` build into the worktree's `_build` wipes the live preview: build into `$TMPDIR`.
- Participant names that mean two things in one slideshow; unverified inherited claims; rules in data models that only a service enforces.
- Session 85: two `bash` builds into the same `/tmp` directories at once corrupt each other; a `git add -u` on a path that `git rm` already staged aborts the commit (check `git log` after every commit); a render that looks unchanged may be a cached image (copy the PNG to a new name before viewing); a diagram with an unconnected node fails `ggarch check` (leave key-only records out of the figure and describe them in the text); a scaffold keeps foreign keys to trimmed lookups, which `ggarch check` rejects (drop the `fk` flag on the trimmed record).

## End of session
1. Write the next launch prompt to `NEXT-PROMPT.md` (overwrite) and copy it unchanged to `prompts/session-<N>.md` (N is 87 for this file's successor). Never edit an archived prompt.
2. Append the outcome to `SESSIONS.md` with a one-line pointer to the prompt that launched the session.
3. Tell the user the one-line start.
