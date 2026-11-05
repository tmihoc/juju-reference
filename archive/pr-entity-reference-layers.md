# PR: anchor entity rules and errors inside their layers

State as of 2026-09-30 (session 76). Read this first when resuming the entity
reference work.

## Where things are

- Branch: `4.1-docs-entity-reference-layers` on `origin` (tmihoc/juju), tip
  `2576a81b14`, 25 commits on upstream/4.1 (70591a13ec). Pushed to origin only;
  never push to upstream; ask before every push.
- Worktree: `~/git/misc/juju-entity-ref`. Baseline worktree for warning diffs:
  `~/git/misc/juju-base` (detached at upstream/4.1).
- Compare link (PR form against juju/juju 4.1):
  https://github.com/juju/juju/compare/4.1...tmihoc:4.1-docs-entity-reference-layers?expand=1
- The PR is not opened yet (the user creates it).
- Live preview: `~/git/misc/juju-reference/preview-entity-ref.sh` serves
  http://127.0.0.1:8001/ (port 8000 belongs to another preview). It runs with
  the sandbox off and dies on a machine restart.
- Build: `/tmp/claude-1000/build.sh`-style purged dirhtml build on the venv of
  `../juju-pr4/docs/.venv`, sandbox off. Result: same non-meta warnings as the
  baseline. The LaTeX builder was not run (no ggarch nodes on these pages).
- Related files in this directory: `reference-page-types.md` (types and
  treatment), `entity-page-form.md` (the form and checklist),
  `machine-rewrite-draft.md`, `fence-manifest.md` (41 removed diagram fences),
  `tools/` (`raise_sites.py`, `loss_check.py`). Decisions: ggarch ADR-016 (form
  and "Rollout" findings), ADR-013 amendment (page types).

## Open: 4.1 content the restructure drops

The description below is written against upstream 4.1. A fidelity check against
the 4.1 pages (not the prep branch) shows the PR drops 4.1 prose that has no
equivalent on the new pages. The description discloses it; the recommendation is
to restore the user-facing pieces:

- charm: track, risk and branch definitions, the `juju info` and `--channel`
  usage (the page now defers to Charmhub docs).
- secret: URI, name and label explanations, the name regex, the lifecycle
  narrative.
- machine: the definition of `base`, the `add-machine` and `deploy --to`
  walkthroughs.
- action: the CLI workflow (blocking, result format, the action commands).
- credential: the "credential means cloud authentication" notes.
- relation: the taxonomy and databag figures are replaced by text; the six image
  files `relation-taxonomy.{svg,dark.svg,excalidraw}` and
  `relation-databags.{svg,dark.svg,excalidraw}` are now unreferenced and can be
  deleted.
- Smaller: placement-directive developer note (an HTML comment), controller S3
  policy (commented out in 4.1), cloud and credential pointer sentences, the
  constraint intro sentences.

Pending the user's go: restore those pieces, delete the orphaned images, rebuild
and diff warnings, push the extra commits to origin (separate commits, no
amend).

## PR title

```
docs(reference): anchor entity rules and errors inside their layers
```

## PR description (relative to upstream/4.1)

```
## Problem

The 4.1 entity reference pages define each entity and list some of its attributes and commands. They say little about what Juju stores for an entity, what runs in the background when it is declared, which rules Juju enforces, or which errors a user meets and why. The 4.1 pages contain no error strings at all (for example, the unit page is 33 lines), so a reader who holds an error message has nowhere to land.

## Fix

The 24 entity pages now share one form. Each page has three layers that follow the order an intent travels: what you declare, what Juju stores, and what happens in the background. Every rule, error, trigger and remediation sits under the bullet it constrains, so an error string lands next to the thing that raises it:

- Declaration bullets are anchored by lifecycle action (create, designate, consume, remove).
- Persistence bullets are anchored by stored record component (primary entry, parent record, cloud instance record, status records, lookups).
- Execution bullets are anchored by operational loop (provisioning, leadership, removal, watchers).

Errors use the literal Go message and are filed in the layer whose code raises them. Each one was resolved to its Go constant and raise sites in the 4.1 source, and the other claims on the pages were checked against the source too.

Pages covered: access (new), action, application, bundle, charm, cloud, constraint, controller, credential, machine, model, offer, placement-directive, relation, resource-charm, script, secret, space, ssh-key, storage, subnet, unit, user and zone. A new `watcher.md` (label `watchers`) explains what a watcher is, because every entity page links it. The reference index lists it.

What changes for existing readers of these pages:

- The definitions and the reference lists stay: constraint keys, placement directive forms, secret backend options, charm types, user access levels, storage providers and pools, cloud types, hook and action environment variables.
- Prose that walked through CLI sessions and command output (for example the `add-machine` and `deploy --to` walkthroughs, the action run workflow, the secret lifecycle example) gives way to descriptions of the records and loops behind them. The how-to pages carry the command-level guidance.
- The charm page keeps the channel summary (track, risk levels, branch) and leaves the guardrail detail to the Charmhub documentation.
- The relation taxonomy and settings figures stay, each beside the text that explains it.
- The pre-3.6 version notes on the controller, constraint and secret pages are removed, in line with the 4.1 cleanup.

Behaviour that these pages now document for the first time:

- Which errors each entity raises, with trigger and remediation (for example `user unauthorized` is a wrong or missing password, `machine constraint violation` compares the architecture only, `action not defined for charm` is raised when the run is enqueued).
- `quota limit exceeded` covers two different errors: a relation endpoint at capacity, and application configuration over 16 MB.
- Storage detachment (`juju detach-storage`) removes one attachment or all of an instance's attachments, honours force and a maximum wait, and refuses to take a unit below the charm's minimum.
- The controller has no `juju enable-ha` command in 4.1, and the `EnableHA` call on the controller API adds and removes nodes.
- A migration target must be Juju 4.1 or later.
- Zones are cached in the model database and adopted together with subnets.
- The S3 object store is configured through the object-store backend records.

The entity diagrams follow in a separate change. The 4.1 `docs/juju.ggarch` holds only the architecture views, so each entity view has to be ported and verified against the 4.1 schema first. This PR carries the text only.

## Checklist

- [ ] ~Code style: imports ordered, good names, simple structure, etc~
- [ ] ~Comments saying why design decisions were made~
- [ ] ~Go unit tests, with comments saying what you're testing~
- [ ] ~[Integration tests](https://github.com/juju/juju/tree/main/tests), with comments saying what you're testing~
- [ ] ~[doc.go](https://discourse.charmhub.io/t/readme-in-packages/451) added or updated in changed packages~

## QA steps

Documentation only. From `docs/`, run a purged build and compare its warnings with a build of `4.1`:

    rm -rf _build .sphinx/.doctrees
    sphinx-build --keep-going -b dirhtml . _build -w warnings.txt -c . -d .sphinx/.doctrees -j auto

The warnings match the `4.1` baseline apart from "unknown node type" meta lines. Then open any page under Reference in the Read the Docs preview (for example Machine, Unit, Relation or Secret) and check that each layer lists its errors under the bullet that raises them, and that older links such as `#machine-execution-rules` still land on the layer heading.

## Documentation changes

The Reference pages for 24 entities change structure as described above, and two pages are new (access and watcher). There is no change to CLI or API behaviour.

## Links

~**Issue:**~

~**Jira card:**~
```

If the dropped content is restored, edit the "What changes for existing readers"
bullets (the CLI-walkthrough, charm and relation bullets) to match before the PR
is opened.

## Other open items

- Diagrams: port the 41 removed views into `docs/juju.ggarch` (verify against
  the 4.1 schema), one PR per group; the ggarch CI check is due with the first.
- Pages of types 3-11 (agent, pebble, jujuagentd, containeragent, database, log,
  status, telemetry, hook, configuration, metadata, HA, scaling, removing-things)
  are not yet checked against 4.1; `worker.md` was not brought over.
- Consider splitting the PR along the 5a-5d groups if the review is too large
  (26 files, +2,402/-704).
- The user's own DPE improvement ideas are still to come: ask before proposing.

## Update 2026-10-19

- The user opened the PR: juju/juju #23451 ("docs: 4.1 docs entity reference
  layers"), head `2576a81b14`, 25 commits, 26 files. No reviews or comments yet.
  GitHub reports it as not mergeable ("dirty"): upstream/4.1 moved to
  `697840de09` (578 commits since the base) and changed `docs/reference/ssh-key.md`
  (SSH proxy docs), which conflicts with the rewritten page.
- All 184 error strings on the 24 pages still exist in the upstream/4.1 Go
  sources (existence only; raise sites not re-checked).
- ssh-key.md narrative is stale, and was stale at my base: the machine-agent
  `sshkeyupdater` worker only injects and removes ephemeral keys for the SSH
  reverse tunnel (sshsession); it does not sync user keys onto the `ubuntu`
  account. User keys now authenticate users at the controller's SSH server. The
  persistence projection and watcher sections need re-reading against
  `domain/ssh`, `domain/keymanager`, `domain/keyupdater`. Lesson: the error
  inventory was verified at the raise-site level, but the execution-layer
  narrative was carried over from the prep branch and only partly re-read.
- Domains with the most code churn since the base (commits touching non-test
  code): network 24, removal 22, crossmodelrelation 22, application 18, relation
  15, machine 13, resource 11, modelmigration 11, ssh 10. Re-verify the
  execution narrative of the pages behind these first.
- #23427 (4.1-docs-dissolve-contributor-tree, PR 1) is still open at
  `03ec8ddc55`: 18 commits on base `5498725be0`, 578 behind upstream/4.1. It
  conflicts with upstream/4.1 by itself on `docs/conf.py` and
  `docs/reference/jujud.md` (PR 3 renamed jujud.md to jujuagentd.md; keep the
  `(jujuagentd)=` label in jujuagentd.md). It shares no file with #23451, and
  the entity pages link no `docs/contributor` label.
- Next steps (not started): rebase the entity branch onto upstream/4.1 and
  resolve ssh-key.md; rewrite the ssh-key execution layer from the current
  source; sweep the high-churn pages; ask before any push (origin only).

## Update 2026-10-19 (later): #23427 rebased locally

- Worktree `~/git/misc/juju-pr1`, branch `4.1-docs-dissolve-contributor-tree`,
  rebased onto upstream/4.1 `697840de09`: 17 commits (was 18; old tip
  `03ec8ddc55` stays on origin until the force-push). NOT PUSHED yet; the push
  needs `--force-with-lease=4.1-docs-dissolve-contributor-tree:03ec8ddc55`.
- Conflicts: `docs/conf.py` (both sides added redirects; kept both) and
  `docs/reference/jujud.md` (upstream renamed it to `jujuagentd.md`, which
  already defines `(jujuagentd)=`): the commit "add the jujuagentd label to the
  jujud page" was SKIPPED. `range-diff`: 15 patches identical, 2 differ in
  context only, 1 differs by the `conf.py` resolution.
- Verified: purged dirhtml build has no real warnings (baseline upstream/4.1
  also none; the totals differ only by "unknown node type" meta lines from the
  deleted contributor pages: 159 baseline, 130 here); the 12 touched `doc.go`
  packages build (`go build` exit 0); `gci` shows no diff; no `cmd/<binary>/`
  import path outside its binary.
- The PR text needs one edit: delete the first sentence of the "Drive-by
  improvements" paragraph ("The `jujud` page now defines the missing
  `jujuagentd` label ... no warnings.") and keep the "Merging patches forward"
  sentence. The test plan's "no warnings" claim still holds.
- New docs venv (the old ones broke with the OS upgrade to Python 3.14):
  `~/git/misc/docs-venv`, built from the PR's `docs/requirements.txt`
  (Sphinx 7.4.7, ggarch pinned). The build script lives in the session
  scratchpad; recreate it as `source docs-venv/bin/activate; sphinx-build
  --keep-going -b dirhtml . _build -w <log> -c . -d .sphinx/.doctrees -j auto`.
- Mistake made and repaired: a failed `cd` ran the first rebase in the main
  checkout on the merged CLI-links branch; restored with `git reset --hard
  4bba4427f6` (reflog-verified); nothing pushed. Chain worktree steps with `&&`.

- PUSHED (user approved) to origin with --force-with-lease: 03ec8ddc55 -> 28426535f7. Remaining for the user: edit the PR text (drop the jujuagentd-label sentence) and merge.

## Update 2026-10-19 (end of session): #23427 merged; resume with #23451

- #23427 (dissolve contributor tree) is MERGED (user, after the force-push of
  28426535f7). Worktree `~/git/misc/juju-pr1` and branch can be removed.
- Next: #23451 (this branch, `4.1-docs-entity-reference-layers`, worktree
  `~/git/misc/juju-entity-ref`, head `2576a81b14`, not mergeable: conflicts with
  upstream/4.1 in `docs/reference/ssh-key.md`).
  1. `git fetch upstream`, rebase onto upstream/4.1 (expect the ssh-key.md
     conflict, possibly more: upstream moved ~580+ commits). Chain worktree steps
     with `&&`; never run a rebase without checking `pwd` and `git branch
     --show-current` first.
  2. Rewrite the ssh-key execution layer (and the persistence projection and
     watcher parts) from the current source: `internal/worker/sshkeyupdater`
     (ephemeral keys only), `internal/worker/sshsession`, `domain/ssh`,
     `domain/keymanager`, `domain/keyupdater`, the controller SSH server. Merge
     upstream's new ssh-key.md intro (SSH proxy, `{ref}juju-ssh`).
  3. Re-read the execution narrative of the pages behind the high-churn
     domains: network, removal, crossmodelrelation, application, relation,
     machine, resource, modelmigration.
  4. Restore the 4.1 prose the restructure drops and delete the six orphaned
     relation images (the user's go still pending); edit the PR text to match.
  5. Rebuild (purged; venv `~/git/misc/docs-venv`; build script must be
     recreated), diff warnings against a baseline of upstream/4.1, push to origin
     only after asking.
- Environment notes: the sandbox fails to start in this setup (bubblewrap
  user-namespace error), so git network access, go and sphinx run with the
  sandbox off; the old docs venvs are broken (Python 3.14); the preview script
  `preview-entity-ref.sh` points at a dead venv: change it to
  `~/git/misc/docs-venv/bin/sphinx-autobuild`.

## Update 2026-10-19 (template v2)

Separate from the work on #23451: the error template was revisited. See
`entity-page-form-v2-proposal.md` (proposal, worked migration example, derived
decisions) and ADR-016 "Amendment 2026-10-19 (PROPOSED)". It does not change
#23451's pages; it applies to follow-up PRs, one per operation, after #23451
merges.

## Update 2026-10-19 (session 77): rebased, execution layers re-read

- #23451 had no reviews or comments at the start of the session (fetched
  from the API); head was `2576a81b14`.
- Rebased onto upstream/4.1 `d9fe58a4a1`; the only conflict was ssh-key.md
  (upstream's new intro merged in). Old tip `2576a81b14` stays on origin until
  the force-push (`--force-with-lease=4.1-docs-entity-reference-layers:2576a81b14`).
  NOT PUSHED yet; ask first.
- Five new commits on top of the rebased 25 (30 total): ssh-key execution layer from the
  current source (sshkeyupdater = ephemeral tunnel keys only; user keys
  authenticate at the controller SSH server; keyupdater facade kept for old
  agents; persistence adds host key, port, virtual host keys, connection
  requests); machine reprovisioning; resource immutability and removal job;
  unit/relation/offer/model removal and CMR details; space/subnet network
  setup and controller network watcher; application constraints at deploy;
  3.6 import transformations.
- Purged dirhtml builds (this branch vs upstream/4.1 baseline): warnings match
  apart from "unknown node type" meta lines (+2 for the new access and watcher
  pages, -1 relation caption). The latex build has two duplicate-target
  warnings in a howto page this PR does not touch.
- Still pending the user's go: restoring the dropped 4.1 prose and the six
  orphaned relation images; splitting the PR. The PR text still needs its
  counts and the "What changes" bullets re-checked after those decisions.
- Track 2 (template v2) not started; waits for #23451 to merge and for the
  user's ratification.

## Update 2026-10-19 (session 77, later): pending decisions resolved by analysis

- Images: the six files (4 relation SVGs, 2 excalidraw sources) were orphaned
  only by this PR; the figures match the new prose, so they are back in
  relation.md. The five `hook-charm-lifecycle-*` PNGs were already unreferenced
  in upstream/4.1 and are not this PR's concern.
- Dropped prose: restored what is accurate and not already covered (charm
  track/risk/branch, secret identifiers, machine designations and base, action
  wait behaviour, credential purpose). Not restored: the old claim that secret
  names match `^([a-z](?:-?[a-z0-9]){2,})$`; that regex is enforced only on
  secret data keys (`core/secrets/createsecret.go`), and no name validation
  exists.
- Split: not now. The pages cross-reference each other (execution-layer labels,
  watcher page), so a split is a sequential stack onto 4.1, and no reviewer has
  commented yet. Revisit when review round 1 shows the size is the obstacle.
- PR text: edit the charm and relation bullets as in "What changes" above.
