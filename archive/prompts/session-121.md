# Session 121 launch: advance the global reference structure

Read `HANDOFF.md` first and follow its current session-120 section. Read the active JUJU-10585 plan in `structure-discovery-plan.md`, `TODOS.md`, `work/global-skeleton-119.md`, `work/content-planning-algorithm-119.md` and `work/content-planning-slice-relation-120.md`. A pasted PR-review batch preempts other work; do not wait for one if none has arrived.

## Start ritual

1. Check `ss -ltnp 'sport = :8003'`; if a preview owns the port, verify its cwd is `/home/dora/git/misc/juju-tutorial-diagrams/docs` before stopping it. Start from that directory with `/home/dora/git/misc/docs-venv/bin/sphinx-autobuild --port 8003 --host 127.0.0.1 . _build -c . -d .sphinx/.doctrees -b dirhtml -j auto -D llms_txt_enabled=0 --ignore '_build/*' --ignore '.sphinx/*'`. Confirm listener and HTTP 200 for a reference page; give the preview URL when there is something to view.
2. Verify the docs worktree `/home/dora/git/misc/juju-tutorial-diagrams`, local tracking ref, PR #23661 via the GitHub API, and the established selected-page counts with `python3 /home/dora/git/misc/juju-reference/tools/count_errors.py /home/dora/git/misc/juju-tutorial-diagrams`. Session 120 checked docs clean at `48ef1fca17`, tracking the same SHA; PR open/draft at that head and base `e5db99d585`; counts 960/674/204/182. Those are historical observations. Do not widen counts or PR links.
3. Use the 4.1 source anchor `/tmp/juju-41-tree` at `e5db99d585`; never touch `/home/dora/git/juju`. Code is the source of truth; comments and existing pages are not evidence of behavior.

## Immediate goal

Advance the connected, system-derived global structure with a concrete result. A suitable next bounded question is the shared operation/task contract across charm actions and administrative exec: reuse existing source traces and anchors, preserve the unit-versus-machine target distinction, and identify which semantics are shared versus invocation-specific. Choose a discriminating question before source inspection; preregister predictions, falsifiers, threshold and caveats in `structure-discovery-plan.md`. Do not treat a command inventory, prior page placement, or reader questions as proof of a boundary. Competing layouts with the same facts can remain editorial ties; never claim source forces a unique file or that links prove reader benefit.

E69 passes only its bounded checks; it is historically contaminated and excludes individual command completeness. Hook metadata validation is not a hook-command context matrix. Preserve the relation/settings/context/leadership semantic split and partial `relation-set` address without generalizing it to all commands. Non-CLI reference pages remain client-agnostic: platform/API facts first, clients as examples or separate interface pages.

The 402-denied `WorkloadModel`, `HookCommandPages` and `KubernetesCloudAttributes` scopes must not be relaunched or worked around; report them and retain uncertainty. The other named potential defects and publication questions remain open in `TODOS.md` and the current handoff. Never document away a possible code defect.

Defer page, structural and repository-rule edits until the structure is settled and then obtain explicit approval of concrete changes. Preserve anchors and figures. Checker-script moves and ggarch session-83 items await the user's word. Maintain one integrated PR while keeping JUJU-10585, JUJU-10586 and JUJU-9635 acceptance distinct. The user pastes the PR body. Ask before every push to origin and never push material revealing security issues except hardening-style warnings.

## Close-out

Record preregistration, outcome, limits and exercised verification. Check both documentation builders when applicable. Update `HANDOFF.md`, append to `SESSIONS.md`, overwrite this prompt for the next session and archive it unchanged in `prompts/session-<N+1>.md`; commit only the session's archive records locally, stop its preview and give the user the launch instruction. Do not claim unrun builders, tests, live behavior or pushes.
