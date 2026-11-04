# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 113, 2026-11-04 (E53-E56 surface closure and ownership traces; no docs-tree changes). The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

Archive convention: `prompts/session-<N>.md` holds the launch prompt of session N; this one is archived unchanged as `prompts/session-114.md`. **The whole archive is a public repo: https://github.com/tmihoc/juju-reference -- commit and push the session records at every close-out.**

## Start ritual

Restart the docs preview exactly as before:

```bash
cd ~/git/misc/juju-tutorial-diagrams/docs
source ~/git/misc/docs-venv/bin/activate
sphinx-autobuild --port 8003 --host 127.0.0.1 . _build -c . -d .sphinx/.doctrees -b dirhtml -j auto -D llms_txt_enabled=0 --ignore '_build/*' --ignore '.sphinx/*'
```

Check port 8003 first with `ss -ltnp 'sport = :8003'`; if an old docs preview holds it, verify cwd is the docs dir, kill that pid, and start fresh. Confirm the new listener pid and an HTTP 200 for a reference page. Whenever there is something to view, include the live-preview link (`http://127.0.0.1:8003/<page-path>/`).

Verify state at start:
- docs worktree `~/git/misc/juju-tutorial-diagrams` should be clean on `4.1-docs-illustrate-docs-juju-9635` at `48ef1fca17`, equal to origin.
- PR #23661 should still be open/draft on `juju/juju`, head `48ef1fca17`, base `e5db99d585` (use `curl`; `gh` is not installed).
- Selected-page counts baseline remains **960/674/204/182** from `python3 ~/git/misc/juju-reference/tools/count_errors.py ~/git/misc/juju-tutorial-diagrams`. Do not widen the counter or selected links without the user.
- No docs-tree changes were made in session 113.

## Session 113 state

Priority remained JUJU-10585 deliverable 1: derive a source-grounded subject/relationship map and usable internal form from the running system and supported surfaces, without mistaking page filenames or samples for global coverage.

Session 113 produced four bounded research outputs:

1. **E53: explicit surface continuation from E52**
   - Registered in `structure-discovery-plan.md` before investigation.
   - `work/surface-ledger-113.md` records nested docs and dynamic/registered surface families.
   - `work/subject-map-delta-113.md` records deltas against `work/subject-map-112.md`.
   - Nested generated docs are surface inventories, not page-per-file subject inventories:
     - CLI command pages: 160 `.md` including index; 159 command pages.
     - Hook-command pages: 39 `.md` including index; 38 command pages.
     - Configuration key lists, compute-resource local commands, introspection macros, Juju compatibility child page, and Kubernetes reuse snippets were accounted for.
   - Dynamic surfaces traced: HTTP routes, control-socket endpoints, CAAS/model restrictions, hook-command context sensitivity, Kubernetes storage provider behavior, and image metadata.
   - `script.md` already provides neutral `script`, `task`, and `operation` anchors; the open question is link/findability and call-specific differences, not a missing top-level operation page.

2. **E54: generated command surfaces against source registration**
   - `work/surface-inventory-113.md` records the reconciliation.
   - Generated CLI command docs exactly match the 159 ordinary non-alias built-in commands from `go run ./cmd/juju help commands` at the 4.1 source anchor.
   - 29 help-visible aliases are not generated as separate pages; aliases are redirects, not separate subject candidates.
   - Hook-command generated docs exactly match the 38 command names in `internal/worker/uniter/runner/jujuc/server.go`.
   - This establishes closed **name inventories**, not backend behavior, authorization, model-type support, hook-context success, live output or complete errors.
   - Conditional/dynamic exceptions: developer-mode `dump`/`dump-db`, local plugin lookup, and embedded-client whitelists.

3. **E55: backup subject trace**
   - `work/backup-subject-113.md` records the trace.
   - `create-backup` is an ordinary built-in CLI command at the anchor.
   - Source path: CLI -> `POST /backup` -> controller-admin HTTP route -> handler -> controller-machine backup creator -> archive containing controller export, every model namespace export, and referenced object-store content.
   - The worker uses a backup-creation lease so only one creation proceeds.
   - Backup is a controller-admin backup mechanism with CLI/HTTP surface and database/object-store archive content; it is not merely a CLI command and not solely a database page.
   - Candidate stable address: controller or database reference anchor such as `[controller backup]`, linked from `create-backup`, `database`, `object-store`, and recovery/upgrade material.
   - The upgrade how-to's 4.1 `create-backup` not-implemented claim conflicts with source and generated CLI docs. This remains a candidate docs correction only; no page edit was authorized.
   - No live backup, restore, provider/platform success, or best physical docs filename was proven.

4. **E56: model command block trace**
   - `work/model-command-blocks-113.md` records the trace.
   - `disable-command`, `enable-command`, and `disabled-commands` expose command sets `all`, `destroy-model`, `remove-object`, mapped to `BlockChange`, `BlockDestroy`, `BlockRemove`.
   - The Block facade is model-scoped: listing requires model read access; switching requires model write access.
   - The model DB stores seeded block types `destroy`, `remove`, `change`; `block_command` stores one optional-message row per type.
   - Common checker precedence: change; remove then change; destroy then remove then change.
   - Representative affected calls traced: model config set, `juju exec` operation creation, machine destruction, model destruction.
   - Ownership decision: model command blocks are model-owned controls, not access grants and not page-per-command subjects. Candidate stable owner: model reference anchor `[model command blocks]`.
   - Generated command-set prose includes `set-application-base` and `sync-agents`, which are not ordinary non-alias commands at the E54 anchor. Treat that prose list as a coverage lead, not exact proof.
   - No complete inventory of all blocked commands/facades, live rendering, force-option bypass behavior, or final docs heading was proven.

## Best next move

Start the next session fresh on **storage pool / storage instance / storage attachment ownership**, unless a pasted PR review batch preempts.

Why: storage is the next highest-value boundary uncertainty from E52/E53. It tests the subject/relationship rule on a hard case:
- pool = reusable model/provider configuration,
- instance = provisioned storage object,
- attachment = relationship between storage and unit/machine,
- provider/platform behavior = conditional limits.

Bound it tightly:
1. Register the probe in `structure-discovery-plan.md` before tracing.
2. Trace only pool create/list/update/remove API/service path, storage instance identity/provisioning path, attach/detach relationship path, and one provider condition as a limit.
3. Produce `work/storage-boundary-114.md` and update `work/subject-map-delta-114.md` only if ownership changes.
4. Stop before full provider matrix, all storage errors, all storage commands, or docs edits.

If the session feels token-heavy or quality starts dropping, propose a new session. The user explicitly wants best-next recommendations and new-session suggestions when quality/tokens make that better.

## Standing decisions and constraints

- Pasted PR review batches preempt research.
- No page, structure or repo-rule edits are authorized by research artifacts alone. Propose concrete edits and obtain explicit authorization first.
- Competency questions test relevance and coverage; they do not decide page boundaries, section ownership or ordering.
- Derive structure from the running system's subjects, relationships and behavior, not code organization, current pages, filenames, registries, or personas.
- A reference should be predictive in where information belongs and in what software behavior follows, with explicit limits.
- Registration is a lead, not proof of callable behavior.
- Source traces are not live tests; label them.
- Do not claim global completeness from samples or filename reconciliation.
- The checker-script move (`count_errors.py` and `check_page_rules.py` into `docs/scripts/`) still awaits the user's word.
- ggarch session-83 items 1-3 still await the user's pick.
- PR body paste is the user's action; keep `pr-description.md` current when relevant but do not queue the paste.

## Close-out rule for the next session

Overwrite this file, copy it unchanged to the next `prompts/session-<N+1>.md`, append the outcome to `SESSIONS.md`, update the current block in `HANDOFF.md`, commit and push the archive repo (`https://github.com/tmihoc/juju-reference`), then tell the user the one-line start for the next session.
