# Session 100 decisions (2026-10-22, attended)

From the page-decisions ask (answers verbatim-essential) plus
in-session investigations. The executed commits cite this file.

## Ask answers

- bundle.md: KEEP AS-IS. The facade and CLI are alive in 4.1
  (`juju export-bundle`, cmd/juju/commands/main.go:429; the
  `client/bundle` facade exists) and no bundle record lives in either
  database, so there is no schema/calls page to write.
- configuration.md + its nested key lists: CONTINUE AS-IS. List pages
  keep their own form (paradigm, session 94); the key lists are the
  anchor homes other pages cite.
- log.md: REWORK (executed, `3223dc2897`). Added the log change streams
  (WatchLoggingConfig, v2 WatchControllerLokiConfig) and the log calls
  (Reading the logging configuration, Reading the log forwarding
  endpoint) from the `agent/logger` facade (logger.go:104/:140/:167;
  Caller: machine, unit, application, and model agents,
  logger.go:71-74). Pinned the LogSink path: each machine agent writes
  its own logsink.log through its log sink (agent/logger.go:29
  PrimeLogSink; --log-to-stderr logs to stderr instead), the agent also
  streams its buffered records to the controller's logsink endpoint,
  the API server stores them through its LogSink
  (apiserver/apiserver.go:229-230), `juju debug-log` reads them back
  through the API, and with a log forwarding endpoint set the agent
  forwards to Loki instead.
- machine.md designations table: MOVE TO CLI DOCS (executed,
  `af7784dacc`). The shapes (`lxd:25`, `0/lxd/4`, comma lists) are
  juju-CLI argument grammar; the API takes structured placement plus
  directive strings (machinemanager.go:179). The table moved to
  placement-directive.md's `<machine>` location (the hand-written
  `--to` grammar page; add-machine.md/deploy.md are generated and
  untouchable), with the (machine-designations) anchor traveling so
  unit.md:119 and machine.md:105 links resolve unchanged.
- resource-compute.md: KEEP (investigated, then decided). machine.md's
  lede defines a machine as a compute resource, so the genus needs a
  definition home; the command list (`juju-exec`, `juju-introspect`,
  `juju-dumplogs`) is shared by both agent kinds — containeragent
  serves juju-exec/juju-introspect invocations of itself
  (cmd/containeragent/main_test.go:46-48) and the machine agent manages
  the juju-run→juju-exec symlink (internal/agent/machine.go:1007-1010).
  Tool/list pages keep their own form; no entity-form rework.
- scaling.md: KEEP (evaluated from first principles). The
  vertical→constraints / horizontal→units mapping is a spanning fact no
  single page states; three pages lean on it (manage-applications.md:192,
  high-availability.md:17, reference/index.md:115); four sentences, no
  maintenance cost. Dissolving would spread the mapping and break links.
- status.md: REWORK (executed, `20cb05bd99`). Kept the values tables
  and the `juju status` output mapping; dropped status.png — its
  transition content contradicts the standing rule (a status's
  transitions live in the call that changes it) and it was the only
  non-ggarch figure left on an entity page. Transition reasons live in
  the calls that change status (status-set hook command on unit.md and
  application.md; Juju sets error/terminated/unknown).
- telemetry.md: KEEP. Reported the section derivation in chat: the
  recipe's "each section only when its facts exist" — business metrics
  have no controller API surface (the model worker posts to Charmhub
  once a day), so they earn the lede and a prose section; tracing and
  log forwarding have controller records (schema), watchers (change
  streams: WatchControllerTracingConfig, WatchControllerLokiConfig),
  and a named surface (the control socket, calls). No section was added
  without its facts.
- Item 16 (the change-streams/hook-commands cycle): see the Verdict
  follow-ups below — the user asked for the boundary + Grice
  assessment before any verdict; delivered, two fixable gaps found.
- Item 18 (llms.txt): MEASURED, hurts; alt-only emission confirmed by
  the user and queued on the ggarch tool. Each `{ggarch}` embed inlines
  the ENTIRE juju.ggarch source (215,333 bytes, all 14 models) verbatim
  into the page's markdown export — never trimmed to the view. 57
  embeds = 12.27 MB = 84% of the 14.59 MB llms-full.txt; every entity
  page carries ≥215 KB before its prose (model page: 474 KB = 431 KB
  ggarch + 43 KB prose). Captions do NOT export (0 occurrences); the
  alt text exports once per figure as an HTML comment; 0 SVG leaks;
  llms.txt index unaffected (78 KB). The session-95 "~40 KB / ~1.7%"
  estimate undercounted (it measured only the caption/alt prose).
  Recommendation: teach the llms-markdown path in sphinxcontrib_ggarch
  to emit the alt text only (as image/figure nodes do) — recorded in
  ~/git/ggarch/TODOS.md session-100 block (session-74 item 3 is its
  ancestor).
- Item 19: SWEEP (executed, `89f6adfa86`). The remaining 29 schema
  captions (not 42 — the recipe keeps 14 sequence/state story captions,
  and 7 were the session-99 trial) now carry the takeaway; alt text
  unchanged on every figure; checker identical to HEAD baseline on all
  29 pages; counts unchanged; ggarch check green at 14 models /
  45 views / 22 sequences; both builders at baseline.
- Checker TITLES: ADD BOTH (executed with the sweep verification).
  `Agent facades` and `Agent kinds` joined the allow-list; agent.md now
  checks clean (0 findings).
- CancelTask: FIXED FOR 4.1 (user answer) — NO warning on action.md's
  Canceling section. The PR text's Please-check bullet is corrected at
  this session's PR-body draft.

## Verdict follow-ups (same session, after the user's answers)

- Item 16 (the cycle): the user asked whether hook.md is cut at the
  right boundaries and passes a Gricean check in general — a scout ran
  (HookBoundaryGrice), its key findings re-verified against the code:
  the boundaries are RIGHT (no section moves; the hook-command name
  links are the session-95 design; the exhaustive command list belongs
  to the list pages; `collect-metrics` does not exist in 4.1 — only a
  stale comment at runhook.go:284 — so its omission is correct). Two
  verified gaps, both fixable in place: (a) the generic env-vars
  section misses the tracing configuration
  (context.go:1439-1441: JUJU_CHARM_TRACE_CONFIG_HTTP/_GRPC/_CA_CERT,
  documented on telemetry.md:41); (b) "Other hooks" is the code's
  `unitHooks` (hooks.go:107-118) and is missing `leader-elected` and
  `leader-deposed` (no pages exist; plain code font). Reported to the
  user with the recommendation: fix in place, one commit — their word
  launches it.
- Item 18: alt-only emission confirmed — queued in ~/git/ggarch/TODOS.md
  (session-100 block) with the measured evidence (12.27 MB = 84% of
  llms-full.txt is verbatim fenced model source; captions don't export;
  alt text exports once per figure).
- The linking sweep: EXECUTED and pushed as `2590d1a5c6` — 24 recorded
  no-link sentences across 10 pages (cloud, credential, lease,
  link-layer-device, offer, relation, secret, space, ssh-key, subnet),
  every other page's subject now hyperlinked; checker identical to
  HEAD on all 10; counts unchanged; both builders at baseline. The
  recipe-compliant restatements stayed (agent Caller identities per
  calls-intro; the machine-agent definition on storage.md:138).
- The PR body: drafted in pr-description.md — header now
  sessions 86-100; "The form" gained the schema-figure caption rule;
  "What this PR adds" gained the cross-page density/facades bullet
  (including the 24-link commit); the questions now read ImportKeys,
  lifeflag/facade.go:62, the application login
  (caasapplicationprovisioner/worker.go:171), creating a machine,
  revoke-below-level, the object-store lease, the how-to
  disagreements — CancelTask resolved OUT (fixed for 4.1, no warning on
  action.md). The user pastes the fenced blocks; totals unchanged at
  956/674/204/182 (the count tool's universe parse re-verified: 35
  slugs from the links line).
- The user's next-stream pick: the ggarch tool queue (ARROWHEAD_SIZE
  geometry.py:29, the state renderer's pinned exits
  state_renderer.py:328-336, the llms alt-only emission).

## Executed this session (all pushed, branch even with origin)

- `3223dc2897` — log.md rework (calls + change streams + LogSink path).
- `20cb05bd99` — status.md: transitions figure and status.png dropped.
- `af7784dacc` — machine designations moved to placement-directive.md.
- `89f6adfa86` — the 29-caption schema sweep.
- `2590d1a5c6` — the linking sweep over the recorded no-link sentences.
- The space/subnet/zone/link-layer-device sweep slice ran in-session
  (cluster 6 recorded in `work/duplicate-facts-99.md`; 21 of 35 entity
  pages swept, 14 remain, all list/concept-class).
- The checker TITLES allow-list addition (tools/check_page_rules.py,
  juju-reference local).
- Session totals: five docs commits plus the local checker/work-file
  updates; counts 956/674/204/182 verified after every commit; both
  builders at baseline after every commit.

## Still open after this

- The hook.md in-place fix (the two verified gaps: tracing env vars;
  leader hooks in a "Unit hooks" subsection) — one commit, awaiting
  the user's word.
- The PR body paste (the user pastes the fenced blocks from
  pr-description.md).
- The PR-text code questions ride in the pasted body (lifeflag,
  the application login) — recorded in work/agent-facades-99.md.
- The ggarch tool stream (the user's next pick): ARROWHEAD_SIZE
  (geometry.py:29), the state renderer's pinned exits
  (state_renderer.py:328-336, then audit Model migration phase,
  Relation status, Upgrade state), the llms alt-only emission.
- The CI-lint stream; fix 15 (needs the router work).
- The 14 unswept entity pages (list/concept-class; low priority).