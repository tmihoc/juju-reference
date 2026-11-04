# Session 115 launch: Juju reference first principles

Read `HANDOFF.md` and the **Current JUJU-10585 delivery plan** at the top of `structure-discovery-plan.md`, then begin the plan. A pasted PR review batch preempts research. Do not wait for one if none has arrived.

## Start ritual

1. Restart the docs preview. Check `ss -ltnp 'sport = :8003'`; if an old preview owns the port, verify its cwd is `/home/dora/git/misc/juju-tutorial-diagrams/docs` before stopping it. Start from that directory with `/home/dora/git/misc/docs-venv/bin/sphinx-autobuild --port 8003 --host 127.0.0.1 . _build -c . -d .sphinx/.doctrees -b dirhtml -j auto -D llms_txt_enabled=0 --ignore '_build/*' --ignore '.sphinx/*'`. Confirm the listener and HTTP 200 for a reference page. Give `http://127.0.0.1:8003/<page-path>/` when there is something to view.
2. Verify the docs worktree `/home/dora/git/misc/juju-tutorial-diagrams`, its tracking ref, PR #23661 via the GitHub API, and the established selected-page counts with `python3 /home/dora/git/misc/juju-reference/tools/count_errors.py /home/dora/git/misc/juju-tutorial-diagrams`. At session 114 start the docs branch was clean at `48ef1fca17`, equal to origin; the PR was open/draft at that head, base `e5db99d585`, and counts were 960/674/204/182. These are historical observations, not current assertions. Never widen the counter or selected links without the user.
3. Use the 4.1 source anchor `/tmp/juju-41-tree` at `e5db99d585`; do not touch the main checkout `/home/dora/git/juju`. Source traces are not live controller or provider evidence.

## Immediate goal

The user challenged the earlier drift toward command inventories and isolated traces. Produce **one coherent source-grounded model of Juju's running subjects, relationships and behavior**, not a list of existing pages, commands, tables or Go packages. For each subject/relationship capture what it is, scope, independently varying behavior, dependencies, effects, and conditions or limits. Include controllers, models, applications, units, charms, relations, infrastructure and connecting mechanisms across the defined reference scope. Reuse prior evidence; investigate a gap only when it can change a structural boundary. Show uncertainties and exclusions. The existing `work/subject-map-112.md` and `work/subject-map-delta-113.md` are inputs, not a completed system model.

Then follow the recorded plan: derive stable reference addresses and common/conditional entry parts from the system model; preserve the user's settled causal-chain order; compare with the alphabetical TOC and PR only after deriving the structure. Pre-register held-out predictions, falsifiers, thresholds where meaningful and caveats before testing. Include unexamined entities, a relationship and a cross-subject mechanism; report failures. If comparing forms, hold content constant. No human raters. Finally propose an application disposition across the defined entity-reference set and supporting pages, then translate supported principles into shared contributor/bot guidance. Pasted review batches preempt. No page, structural or repository-rule edits without explicit approval.

## Anti-drift and evidence

- The goal is an explanatory and predictive structure: it explains similarities and differences, predicts where facts belong and supports behavior deductions under stated conditions. Competency questions test relevance and coverage, never boundaries, ownership or ordering. Existing pages and how-tos are comparisons, not proof of correct chunking.
- Command-name and filename counts are consistency or discovery aids, not epic progress or evidence of structural correctness. Do not substitute broad interface/provider/field/error inventories or isolated traces for the system model. Check earlier decisions before repeating a question.
- `structure-discovery-plan.md` records the active plan and experimental history. E37/E38 and E47 undermined mechanical grouping/worker-owner rules. E44 did not establish the old form helps across tested pages; content and form were confounded and its equal-content control was not run. E50/E51 and E57/E58 are bounded evidence, not a complete theory. Finite tests cannot establish global completeness.
- Session 114: `work/storage-boundary-114.md` and `work/filesystem-lifetime-114.md` trace storage boundaries and an EBS-backed filesystem counterexample to the reference's unconditional machine-lifetime claim. Actual provider composition helpers ran; no live cloud or removal job ran. No docs correction was applied.
- `docs/reference/script.md:15,24` defines tasks and operations only for units, while `apiserver/facades/client/action/operation.go:241-261,296-310` accepts machine targets and returns machine task results. This is source-traced, not live tested: an existing anchor is not proof of an accurate contract. `hook.md:12,45` also overgeneralizes database/watcher initiation; the `update-status` timer is a source-traced exception. No page edits were authorized.
- Existing `docs/agents/AGENTS.documentation.rules.md:465` says a reader's question decides ownership; that conflicts with the user's later decision that questions test relevance/coverage only. Propose reconciliation; do not edit rules unprompted.
- Three epics remain distinct but share the one integrated PR: JUJU-10585 reference paradigm and defined entity set; JUJU-10586 client-visible error contract and enforcement; JUJU-9635 figures and contributor process. Do not treat error counts, diagram counts or checker success as proof of 10585. No silent PR split.

## Other gates

The checker-script move (`count_errors.py`, `check_page_rules.py` into `docs/scripts/`) and ggarch session-83 items 1-3 await the user's word. The user pastes the PR body. Push only to origin and ask before every push. Record results and caveats; recommend a fresh session when quality warrants it.

## Close-out

Update `HANDOFF.md`, append to `SESSIONS.md`, overwrite this launch prompt for the next session and archive it unchanged in `prompts/session-<N+1>.md`. Commit the archive records, ask before pushing to origin, stop the session's preview, and give the user the one-line launch instruction. Do not claim unrun builders, tests or live behavior.
