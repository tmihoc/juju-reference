# TODOS -- live queue (restructured 2026-09-26, addendum 114)

**LOCAL-ONLY: gitignored; never commit, push, or track.**

**Structure (session-23/24 bridge, reviewer-ratified):** this file
holds ONLY the live queue + the parked list. All history, verdicts,
and verbatim records live in SESSIONS (append-only) — re-read them
there, never here. Pre-2026-09-26 content: TODOS-archive-2026-09-26.md
(2469 lines) + SESSIONS. The prior 2469-line file conflated ledger +
queue + verbatim notes; the true open set was the triage below.

**RATIFICATION (session 26):** the reviewer's ordering directive — all
NON-ARCHITECTURE text work first (contributor + entity reference), then
diagrams, then the architecture text.

**PROCESS LAW (session 34, reviewer directive, binding):** "I don't like
it when you ask me for verdicts -- if a verdict doesn't jump out of the
page, then it's not the right verdict." Design answers present the worked
artifact so the verdict is self-evident; asking "which do you prefer?" is
the failure signature. If the choice is genuinely open, the artifact is
not yet right. (Sharpens the session-33 worked-example rule.)

**PROCESS LAW (session-48 post-close, reviewer directive, binding —
extends the session-34 law):** "I don't want us to deal in verdicts. I
want us to tease things apart until the right thing to do becomes
obvious." ADR-013 is the exemplar — teasing access apart is what
surfaced the associative-entity class (true entities are those with a
lifecycle in the DPE sense) and refined the primitive bits inventory
mid-push. The target is the emergent insight, not the decision: present
teardowns (what does the record say, where does each rule live, what
does the DPE coercion force and reveal), not option menus. The DPE
Procrustean bed is the tease TOOL: forcing material into a layer is how
fuzzy content is discovered and how the framework gets refined.

**SESSION 100 QUEUE (2026-10-22, live; measured on the JUJU-9635 PR tree, session 74 item 3 confirmed and quantified):**
1. DONE (session 101, pushed to origin/hide-fields): fix (a) taken — `de31c15` teaches the llms-markdown path to emit the alt text only (plus a fallback line), dropping the fenced source; measured on the real tree: 15 MB → 3.1 MB of markdown, 57 fences → 0, one alt comment per figure, model.md 460 KB → 40 KB; `104199a` in the same push makes the drawn head size a style knob (`arrowhead-size`, default edge style only). Historical record: each `{ggarch}` embed inlined the ENTIRE model source (215,333 bytes, all 14 models of docs/juju.ggarch) verbatim into that page's markdown — never trimmed to the view. Measured on a fresh `sphinx -b llms-markdown` build: 57 embeds = 12.27 MB = 84% of the 14.59 MB llms-full.txt; every entity page carries at least one full copy (the model page: 474 KB total = 431 KB ggarch + 43 KB prose). The captions do NOT export (better than feared); the alt text exports once per figure as an HTML comment; 0 SVG leaks; the llms.txt index is unaffected (78 KB). The session-95 estimate "~40 KB / ~1.7%" undercounted: it measured only the caption/alt prose, not the fenced sources. Fix candidates were: (a) teach the llms-markdown path in sphinxcontrib_ggarch to emit the alt text only, as image/figure nodes do (preferred: the alt text is the figure's own inventory, written for this); (b) emit only the selected view's slice instead of the whole model. The user's item-18 decision is closed by the push (juju-reference work/decisions-100.md, work/general-method-101.md).

**SESSION 83 QUEUE (2026-10-20, live; epic JUJU-9635, the user's notes on the model page):**
1. Captions: inline code does not render. A slide caption such as "In `quiesce`, the model's agents stop their work" shows the backticks literally (slideshow figcaption is set from `data-caption` with `textContent`; check the plain-figure caption path too). Render inline literals (and emphasis) in `:caption:`, `:slide-captions:` and the modal caption, in the HTML, LaTeX and text builders.
2. Captions: support roles, at least `{ref}`, `{doc}` and external links, in `:caption:` and `:slide-captions:`. Today the caption is plain text, so a page cannot link a term it mentions in a caption (the pages' first-mention-link rule then has to be skipped there). Sphinx must resolve the reference at build time (also for the search index and the latex build); the slideshow's JS must swap rendered HTML instead of text.
3. Links in node and edge labels (ERD boxes, sequence messages, state transitions), as Mermaid allows with `click` and link syntax. Design points: label syntax (`[text](target)` or a `link:` attribute on the node or edge, with `{ref}` targets resolved by Sphinx); SVG referenced through `<img>` is not interactive, so linked figures need inline SVG (or `<object>`), which also affects the expand modal, dark mode and the LaTeX/PDF build (use plain text there). Difficulty: medium to high.
4. Slideshow: keep previous and next, the counter and the arrow keys in the expanded (modal) view, and sync the page slide on close. Fix in `_GGARCH_JS` of `src/ggarch/sphinxcontrib_ggarch.py` (about 60 lines plus CSS, plus a test on the generated script). Difficulty: low to medium. Also seen on `explanation/architecture.md`.
5. DONE (000384e on `hide-fields`): state view ports spread, so the exits of downward transitions start at the middle of the bottom face and the arrivals spread along the target's left face.

**SESSION 73 QUEUE (2026-09-29, live; the 4.1 docs split, PR 4):**
1. `deployed` notation: DONE (f4b13f1): `deployed: true` draws a cloud badge top-right in the border colour; the empty inner boxes are gone
   from docs/juju.ggarch. ADR-015 updated. (The reviewer: "yes".)
2. ggarch CI check: DELIBERATELY SKIPPED in PR 4. Revisit when several people edit docs/juju.ggarch or at the first entity-reference PR:
   one step in the existing juju `.github/workflows/docs.yml` (on docs/*.ggarch changes): install the pinned ggarch, `ggarch check
   docs/*.ggarch`, fail the docs build on `ggarch parse/validate error` lines. Later port the grounding gate
   (docs/tools/check-grounding.py) and the geometry audit with the entity pages. Recorded in
   ~/git/misc/juju-architecture/pr-split-plan-4.1.md and in Claude memory (ggarch-ci-check-todo).
3. README.md: the "Check and render" example is stale (`ggarch render f.ggarch "View" --out x.svg`); the real form is
   `ggarch render f.ggarch --view "View" --out STEM` (writes STEM-light.svg and STEM-dark.svg); `render-seq` likewise.
4. Prep-branch models and pages need a look under the new grammar before their PRs land: diagrams.md and the entity pages (colours,
   badges, transparent canvas, the record/database orange), `type: container` -> `node` (alias works, rename is optional).
5. Sphinx extension: emitting the modal's dark rules for "auto" pages is done (6bfab23); check the same for any other place that assumes
   an opaque canvas (legend strip swatches, slide nav) once a page with them lands on RTD.
6. ERD halos and generalization triangles still fill with the canvas colour; make them mask-based (like the sequence lifelines) before
   an ERD view is embedded on a page whose background is not white or #1E1E2E.
7. Pin discipline: docs/requirements.txt pins ggarch by full SHA; bump it (fixup into the build commit) whenever a diagram needs a newer
   renderer, and re-point the docs venv from the editable checkout back to the pin before opening/updating the PR.

**SESSION 76 QUEUE (2026-09-30, live; entity-reference wave, form before PRs):**
1. The user's thoughts on improving DPE: pending, ask first; nothing is proposed before they are given.
2. Rulings owed on agent, database, zone, hook (ADR-013 amendment has the working assignment; the user decides).
3. DONE (session 76): ADR-016 applied to all 24 entity pages on `4.1-docs-entity-reference-layers` (worktree `~/git/misc/juju-entity-ref`, 25 commits, unpushed, build clean vs baseline). NEXT: the user reviews; ask before any push; PR text; consider splitting the PR by group.
4. DONE for type 1-2 pages. STILL OWED for types 3-11 (claim checks against 4.1: agent, pebble, jujuagentd, containeragent, database, log, status, telemetry, hook, configuration, metadata, HA, scaling, removing-things, upgrading pages gone) and the watcher/worker pair (worker.md not brought over).
5. Re-cut the 5a-5d split by type (see `reference-page-types.md`), after 1-2.
6. Decide whether the missing entities (model migration, secret backend, block commands, firewall rules, model defaults) get pages.
10. Template v2 (ADR-016 amendment 2026-10-19, PROPOSED; `~/git/misc/juju-reference/entity-page-form-v2-proposal.md`): after #23451 merges, one PR per operation (migration, removal, cross-model, deploy/upgrade) with reference rows and howto pointer together; build the error-index generator and its CI check; the user ratifies the amendment by reading it.
9. Error inventory vs how-to troubleshooting (analysis in `~/git/misc/juju-reference/error-inventory-vs-howto-troubleshooting.md`): migration bullet set in model.md, generated error index + constant coverage check, message-shape item in ADR-016; pages/sections for modelmigration, removal, secretbackend, objectstore, agentbinary, crossmodelrelation; fix or retire the two stale migration howto entries. Awaiting the user's go.
8. Port the 41 removed diagram views into docs/juju.ggarch (manifest: `~/git/misc/juju-reference/fence-manifest.md`), verified against the 4.1 schema, one PR per group; ggarch CI check due with the first.
7. `provisioning error` retry sentence (prep machine.md): no source support found; verify in the provisioner or drop.

**SESSION 75 QUEUE (2026-09-30, live; 4.1 docs PRs after review round 1):**
1. Edit the PR descriptions by hand (#23434 mgmt-space/caas-image-repo/redirect paragraphs, #23436 hook.md + llms-full.txt note, #23437 conf.py + typo, #23439 hook guarantees + caption); post the reply drafts; resolve threads (user).
2. Watch for round 2 from lee-van-cleef[bot] and from manadart/SimonRichardson (requested reviewers on #23434, #23437, #23439); re-fetch all PRs first.
3. Merge-order hazard: #23427 vs #23438 both touch docs/reference/jujud.md and the jujuagentd label; also docs/conf.py and docs/redirects.txt overlap across PRs 1-4 and the upgrade guide.
4. Decide ggarch distribution (canonical-owned mirror vs personal repo pin) for the bot's architecture note on #23439.
5. PR 5a-5d entity-reference split: wait for the user's go-ahead; 5a brings the ggarch CI check due; hook.md execution diagrams belong to 5c.
6. Follow-ups found: old-domain `juju.is` links (cmd/doc.go:22, log.md:26), robots.txt sitemap host, stale hook.Info comment, run-time check that the md-gen could render readonlyMethods (bot idea, not needed now).
7. (afternoon update) Re-check #23437 CI (attempt 2 of "Unit Tests / Test"; attempt 1 failed, cause unknown, suspected flake: ask the user to paste the failing test name from the job log). Re-fetch reviews of #23438 (bot and nvinuesa pending) and #23439 (bot round 2 on the caption/hook changes) before declaring either review-free. Simon to confirm the 17022 wording in the hardening guide (#23438). HOLD rebases until the user's next merge; afterwards rebase what is behind and re-check the #23427/#23438 jujud.md label overlap.
8. (afternoon update) Standing rules from the user: reviewer fixes go in separate commits (no force-push); captions start with their subject and point and carry the technical layer, main text stays light. Check every caption against them in PR 5a-5d pages.
9. (evening update) #23449 (RTD/PDF fix, branch 4.1-docs-fix-rtd-pdf-build, 5f7714b89c): get a human review and merge it, then confirm the next RTD build of 4.1 is green (the published docs have not updated since PR 4 merged). Pull ggarch main into ~/git/ggarch (1 behind). Consider tagging ggarch 85546a9 (v0.1.1) and revisit the canonical mirror question.
10. (evening update) Add a `-b latex` build (and text/markdown) to the pre-push checks for every ggarch renderer/extension change and every new docs directive; consider a CI step for `sphinx -b latex` in .github/workflows/docs.yml since the html job alone cannot catch this class of failure.

**SESSION 74 QUEUE (2026-09-30, live; PR 4 close-out):**
1. DONE: PR 4 force-pushed (0b5a6b3256); RTD build fine and the tab/slideshow/modal click-through works (reviewer, 2026-09-30). Now: act on the technical reviews with fixup commits (ask before every push).
2. A Juju engineer should confirm: per-model workers incl. the charm downloader; Kubernetes unit = pod with containeragent + Pebble; StatefulSet at bootstrap and namespace per model; strongly consistent database / eventually consistent units; the problem section's "nothing describes the whole deployment" claim.
3. llms/markdown visitor emits the whole model source per figure (~200 lines x 5 on the architecture page); emit only the selected view.
4. Person node label: diagram 1 says SRE (separate `sre` node), later diagrams say User. If more diagrams reuse the person, decide the label per story position.
5. Candidate house rules for docs/agents (explanation pages): diagram first in each section; links only in end-of-section See-more notes; the persona split; tabs sorted alphabetically; no progressive reveal outside tutorials. Propose after PR 4 lands.
6. Parked engine ideas: clickable node labels (needs inline/<object> SVG embedding); a "copy as light PNG on white" button in the expand modal (the transparent dark SVG pastes pale onto white).
7. Entity-reference split (plan item 5): PR 5a brings the ggarch CI check due (session 73 item 2).
8. History wart: commit 1 adds an older 568-line architecture.md that commit 3 replaces (per-commit history only).

**REVIEWER NOTES (session 52, EXECUTED, rule 5):** the reviewer's verdict on BOTH landed pages —
"Your rewrites made me very frustrated. I feel you aren't listening." Recorded VERBATIM in
build/review/feedback-compression-round2.md: the machine breakdown (the session-51 spec re-sent),
the FULL Gemini machine rewrite (new target density; sentence-case; numbered sections), the
controller diagnosis (meta-commentary / recursion inception / punt-style schema-gap explanations /
narrative walls) + editing blueprint (cut meta-commentary, flatten recursion, key-value spec
pattern), the AI-parse answer ("yes, I can parse it, but... I have to work hard"), and the
interjection: "bullets are not paragraphs in costume" — eliminate parenthetical interruptions
ENTIRELY, one fact per sentence, cut word count in half. Binding: both pages re-edited this round;
anchors + ggarch blocks byte-identical; facts re-grounded (grandparent string verified:
errors.go:37); Gemini's structural deletions (designations table, kinds h3s, state-machine views,
operations h4s, record-set bullet) FLAGGED for the reviewer, not executed.

**REVIEWER NOTES (session 51, EXECUTED, rule 5):** post-close feedback via Gemini on the LANDED
machine.md — "still a narrative hot mess". Recorded VERBATIM in
build/review/feedback-machine-compression.md; the three editing rules are BINDING corpus-wide:
(1) table-name-first bullets (`**`table` (concept):** mechanism`); (2) strip narrative filler;
(3) rules/errors in dedicated sub-lists. EXECUTED on machine.md (00afbe5447, pushed; 377 -> 224
lines; anchors + ggarch blocks byte-identical; facts re-packaged, none deleted). Sweep queue pending
the reviewer's read: controller.md FIRST, then the light pages.

**REVIEWER NOTES (session 65, live — content notes, NOT executed, triage owed):**
1. **charm.md's residual rules chapter — RETRACTED (reviewer, same session):** "I was
   looking at cached content. The errors are okay." The rules chapter stands as built
   (layer h2s + rules h3s, execution rules riding the legacy page-level anchor
   `(the-charm-rules-and-errors)` — not an issue per the reviewer). Nothing owed.
2. **The old Types-of-charm content — LIVE:** "It's just the types of charm that's an
   issue. What should we do with the old types of charm content? Do they fit anywhere
   in DPE?" Ground I see at the page: the `(types-of-charm)` h2 (charm.md:278) with five
   taxonomy h3s — substrates (:287), functions (:320), roles (:365), architectures
   (:385), generations (:406) — carrying 12+ h4 anchors (kubernetes-charm,
   machine-charm, infrastructure-agnostic-charm, workloadless-charm, configurator-charm,
   proxy-charm, integrator-charm, principal-charm, subordinate-charm, sidecar-charm,
   podspec-charm, ops-charm, 12-factor-app-charm, reactive-charm, bare-charm). Open
   question for triage: none of the taxonomy h3/h4s has a DPE home (a taxonomy is
   record-derived or client-projection content — cf. the secret.md Types /
   ADR-011-style stored-vs-derived calls); the anchor census + the "who links here"
   sweep owed before any verdict.
3. **Persistence-layer diagram presentation — SCHEDULED ROUND 10 (reviewer):** "we want
   the collapsed tables with the one(s) for the main entity in focus and with the text
   below describing things in prose rather than by the technical column (name) and in a
   way that's pruned by relevance. E.g., in machine.md, the machine_status table's
   `updated_at?` is really just internal stuff, nobody needs to know that." Reference
   form = the "Charm origins" view (charm.md's first persistence diagram,
   juju.ggarch:3145; collapsed record chips, typed data edges, no fields blocks).
   DIRECTIVE (reviewer-confirmed): (a) the eight "X attributes" views (Machine,
   Application, Unit, Charm, Secret, Controller, Subnet, Relation — 48 fields-block
   nodes) convert to the collapsed-chip form; (b) chip labels PRUNED BY RELEVANCE —
   internal bookkeeping columns (the machine_status `updated_at` class) drop out of the
   labels entirely; (c) the prose below each diagram describes the records
   semantically, NOT column-by-column; (d) APPLIES TO EVERY ENTITY DOC, not only the
   ones with diagrams: "Some entity docs never had a detailed persistence layer table.
   E.g., model.md. That doesn't mean what they have now is good. What each entity doc
   should have is a clean persistence layer section with a collapsed and focused ERD
   and some nice bullet points extracting from it the contract-level tl;dr (e.g., the
   fact that a model has an owner or configs, that level)." Pages without views get NEW
   collapsed focused views; every persistence section gets the contract-bullet form.
   MECHANICS (reviewer-directed): FIRST a backup of the pre-change files to
   ~/git/misc/juju-reference-persistence-full/ ("not sure if it's needed but I worry
   about losing all this crap") — WRITE-ONLY archive (the ~/git/misc contamination
   rule: never read back as records/state; restore byte-equal only at the reviewer's
   word), covering the entity pages + docs/juju.ggarch, with a manifest (HEAD sha,
   file list, checksums). Tension check on record: the fk-completeness validator law is
   unaffected — edges stay grounded on the FK columns; only the column rendering goes.
   Engine chain (audit-before dump, pytest ~413, make variants, check-ggarch) applies;
   every new/changed view lands in explanation/diagrams.md (the catalogue is the
   product surface); the prose-below rework rides the same round per page.
   PROGRESS (session 66, round 10 batch 1 LANDED at 63e28f82d2): backup taken
   (50 files, sha256-verified, WRITE-ONLY); Machine/Application/Unit/Charm
   attributes views CONVERTED (21 fields blocks deleted, FKs preserved as edge
   grounds), prose re-formed on the model.md pattern, 4 catalogue entries
   updated, gate + chain + served + rasters all PASS.
   PROGRESS (session 67, round 10 batch 2 LANDED at 574608b28e): Secret +
   Controller attributes views CONVERTED (the last 11 fields blocks; ALL
   EIGHT attributes views now chip-form), prose plain per THE AMENDMENT
   (zero DDL/table/column/view identifiers on both pages, served greps
   ABSENT), the previously-missing Controller attributes catalogue entry
   ADDED, gate + chain + served + rasters all PASS. NAMED: check-ggarch
   was RED at batch 1's HEAD (Application attributes ratio 2.03 > 2x,
   born in batch 1's chip heights); fixed in batch 2 by reordering the
   application fan (app_endpoint first, ratio 1.60). REMAINING: Subnet +
   Relation (the routing:orthogonal slices; kept-columns NOT yet proposed
   -- derive from the 0005-subnet-class DDL; the session-scoped
   local://round10-parts.md carried B1/B2 proposals only), then the
   residual identifier sweep (the census in the session-67 prompt), then
   the no-view pages (model.md the exemplar first).
   PROGRESS (session 67, same-session style sweep LANDED at 718d6944c4):
   the reviewer's unit.md style pass (no raw storage jargon in the
   conceptual overview; full-sentence bullet assertions) swept
   corpus-wide at the user's word: 25 files, all row/table narration ->
   record phrasing incl. captions + catalogue; ggarch untouched; one
   real relation.md duplicated-clause bug fixed by the sweep.
   PROGRESS (session 68, round 10 batch 3 LANDED at 4c780bf6de):
   Subnet + Relation attributes views CONVERTED (the last 16 fields
   blocks) — ALL TEN attributes views now chip-form, clause (a)
   COMPLETE; both keep routing:orthogonal (named); audits clean
   (Subnet/Relation strip-crossings + residuals -> 0); prose plain
   per the amendment, zero storage identifiers on both pages
   (served greps absent); gate + chain + served + rasters all PASS;
   parts list now at ~/git/ggarch/round10-parts-b3.md (gitignored
   repo-local; the session-scoped local:// class retired). REMAINING
   under this note: B4 the residual identifier sweep (recompute the
   census mechanically), then the no-view pages (model.md first,
   NEW views declared per batch).
   PROGRESS (session 69, B4 census presented + B4-1 LANDED at
   4133472636, pushed): census recomputed mechanically -- 12 live
   pages + 1 catalogue caption; model.md already clean; sanctioned
   NAMED (TF resource names, paas_charm, authorized_keys, the
   juju-db-repl + cloud-list + introspect-macro surfaces); sync
   annex: 12 pre-existing page<->catalogue drift views + 5
   no-entry views, none identifier-bearing but the Storage pair.
   B4-1: storage.md -> contract bullets + the Storage model
   catalogue entry synced to the page block (byte-equal; drift +
   DDL cite cleared together); gates + chain + served all PASS.
   Reviewer's word: ADJUST FIRST -- B4-2 (action + script) BLOCKED
   on the named adjustments; session self-audit: form found
   corpus-consistent (candidates NAMED in the session log).
   PROGRESS (session 69, continued — reviewer adjustments LANDED
   at 4ac15dc315, both commits pushed): the four form laws + two
   riders recorded (REVIEWER NOTES session 69 below + gate 2.5);
   possessive headings KEEP their article (reviewer's call); the
   missed "Arrows carry multiplicities" delta corrected (the
   clause restored machine-form). B4-2..B4-5 + the three corpus
   sweeps = the NEXT session, MINIMUM STEERAGE (the reviewer's
   word: no mid-session check-ins, break before context
   degradation).
   AMENDMENT (reviewer, post-close, LANDED as 0e764a9159): the persistence
   prose drops the storage-layer vocabulary entirely -- no DDL file names, no
   table or column identifiers, no schema-view names ("we no longer show
   those column names in the collapsed view"). The round charter's "DDL file
   names stay as ground pointers" is RETRACTED. Batch 1's four pages swept
   (the DDL cites, the table/column code spans, the v_ view names, the
   charm.uuid class, "the X table has no type column" -> "the X record");
   the catalogue insert-at pointers and the Charm origins caption cleaned
   with them. THE LAW FOR ALL REMAINING BATCHES (secret/controller, subnet/
   relation, the no-view pages): plain prose only; chip labels keep their
   salient-column lists (unchanged); FK grounds stay in the ggarch edges
   (engine-side, untouched). Residual for the reviewer's word: other
   already-collapsed pages (storage.md "grounded in 0011-storage.sql" class)
   still cite DDL in prose/captions -- NOT swept, scope was the four batch-1
   pages.
   PROGRESS (session 71, CAPTION-DEDUPE + EM-DASH RESIDUAL SWEEP LANDED
   at cee5ee23db, pushed -- completed by a follow-up Claude Code
   session, see HANDOFF State): session 71 (omp) opened at the
   reviewer's go-word, made all 27 edits (caption-dedupe on every
   touched page + the em-dash-to-colon/comma/paren rewrite on
   agent/bundle/hook/tutorial-index/database/high-availability/
   status/jujuc/upgrading-things + the two explanation pages),
   self-reported gate 2.5 CLEAN on all 27 -- then crashed silently
   right after killing sphinx-autobuild for the purge build (five
   "continue" prompts, zero assistant output, session dead). Working
   tree was left uncommitted, service down, nothing pushed, no
   records written. A follow-up Claude Code session found the omp
   session log (~/.omp/agent/sessions/-git-juju/...01a0e9d0...),
   independently RE-VERIFIED gate 2.5 (still CLEAN), the row/table-
   jargon + diagram-kind-prefix checks (clean; the pre-existing
   juju-architecture.md Constraint/Status table refs + diagrams.md's
   sanctioned "in a row" alts are RESIDUAL, untouched, NAMED, not
   this round's scope), the anchor diff (zero, no anchors touched)
   and the truncation census (zero); then ran the purge build (exact
   3-warning baseline), verify-docs (PASS serverless), relaunched
   juju-docs-serve-floor, curled the changed pages (200) and
   round-tripped six rewritten sentences through the whitespace-
   normalized strip-tags check (2 false-positive raw ' -- ' hits
   were :caption: lines, exempt by the gate's own exclusion regex).
   Committed cee5ee23db, commitlint 0, pushed. B5+ (the actual new
   no-view-page work this session's cold-start prompt sequenced --
   model.md first) was NEVER STARTED; it is still sequenced, still
   waiting on the reviewer's word. NEW GOTCHA for Appendix B: an omp
   session can crash mid-chain (stop responding to "continue") after
   self-reporting gate-CLEAN but before the build/commit/push/records
   steps -- the working tree is a reliable record of what it actually
   did; a stalled session's OWN CLEAN claim should still be
   independently re-run, not trusted, before continuing the chain.
   PROGRESS (session 70, B4-2 LANDED at 7ead5b824d, pushed): action.md
   + script.md swept to the amendment law (opener links the model
   database via data-model-full-spine; record bullets sentence-form;
   the DDL cites + all table/view identifiers gone; status vocabulary
   + code symbols kept); the three action captions drop their kind
   prefixes, catalogue synced byte-equal; script's 12 pre-existing
   prose em-dashes rewritten (gate 2.5; front matter excluded) --
   DEVIATION NAMED: script.md prose em-dashes were not in the census
   surface, fixed because the touched page must pass the gate; the
   census recount found caption-embedded identifiers the session-69
   shorthand missed (action.md :70 + catalogue :95 operation_action;
   catalogue :564 offer trio) and two numeric deltas (resource-charm
   23 snake vs "25"; space 3 snake vs "1" -- subnet.space_uuid :58/
   :67), all NAMED before editing. Gates + purge build at the exact
   3-warning baseline + verify-docs PASS serverless + relaunch +
   3 pages 200 + strip-tags sentences + hrefs 200 + identifier greps
   ABSENT served; commitlint 0.
   PROGRESS (session 70, S1 LANDED at 9a09a26296, pushed): the
   caption kind-prefix sweep -- 104 prefix drops (34 reference page
   captions + tutorial/index x3 + juju-architecture x3 + 66
   catalogue captions, of which 62 prefixed + the two grid-block
   captions a nested-fence parser bug initially skipped + the
   Taxonomy tree/star pairs the three-kind list omitted); the four
   prefix kinds in the prompt extended with "Taxonomy tree: "/"Taxonomy
   star: " (kind prefixes, same law); :slide-captions: untouched by
   construction (single-line keys; the 3 known lines byte-equal);
   pre-drifted pairs dropped per-side, drift stays NAMED: 26
   caption-drift pairs + the alt drifts enumerated in the session
   log; OUT OF SCOPE (NAMED, pairless pages): the 4
   architecture-principles versions' 7 captions + the
   manage-the-databases how-to caption. Gates + purge build exact
   3-warning baseline + verify-docs PASS serverless + relaunch +
   14 pages curled + served caption greps show ONLY the
   slide-captions values; commitlint 0.
   PROGRESS (session 70, S2+S3 woven LANDED at 526f6d1304, pushed):
   the mass-noun heading articles drop on constraint + controller
   triples (cloud + credential landed with B4-4); the done-8
   persistence openers link their databases IN PLACE ("In the
   {ref}`model database <data-model-full-spine>`, ..." -- the
   adopted sweep form, DEVIATION NAMED vs storage's full-sentence
   exemplar: heterogeneous openers keep their sentence shapes); the
   user.md:146 opener stays unlinked (outside the done-8 scope,
   NAMED residual). Gates + purge build exact 3-warning baseline +
   verify-docs PASS serverless + relaunch + 9 pages curled +
   strip-tags/raw-HTML sentences + hrefs 200; commitlint 0.
   SESSION END: B5+ (model.md first) left sequenced, NOT run -- the
   cold-start prompt's stop rule. Carried unchanged: the reviewer's
   calls (charm.md:259 raiser, space.md:82 attribution, TODOS note 2
   verdict, the split-form FLAG), the PENDING list, the parked
   riders.
   PROGRESS (session 70, B4-5 LANDED at 49f200eafa, pushed):
   space/placement-directive/ssh-key/access swept (space + access
   openers link the model/controller databases; record bullets
   sentence-form; all DDL cites + table/view identifiers + the
   qualified subnet.space_uuid refs gone; the placement bullet keeps
   its non-database opener -- the directive is not stored, no
   database named; ssh-key's spine-linked opener stays). Space
   caption kind-prefix dropped, catalogue synced byte-equal, the
   pair's ALT stays PRE-DRIFTED (NAMED). Sanctioned kept:
   authorized_keys (SSH file), the TF resource names. The four
   pages' remaining prose em-dashes rewritten (style gate 2.5),
   access.md page-wide incl. 4 outside the persistence sections
   (DEVIATION NAMED). Gates + purge build exact 3-warning baseline +
   verify-docs PASS serverless + relaunch + 4 pages 200 + strip-tags
   sentences + identifier greps ABSENT served; commitlint 0.
   PROGRESS (session 70, B4-4 LANDED at d5b45816c8, pushed):
   cloud/credential/offer swept (openers link the controller
   database via (database)= -- the controller-database section in
   database.md has NO anchor, DEVIATION NAMED; offer links the model
   database; record bullets sentence-form; all DDL cites + table/
   view identifiers gone; auth-type vocabulary + identity pairs
   kept); the offer catalogue's two CMR captions drop prefix +
   identifiers per-side (the declared-arrangement pair is
   PRE-DRIFTED, page and catalogue captions differ -- drift stays
   NAMED, not silently fixed); S2 heading law LANDED for cloud +
   credential triples. Gates + purge build exact 3-warning baseline
   + verify-docs PASS serverless + relaunch + curls 200 + strip-tags
   sentences + hrefs 200 + identifier greps ABSENT served;
   commitlint 0.
   PROGRESS (session 70, B4-3 LANDED at 83bb9546fa, pushed):
   resource-charm.md swept (opener links the model database; record
   bullets sentence-form; the DDL cite + both patch-migration
   mentions + all 23 table/column/view identifiers gone; file/
   oci-image/available/potential kept); no view or catalogue entry
   exists for the resource domain (no caption work). Gates + purge
   build at the exact 3-warning baseline + verify-docs PASS
   serverless + relaunch + curl 200 + strip-tags sentences + href
   200 + identifier greps ABSENT served; commitlint 0.
PROGRESS (session 72, B5-1 LANDED at 0da3d18fb5, pushed): the
   no-view roll opens with model.md, the exemplar: a NEW collapsed
   focused "Model attributes" view declared in juju.ggarch (ER-hub
   slice, charm-origins form) + catalogue entry + page embed under
   § Models in the persistence layer. The view reuses the spine
   records (model/cloud/credential/controller/namespace/application)
   with ONE new node: the constraint record (mdl_constraint, the
   model_constraint link flattened in; grounded on the link because
   the quoted reserved-word "constraint" table is DDL-unresolvable
   to the grounding scanner -- NAMED). The model record chip is
   pruned to the salient columns (name, owner, life, type, cloud,
   credential), which also rebalanced the shared views: controller
   attributes + credential chain audit BETTER, full-spine metric
   flips 2<->3 on reruns = rule-3 variance (named nondeterministic
   class), gate exit 0. Not drawn, named in the catalogue caption
   tail: the model-life mirror, the model-database read-only
   identity copy, configuration, storage-pool registry, agent
   version, secret backend. "Model attributes" joins the
   synthesized-variant skip list (the parked
   synthesis-of-ER-forests item). Census: 0 new hits (the 11 hits
   are the pre-existing sanctioned geometric "in a row"/"Top row"
   surfaces). Gates: style 2.5 CLEAN, anchor set unchanged,
   truncation 0, purge build exact 3-warning baseline, verify-docs
   PASS serverless, relaunch ready, curls 200, strip-tags sentences
   + full alt served, identifier greps ABSENT served, 892 hrefs 0
   bad, catalogue anchor id family-form, raster proves the 7 chips
   + exactly the 6 story edges. Engine chain: audit-before gate
   PASS (baseline saved), pytest 413 passed 6 skipped, variants
   regenerated (no twin for the skip class), Principles grep 2,
   check-ggarch PASS. commitlint 0, pushed, tree clean.

PROGRESS (session 72, B5-2 LANDED at fa3eaffef7, pushed):
   resource-charm.md gains its collapsed focused "Resource
   attributes" view (the resource domain's FIRST drawn record set --
   nothing existed before; B4-3's "no view for the resource domain"
   superseded). 8 chips: the content record centred (revision,
   origin, state, poll time), the charm-resource definition west,
   the application usage east, the two store links above, the
   staged, retrieval and unit-copy records below (sub-fan form --
   the first attempt's 3-chip south fan failed the >2x traceability
   gate, max-ratio 2.07; the retrieval sub-fan landed it at 1.69,
   NAMED). Declared flattenings: kind/origin/state/retrieved-by
   vocabularies + the OCI metadata lookup fold into their chips;
   the composite definition pointer (charm_uuid, charm_resource_name)
   is grounded on charm_uuid (NAMED). Not drawn, named in the
   caption tail: the application/unit far sides, store-side object
   metadata, the application's Kubernetes-resources satellite. The
   catalogue gains its first reference/resource-charm.md section.
   SYNTH_SKIP gains "Resource attributes". Gates: style 2.5 CLEAN,
   anchors zero-diff, truncation 0, census 0, purge build exact
   3-warning baseline, verify-docs PASS serverless, relaunch ready,
   curls 200, strip-tags sentence + alt clause OK, identifier greps
   ABSENT served, raster proves all 8 chips (incl. the sub-fan
   retrieval chip; crop under the consent banner -- NAMED). Engine
   chain: variants regenerated, Principles grep 2, check-ggarch
   PASS, audit gate PASS (the only >2x in the failing rerun = the
   known nondeterministic "Relation settings permissions" class,
   gone on the passing rerun -- rule-3 variance), grounding clean
   of new problems. commitlint 0, pushed, tree clean.

PROGRESS (session 72, B5-3 LANDED at b4b442eb16, pushed): space.md's
   persistence diagram converts in place from the three-record spine
   chain (application -> space -> subnet) to the collapsed focused
   form under the KEPT "Network spaces" name (the content-name
   precedent; no inbound refs to rename). The space record sits
   centred (its name + the seeded alpha default), the cloud's
   provider-space identifier west, the application's default
   binding east, the subnets below. NEW spine record node
   provider_space_rec (the cloud's own identifier record for the
   grouping, at most one per space, 0008-space.sql) with its edge
   grounded on the space pointer. Not drawn, named in the catalogue
   caption tail: the endpoint bindings, the exposed grants and the
   constraints that name a space (pointers from other records). The
   page and catalogue blocks drop their :no-legend: and share the
   alt byte-equal; the entry's insert-at pointer corrected to the
   anchor-truth form. The declared view audits 0 defects (max-ratio
   1.00); the synthesized twin regenerates at 4 nodes keeping its 2
   accepted diagonals -- NO skip-list change needed (the 4-node hub
   synthesizes fine, unlike the attributes slices). Gates: style
   2.5 CLEAN, anchors zero-diff, truncation 0, census 0, purge
   build exact 3-warning baseline, verify-docs PASS serverless,
   relaunch ready, curls 200, strip-tags sentence + alt clause OK,
   identifier greps ABSENT served, raster proves the 4 chips + 3
   edges + legend. Engine chain: variants regenerated, Principles
   grep 2, check-ggarch PASS, audit gate PASS, grounding clean of
   new problems. commitlint 0, pushed, tree clean.

PROGRESS (session 72, B5-4 LANDED at a148f84bbc, pushed): user.md
   gains its collapsed focused "User attributes" view + its first
   catalogue section. 4 chips: the user record centred (name,
   display name, external flag, creator), the authentication record
   west, the permission grants east, the access-level lookup under
   them. Declared flattenings: user_password + user_activation_key
   fold into the authentication chip; the two vocab lookups fold
   into the access-level chip; the grant's composite level pointer
   (access_type_id, object_type_id) grounded on access_type_id
   (NAMED). Not drawn, named in the caption tail: the objects the
   grants name, last-login, SSH public keys, macaroon config. The
   carried residual user.md:146 persistence opener IS FOLDED IN
   (the B4-4 controller-database form: {ref}`controller database
   <database>`; the database page's controller section still has no
   anchor, deviation standing). The 4-node hub synthesizes clean:
   the twin passed the corpus tests (pytest 413, NO skip change,
   the Network-spaces precedent). Gates: style 2.5 CLEAN, anchors
   zero-diff, truncation 0, census 0, purge build exact 3-warning
   baseline, verify-docs PASS serverless, relaunch ready, curls
   200, strip-tags sentence + alt clause OK, the opener served
   linked (span-wrapped label; normalized check), identifier greps
   ABSENT served, 426 hrefs 0 bad, raster proves the 4 chips + 3
   edges (OCR-level label noise NAMED). Engine chain: variants
   regenerated, Principles grep 2, check-ggarch PASS, audit gate
   PASS (declared 0 defects, ratio 1.00), grounding clean. commitlint
   0, pushed, tree clean.

PROGRESS (session 72, B5-5 LANDED at a9054b8d15, pushed): offer.md
   gains its collapsed focused "Offer attributes" view beside the
   CMR machinery view. 3 chips: the offer record centred (name +
   published endpoints), the endpoint join record west (NEW node
   of_endpoint, the offer_endpoint table, edge grounded on the
   offer pointer; its far side the application endpoint flattened
   into the chip), the consumer connection records east. Not drawn,
   named in the caption tail: the application endpoints the joins
   name, the offer's users (controller-DB permission records), the
   consuming side's proxy application and remote-offerer record.
   The 3-node linear form synthesizes clean (declared + twin both
   audit 0 defects, ratio 1.00; no skip change; pytest 413). Gates:
   style 2.5 CLEAN, anchors zero-diff, truncation 0, census 0,
   purge build exact 3-warning baseline, verify-docs PASS
   serverless, relaunch ready, curls 200, strip-tags sentence +
   alt clause OK, identifier greps ABSENT served, raster proves
   the 3 chips + 2 edges + legend (the CMR view renders below).
   Engine chain: variants regenerated, Principles grep 2,
   check-ggarch PASS, audit gate PASS, grounding clean. commitlint
   0, pushed, tree clean.

PROGRESS (session 72, cloud unit LANDED at 9bd4ca52a4, pushed —
   MISLABELED, NAMED): the commit's subject/body are the OFFER
   message (the B5-5 message file was reused by mistake for the
   cloud commit; the content is the cloud unit's 3 files, 96
   insertions). Per the never-amend-a-pushed-commit law the
   commit stands as pushed; this record carries the correction.
   Content: "Cloud attributes" (ERD slice) + catalogue section:
   the cloud record centred (name, type, endpoints, CA), the
   region records west, the default configuration values east,
   the admitted authentication types below. Flattenings: the CA
   cert + endpoint fields fold into the cloud chip; region
   defaults into the region chip. Not drawn, named in the tail:
   the models/credentials that name the cloud, the seeded
   controller cloud. Gates: style 2.5 CLEAN, anchors zero-diff,
   truncation 0, census 0, purge build exact 3-warning baseline,
   verify-docs PASS serverless, relaunch ready, curls 200,
   strip-tags sentence + alt clause OK, identifier greps ABSENT
   served, single-block catalogue convention (twin not embedded),
   raster taken. Engine chain: variants regenerated, Principles
   grep 2, check-ggarch PASS, audit gate PASS (declared 0 defects
   ratio 1.00; twin 2 accepted diagonals), grounding clean, pytest
   413 passed. NO PROGRESS-DATA loss; the mislabel is a
   record-level defect, not a content one.

PROGRESS (session 72, constraint unit LANDED at 35ebd5987f, pushed):
   "Constraint attributes" (ERD slice) + catalogue section. The
   compute-spec record centred (arch, cpu cores, memory, root
   disk), the application's nullable constraint east, the machines'
   constraint below. The model's defaults ARE the focal record
   through the model-constraint link; the focal's ground names the
   link (the quoted "constraint" catalog is DDL-unresolvable, the
   mdl_constraint precedent, NAMED); the app/machine links grounded
   on their constraint pointers. Not drawn, named in the tail: the
   tag/space/zone lists, the owners the links name. One PRE-EXISTING
   prose em-dash on the touched page (the image-id note) rewritten
   to a colon (gate 2.5, NAMED). Gates: style 2.5 CLEAN, anchors
   zero-diff, truncation 0, census 0, purge build exact 3-warning
   baseline, verify-docs PASS serverless, relaunch ready, curls
   200, strip-tags sentence + alt clause OK, identifier greps
   ABSENT served. Engine chain: variants regenerated, Principles
   grep 2, check-ggarch PASS, audit gate PASS (declared + twin both
   0 defects, ratio 1.00), grounding clean, pytest 413 passed.
   commitlint 0, pushed, tree clean.

PROGRESS (session 72, ssh-key unit LANDED at cf76d94c6a, pushed):
   "SSH key attributes" (ERD slice) + catalogue section. The user's
   key record centred (material, comment, fingerprint), the
   fingerprint-algorithm lookup west, the per-model authorised-key
   projections east. The owning user folds into the key chip; the
   machines' host keys are PROSE-ONLY (no pointer to the key, the
   validator law) and the authorisation read is not drawn, both
   named in the tail. Edges grounded on their FK columns. Gates:
   style 2.5 CLEAN, anchors zero-diff, truncation 0, census 0,
   purge build exact 3-warning baseline, verify-docs PASS
   serverless, relaunch ready, curls 200, strip-tags sentence +
   alt clause OK, identifier greps ABSENT served. Engine chain:
   variants regenerated, Principles grep 2, check-ggarch PASS,
   audit gate PASS (declared + twin both 0 defects, ratio 1.00),
   grounding clean, pytest 413 passed. commitlint 0, pushed, tree
   clean.

PROGRESS (session 72, access unit LANDED at 90c806715a, pushed):
   "Access attributes" (ERD slice) + catalogue section (the first
   reference/access.md section). The permission grant record centred
   (level, object, user), the level-object pair lookup below, the
   access level vocabulary west, the object kind vocabulary east.
   The grant's pair pointer is the composite FK, grounded on its
   access-type column (the uz view's edge shares that ground —
   NAMED); the pair's own two vocabulary pointers grounded. Not
   drawn, named in the tail: the resolving views, the
   everyone@external group grants, the objects themselves. Gates:
   style 2.5 CLEAN, anchors zero-diff, truncation 0, census 0,
   purge build exact 3-warning baseline, verify-docs PASS
   serverless, relaunch ready, curls 200, strip-tags sentence +
   alt clause OK, identifier greps ABSENT served. Engine chain:
   variants regenerated, Principles grep 2, check-ggarch PASS,
   audit gate PASS (declared 0 defects ratio 1.30; twin 0 defects
   1.24), grounding clean, pytest 413 passed. commitlint 0, pushed,
   tree clean. (iii)-rest SCOPE NAMED: bundle.md EXCLUDED (its
   persistence section is "Nothing here, by design" — no records,
   no view); script.md EXCLUDED (the Operation hierarchy has a
   recorded single home on action.md, "moved off script.md");
   the remaining view units = placement-directive + zone.

PROGRESS (session 72, placement-directive unit LANDED at
   a4f49ad66a, pushed): "Placement attributes" (ERD slice) +
   catalogue section. The placement record centred (directive,
   scope), the machine it belongs to west (the real spine node),
   the placement scope lookup east. The directive values fold into
   the chips. Not drawn, named in the tail: the machine records a
   designation resolves to. Gates: style 2.5 CLEAN, anchors
   zero-diff, truncation 0, census 0, purge build exact 3-warning
   baseline, verify-docs PASS serverless, relaunch ready, curls
   200, strip-tags sentence + alt clause OK, identifier greps
   ABSENT served (the page's own "directive" subject word named as
   sanctioned). Engine chain: variants regenerated, Principles
   grep 2, check-ggarch PASS, audit gate PASS (declared 0 defects
   ratio 1.00; twin 2 accepted diagonals), grounding clean, pytest
   413 passed. commitlint 0, pushed, tree clean.

PROGRESS (session 72, zone unit LANDED at 8be3d1d325, pushed):
   "Zone attributes" (ERD slice) + catalogue section, the LAST of
   the B5 no-view roll. A zone is a value, not an entity: the
   availability-zone lookup record centred (its name), the
   subnet-membership join east. Not drawn, named in the tail: the
   machine instances that land in the zone, the constraints and
   placement directives that name it. SEVEN pre-existing prose
   em-dashes on the touched page rewritten (gate 2.5, NAMED).
   Gates: style 2.5 CLEAN, anchors zero-diff, truncation 0, census
   0, purge build exact 3-warning baseline, verify-docs PASS
   serverless, relaunch ready, curls 200, strip-tags sentence +
   alt clause OK, identifier greps ABSENT served, em-dash rewrites
   served. Engine chain: variants regenerated, Principles grep 2,
   check-ggarch PASS, audit gate PASS (declared + twin both 0
   defects, ratio 1.00), grounding clean, pytest 413 passed.
   commitlint 0, pushed, tree clean. B5+ COMPLETE: 11 view units
   (model, resource-charm, space, user, offer, cloud, constraint,
   ssh-key, access, placement-directive, zone) + the two named
   exclusions (bundle = no records by design; script = the
   operation view's recorded single home on action.md).

**REVIEWER NOTES (session 69, live — exemplar adjustments EXECUTED this session):**
1. **Heading article law (general, all reference docs):** "The storage
   in..." is awkward English -- no specific storage, storage in general:
   "Just say 'Storage'". LANDED for storage.md's three layer headings;
   corpus roll owed: cloud/constraint/controller/credential layer triples
   (+ the agent/database possessive forms -- reviewer's call).
2. **Caption kind-prefix law (NEW; retracts the prefix round fed1c9184a):**
   stop prefixing captions with the diagram type -- "if we have to say
   what kind it is we've failed already". LANDED for the Storage model
   pair; corpus = ~35 page captions + 66 diagrams.md catalogue captions
   (sweep round owed; the slide-captions per-slide kind leads =
   reviewer's call).
3. **Persistence opener law (worked example):** openers LINK the model
   database rather than naming it as a known thing: "Storage is persisted
   in the {ref}`model database <model-database>` as follows:" -- the
   <model-database> label does NOT exist; grounded to (data-model-full-
   spine)= (database.md "Model databases" section) -- DEVIATION NAMED.
   Rolls per batch; the done-8 pages need the sweep.
4. **Cardinality question (grounded answer):** ERD cardinality was never
   DRAWN -- engine cardinality is node-only (xN badges; 0 declarations
   in juju.ggarch current AND pre-roll); pre-roll carried "1/m at each
   end" as a legend clause, round 10 moved it to alt/caption text. The
   Storage pair's old "Arrows carry multiplicities" catalogue alt clause
   was dropped by the light-page re-form and B4-1's sync adopted the page
   form WITHOUT naming that drop (missed; corrected): the clause restored
   as "Each line is a stored pointer; 1/m at each end." (machine form).
   Drawn edge-end multiplicity = engine work if wanted.
5. **Focal-entity prominence TODO (reviewer: "do we have a TODO?"):**
   none existed -- Appendix C's parked visual-language rider covers chip
   style + node-label hyperlinks only -> focal prominence ADDED to the
   PARKED riders this session.
6. **Layout quality (reviewer's observations):** lines grazing edges,
   unnecessary diagonals, left-right/top-bottom flow possibly not
   preattentive -- engine-track; the audits measure crossings/turns/
   residuals but not grazing or preattentive flow -> PARKED rider added.

**SESSION 65 (2026-09-28, CLOSED): ROUND 9 (ssh-key.md) — juju = origin = cb0293fff1 (one commit, pushed); ggarch b264386 unchanged.**
ROUND 9 LANDED (cb0293fff1, 144+/88-): ssh-key.md on the entity-page
pattern. Ground first: 0021-user-ssh-keys.sql (user_public_ssh_key,
two unique indexes per user -- fingerprint AND material;
ssh_fingerprint_hash_algorithm md5/sha256) + 0022-model-authorized-keys.sql
(model_authorized_keys, the projection, composite PK, CONTROLLER
database; v_model_authorized_keys drops removed/disabled users' keys)
+ 0018-machine.sql machine_ssh_host_key (model database). Raiser
census per constant non-test by NAME: all FIVE raised (already exists
state.go:271; invalid public key service.go:159,:303; reserved comment
service :169,:313; unknown import source :283; subject not found
:288). Corrections pre-write: the constant is `key contains a reserved
comment` (the old `reserved comment violation` names nothing); the
RESERVED comment `juju-system-key` (types.go:9) vs the agents' `Juju:`
prefix (utils v4.0.5) are TWO comments the old page conflated; the
projection is controller-side; the watch surface EXISTS
(WatchAuthorisedKeysForMachine, keyupdater service.go:184, the
model_authorized_keys + user_authentication namespaces; one consumer
chain: agent keyupdater facade -> authenticationworker). CLI spellings
dropped. Unused surfaces stated: DeleteKeysForModel +
GetAllUsersPublicKeys, zero non-test callers. No ggarch view (census
pre-write). 7 anchors: (ssh-key) kept 3 inbound; 4 pattern slots kept;
NEW the two rules anchors; 4 DISSOLVED zero-inbound both forms.
Gate: style CLEAN first pass; truncation census clean; purge build at
the exact 3-warning baseline; verify-docs PASS serverless; relaunch
first-attempt ready; 9/9 anchor ids + 39/39 key sentences served; all
internal hrefs 200; rasters prove the ladder (5200px window = the
standing form for bottom anchors). Commit -F file; commitlint PASS
(--config form); push verified, tree clean.
NEXT: at the reviewer's word, the roll's next target (the records name
no next after ssh-key). Reviewer's calls still carried:
charm.md:259's second raiser; space.md:82's watcher attribution.
MANDATORY break after ~3 reviewer interventions. The split-form FLAG
(addendum 164) still parked. PENDING unchanged (rounds (a)/(b),
user-secret access-level, ADR-013 stamp, P0-1 pick, +BUBBLE-UP
SURFACES, the designations-split proposal, the S3-policy-JSON rehome,
the 3.x version-history corpus sweep; router-nondeterminism rider
parked). Chain + gotchas: HANDOFF Appendices A-C.

**SESSION 64 (2026-09-28, CLOSED): LEDGER READ (RATIFIED) + ROUND 8 (resource-charm.md) — juju = origin = 94de88a65a (one commit, pushed); ggarch b264386 unchanged.**
LEDGER READ: addendum 178's two-raiser `charm not resolved` amendment
re-verified at 0d17a7a8cb file:line and RATIFIED (application.go:1152;
state/charm.go:874; uniter.go:1139-1140; the errors.go doc comment
matches the availability raiser); the consumer NAME-census law
confirmed (WatchSubnets non-test = the firewaller facade + worker).
ROUND 8 LANDED (94de88a65a, 218+/124-): resource-charm.md on the
entity-page pattern. No ggarch view exists for resource -- persistence
= DDL prose + record bullets over 0015-charm.sql (charm_resource
composite PK (charm_uuid, name), charm_resource_kind file/oci-image,
v_charm_resource) + 0023-resource.sql (resource, the nullable revision
+ origin/state lookups; application_resource, resource_uuid PK = one
blob per application; pending_application_resource, the application by
NAME, no FK; resource_retrieved_by; unit_resource composite PK; the
per-type store links resource_file_store/resource_image_store; the
views v_resource COALESCE, the 0052 INNER-join v_application_resource,
v_unit_resource) + the 0054 patch (application_k8s_resources_managed,
the blocks-removal-until-cleared record, application.go:1080-1083).
Raiser census per constant non-test by NAME: 11 raised; two
ZERO-RAISERS stated (ResourceStateNotValid, ResourceAlreadyStored).
Corrections pre-write: the negative-revision vocabulary splits by path
(`argument not valid` service/resource.go:676 vs `resource revision
not valid` import.go:137 only); the removal surfaces have zero
non-test callers (the failed-deploy teardown
DeleteResourcesAddedBeforeApplication HAS its caller, application
facade :330-350); the `juju attach-resource` spelling dropped.
Execution split by owner (push / repository poll / revision update /
unit's copy / model import / pending teardown / unused removals);
watchers = NO watch surfaces at all (zero Watch in domain/resource
non-test). Gate: style CLEAN first pass; purge build at the exact
3-warning structural baseline (all three persisted in warnings.txt;
zero new); verify-docs PASS serverless; relaunched first-attempt
ready; served 7/7 anchors + 22/22 key sentences (two tag-boundary
variants); the-charm-origins href resolves; rasters prove the full
ladder, no duplication; truncation census clean; commit -F -; push
verified, tree clean. 7 anchors (6 dissolved zero-inbound both forms;
2 new; 4 kept pattern slots; (charm-resource) kept, 7 inbound).
NEXT: at the reviewer's word round 9 = ssh-key.md. Reviewer's calls
still carried: charm.md:259's second raiser; space.md:82's watcher
attribution. MANDATORY break after ~3 reviewer interventions. The
split-form FLAG (addendum 164) still parked. PENDING unchanged
(rounds (a)/(b), user-secret access-level, ADR-013 stamp, P0-1 pick,
+BUBBLE-UP SURFACES, the designations-split proposal, the
S3-policy-JSON rehome, the 3.x version-history corpus sweep;
router-nondeterminism rider parked). Chain + gotchas: HANDOFF
Appendices A-C.

**SESSION 63 (2026-09-28, CLOSED): LEDGER READ (RATIFIED, ONE AMENDED) + ROUND 7 (subnet.md) — juju = origin = 0d17a7a8cb (one commit, pushed); ggarch b264386 unchanged.**
LEDGER READ: addendum 177's six re-verified at 50cc351fb4, per-constant NAME
censuses (raiser sites use constant names, so string greps cannot see them):
five RATIFIED (the two zero-raisers errors.go:215,:258 + store.go:168-170's
prefix raiser; the reservation guards metadata.go:518-572 + actions.go:120 +
the charm-name exemptions meta.go:855-857, metadata.go:521-523; WatchCharms
zero non-test callers; the URL rephrase -- "registry host" gone, no host
parsing in url.go; the CLI drops), ONE AMENDED: `charm not resolved` has TWO
non-test raisers -- the wrong-UUID download resolve (application.go:1151-1152,
charm.md:259's entry) AND the archive-availability read (state/charm.go:873-874;
surfaces "not yet available" at uniter.go:1139-1140); the errors.go doc
comment's story matches the SECOND raiser; application.md:408's entry is that
raiser's; charm.md:259's completeness = the reviewer's call. The 858-char
sentence byte-equal at charm.md:409 (the records' :327 = the pre-rewrite
position). Corpus ellipsis census clean.
ROUND 7 LANDED (0d17a7a8cb, 163+/66-): subnet.md on the machine+controller
pattern -- declaration = the adoption + move acts + the-subnet-declaration-rules
(canonical CIDR, core/network/subnet.go:234-240; the move's constraint guards,
movesubnets.go:98-261; the VLAN non-gate stated; errors `subnet CIDR is not
valid` service/space.go:36-37 + `space not found` the move target,
state/space.go:226); persistence = the ggarch block byte-identical + record
bullets over 0009-subnet.sql + 0008-space.sql + the v_space_subnet reads +
the ip_address consumer + the-subnet-persistence-rules (idempotent adoption;
no-deletion; the alpha rewrite on space removal; `subnet not found` four
raiser groups); execution = the reload (discovery or fallback; the multicast/
link-local drop; the parse error FAILS the reload; the no-delete comment) +
the import (explicit space links; the CAAS fallback) + the unused update/
remove surfaces stated + subnet watchers (namespace `subnet`; the FIREWALLER
consumer -- facades/controller/firewaller/firewaller.go:409 +
internal/worker/firewaller/firewaller.go:286; no space watcher exists,
WatchSpaces zero matches). Corrections caught pre-write, named in addendum
178: the watcher consumer (the old "provisioning and address machinery"
attribution dropped; space.md:82 flagged), the VLAN non-gate, the uncalled
surfaces, the scout's parse-fail correction, the CIDR non-uniqueness grounded
on the code's own comments, the `juju subnets` spelling dropped.
Gate: style CLEAN first pass; purge build at the exact 3-warning structural
baseline (all three persisted in warnings.txt this time -- the exact trio,
zero new); service stopped before build; verify-docs PASS serverless
(worker-exit check first); relaunched under juju-docs-serve-floor,
first-attempt ready; curl 200 x3; served 7/7 anchors + 30/30 key sentences
strip-tags; the img pair + all SVG labels render; rasters prove headings/
lists/no duplication/no broken elements; truncation census + dup scans clean;
ggarch byte-identity re-proven. 7 anchors (5 dissolved zero-inbound both
forms; 2 new; (subnet) kept, 3 inbound).
NEXT: at the reviewer's word round 8 = resource-charm.md (its
the-charm-origins facade ref resolves), then ssh-key. Reviewer's calls carried
from this round: charm.md:259's second raiser; space.md:82's watcher
attribution. MANDATORY break after ~3 reviewer interventions. The split-form
FLAG (addendum 164) still parked. PENDING unchanged (rounds (a)/(b),
user-secret access-level, ADR-013 stamp, P0-1 pick, +BUBBLE-UP SURFACES, the
designations-split proposal, the S3-policy-JSON rehome, the 3.x version-history
corpus sweep; router-nondeterminism rider parked). Chain + gotchas: HANDOFF
Appendices A-C.

**SESSION 62 (2026-09-28, CLOSED): LEDGER READ (RATIFIED) + ROUND 6 (charm.md) — juju = origin = 50cc351fb4 (one commit, pushed); ggarch b264386 unchanged.**
LEDGER READ: addendum 176's five corrections ALL RATIFIED, re-verified directly at
172383d395: the `error` task status has NO writer (the one shared INSERT path,
operation/state/start.go:642; the writers are enqueue/StartTask/FinishTask/cancel;
`error` accepted as a completion + terminal for cancel + the empty-set operation
value, service/query.go:99-106); machine task notifications PENDING ONLY
(state.go:385-404, the machine statement filters `sv.status = 'pending'`; ABORTING is
the unit-side trigger, :369,:405); the JUJU_ACTION_* env vars live in the hook
context builder (uniter/runner/context/context.go:1459-1465); the wait/background CLI
drop stands; the anchor census holds (the five dissolved zero-inbound docs-wide, the
ten kept resolve). Nothing corrected.
ROUND 6 LANDED (50cc351fb4, ~90+/~50-): charm.md on the machine+controller pattern --
declaration = the two model-write acts + charm channels (track/risk/branch; the
four-risk ladder deployment/charm/channel.go; stable the default,
core/charm/channel.go:16) + charm revision (client-agnostic; the juju info/deploy
spellings dropped) + the-charm-declaration-rules h3 (the URL grammar, url.go:66,
:179-181,:333-336: schema ch|local, missing reads ch, name grammar, `-<number>`
suffix, optional supported architecture, no `~user`/query/fragment/user-info; errors
charm not found, origin not valid (core/charm/origin.go:65-69), source not valid;
the Charmhub API codes pass through, transport/error.go:61-92); persistence = both
ggarch blocks byte-identical (identity re-proven) + the unmodifiable-tables fact
(schema/model.go:264-267) + the available-flag projection grounded on the resolve
UPDATE (state/application.go:2164-2214; the local upload lands available,
service/charm.go:937) + the-charm-persistence-rules h3 (the record gates,
service/charm.go:876-948: metadata parses, name valid, manifest >=1 base Ubuntu-only
manifest.go:121,:126-128, download info required, sequenced revision unset :907;
8 error entries with Triggered/Remediation); execution = split by owner (the async
downloader downloadworker.go:168 + service/application.go:1128-1196; the revision
updater charmrevisioner/worker.go:508-552; removal DeleteCharmIfUnused only at zero
applications AND zero units, removal/state/model/application.go:815-856) +
the-charm-watchers h3 + the-charm-rules-and-errors h3 (the hash checks: the upload's
sha256 prefix store.go:169, the download's full sha256 application.go:1160).
THIRTEEN-plus grounding corrections caught pre-write; the SIX named in addendum 177:
(1) `charm SHA256 prefix mismatch` is a stored constant with NO raiser (errors.go
:258); the prefix check raises `charm hash mismatch` (store.go:169) -- the old
page's lowercase error dropped, the zero-raiser stated per the law;
(2) `unable to resolve charm` (errors.go:215) also has NO raiser -- stated;
(3) `charm not resolved`'s raiser path is the wrong-CHARM-UUID download resolve
(service/application.go:1152-1155), the errors.go doc comment's story dropped;
(4) the `juju`/`juju-` reservation applies to relation names/interfaces
(metadata.go:521,:571) and action names (actions.go:120), NOT the charm's own name;
(5) the charm changes watcher has NO subscriber in the current code (WatchCharms,
service/charm.go:997, zero callers) -- the old consumer example dropped, stated;
(6) the URL's "no registry host" claim not derivable from the current grammar --
rephrased to the grammar's own statements; + the charm-revision h3's CLI spellings
dropped (client-agnostic). The 858-char restored reactive sentence survives
byte-equal (re-proven post-write).
Gate: style CLEAN first pass on the final form; purge build at the exact 3-warning
baseline (zero new); service stopped before build; verify-docs PASS serverless
(worker-exit check first); relaunched under juju-docs-serve-floor, curl 200 x3;
served 13/13 anchor ids + key sentences + TF href 200; raster proves x2 (light/dark
pairs, labels render, no duplicated prose); truncation census clean; dup
line+sentence scans clean; the-charm-record dissolved (zero inbound both forms);
35 anchors.
NEXT: at the reviewer's word the roll continues: subnet, resource-charm (its
the-charm-origins facade ref resolves), ssh-key. MANDATORY break after ~3 reviewer
interventions. The split-form FLAG (addendum 164) still parked. PENDING unchanged
(rounds (a)/(b), user-secret access-level, ADR-013 stamp, P0-1 pick, +BUBBLE-UP
SURFACES, the designations-split proposal, the S3-policy-JSON rehome, the 3.x
version-history corpus sweep; router-nondeterminism rider parked). Chain + gotchas:
HANDOFF Appendices A-C.

**SESSION 61 (2026-09-28, CLOSED): LEDGER READ (RATIFIED) + ROUND 5 (action.md, script.md's facade refs riding) — juju = origin = 172383d395 (one commit, pushed); ggarch b264386 unchanged.**
LEDGER READ: addendum 175's thirteen deviations ALL RATIFIED. The three load-bearing
laws re-verified directly at 12e74d9658 (same HEAD, clean tree): the zero-raiser law
(errors.go:116,120,124,140 — UnitHasSubordinates, UnitHasStorageAttachments, UnitIsAlive,
UnitAlreadyHasSubordinate; zero non-test raisers repo-wide), the presence-based display
override (status/service/status.go:254-264 lost-on-absent, :318-325 unknown-unless-
error/terminated), the CAAS/IAAS split (unit.go:871-884 CAAS registration presets
allocating/waiting; :905-910 not-assigned on the OrderedId>=scale-target / not-scaling
trigger). Spot re-verifies: storage.go:2036 `unit is not alive`; interface.go:24,31
`leadership claim denied` / `leadership lease not held`. The remaining eight were
re-verified in session 60 against this same tree state.
ROUND 5 LANDED (172383d395, 183+/157-): action.md on the machine+controller pattern --
declaration as operation bullets (the actions.yaml definition riding the charm revision;
client-agnostic access levels) with the grounded name grammar
(deployment/charm/actions.go:20 `^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$`; reserved `juju` /
`juju-` prefix, meta.go:854-862); persistence as table-name-first record bullets over
0033-operation.sql (operation, operation_action, operation_task, the two receiver joins,
operation_parameter, operation_task_status + the 8-row vocabulary, operation_task_log,
operation_task_output) plus charm_action (0015-charm.sql:528); the action states h3
grounded on the writers (enqueue pending; StartTask pending-to-running via the atomic
row-count guard task.go:140-206; the validated completion set core/status/status.go
:349-357; cancel pending->cancelled / running->aborting task.go:448-513; the operation
completes when its last active task does, task.go:331-382; the query priority
service/query.go:20-37 running>aborting>pending>error>failed>cancelled>completed);
execution split by owner (enqueue existence-not-life checks with per-task failure and no
rollback; FinishTask status+output to the object store under the task UUID; the
cancellation asymmetry: the unit agent polls aborting and reports aborted, the machine
runner has NO abort surface and restart-finishes stale actions failed "action cancelled";
the three watch surfaces: unit pending-or-aborting, machine pending-only, task logs);
per-layer rules-and-errors h3s replacing the banned page-level h2 (the machine-lock
semantics grounded: parallel-no-group concurrent under the 100-slot limiter, others in
exec-command / exec-command-<group>, machineactions/worker.go:208-232,:70); client-agnostic.
NAMED CORRECTIONS caught pre-write: (1) the `error` task status has NO writer in the
current code (accepted completion status, terminal for cancel, no producer) -- the old
page's "failed before it could run" dropped; (2) machine task notifications fire on
PENDING ONLY (state/state.go:389-404), the old "the same" dropped; (3) the JUJU_ACTION_*
env vars STAY on the page (hook.md's "Hook and action environment variables" delegates
here; grounded context.go:1461-1462); (4) the wait/background CLI behaviour dropped to
the command pages; (5) five zero-inbound anchors dissolved (the-actions-records,
the-action-record, the-actions-machinery, the-action-execution, types-of-action), 14 -> 10;
script.md's facade refs (the-action-in-the-data-model, the-action-states,
the-action-operations, the-action-cancellation, the-action-watchers,
the-action-rules-and-errors) all resolve.
Gate: style CLEAN first pass; full purge build at the 3-warning structural baseline
(zero new) + one incremental rebuild folding a late ibnote; verify-docs PASS
serverless+idle (worker-exit check first); served 10/10 anchor ids + key sentences +
error strings + TF href 200 + curl 200 x3; raster proves x3 (3 blocks x light/dark
pair, labels render, no duplicated prose); truncation census clean; dup line+sentence
scans clean; both block identity re-proven byte-identical from 12e74d9658.
NEXT: at the reviewer's word the roll continues: charm, subnet, resource-charm, ssh-key.
MANDATORY break after ~3 reviewer interventions. The split-form FLAG (addendum 164)
still parked. PENDING unchanged (rounds (a)/(b), user-secret access-level, ADR-013
stamp, P0-1 pick, +BUBBLE-UP SURFACES, the designations-split proposal, the
S3-policy-JSON rehome, the 3.x version-history corpus sweep; router-nondeterminism
rider parked). Chain + gotchas: HANDOFF Appendices A-C.

**SESSION 60 (2026-09-28, CLOSED): THE LEDGER READ (RATIFIED) + ROUND 4 (unit.md) — juju = origin = 12e74d9658 (one commit, pushed); ggarch b264386 unchanged.**
LEDGER READ: addendum 174's twelve + the two truncation artifacts + the micro-round close
ALL RATIFIED, re-verified against repo ground (errors.go:46,50,79,86,271;
removal/service/application.go:285-303; service/application.go:1385ff,:1756;
state/application.go:3495-3509,:3721-3742,:1782-1868; fixed_limits.go:21; trust.go:7;
facades/client/application/application.go:1755,1768,1809; exposed.go:133-146;
endpoint.go:7; status.go:540-548; uniter/status.go:132; resolver.go:374-380;
uniter.go:2688; config-get.go:78-84; 0019-application.sql:68). Both artifacts confirmed
restored (charm.md:327 858 chars; application.md slide-captions 791 chars); corpus
ellipsis census (>=700 + U+2026) ZERO.
ROUND 4 LANDED (12e74d9658, 84+/191-): unit.md on the machine+controller pattern --
declaration operation bullets + the grounded name grammar; persistence table-name-first
bullets over 0020-unit.sql; the writer gates (lost/allocating refused, error needs
message) + presence-based display overrides; Leader/Subordinate kinds h3s (the controller-
DB lease; the three grounded gates); execution split by owner with hooks/hook-commands as
the runtime surface (the grounded hook sequence; retry-hooks/no-hooks honoured once);
per-layer rules-and-errors h3s replacing the banned page-level rules h2; client-agnostic.
THIRTEEN grounding corrections caught pre-write (all named in addendum 175): `unit is not
alive` (the raiser's string, storage.go:2036); FOUR zero-raiser constants left out (unit
is alive, unit has subordinates, unit has storage attachments, unit already has
subordinate); the initial statuses narrowed to the CAAS registration path
(unit.go:871-884); the display override re-grounded as presence-based
(status/service/status.go:254-264,:318-325); the writer gates (status/service/
service.go:431-446); leadership grounded (controller lease 0002-lease.sql; gates
leaderservice.go:94-107, relation.go:299-307, secret service.go:785-787) + the leadership
error strings corrected (core/leadership/interface.go:24,31); `unit not assigned` grounded
on the CAAS registration trigger (unit.go:905-910); the unit dead gate + force semantics
(removal/state/model/unit.go:556-634; removal/service/unit.go:100-342); the name grammar +
leader alias (core/unit/name.go; run-target); the add path (unitstate.go:297-330);
resolution (resolve/state/state.go:140-160; uniter/resolver.go:262-293; commithook.go:41);
the hook sequence + the last-unit-on-machine cascade (hooks/hooks.go; resolver.go:335-380;
runhook.go:288-307; removal/service/unit.go:104,135-139); resolve/remove write access
(application.go:1823-1830). Watch surfaces re-verified (service.go:261-813).
Gate: style CLEAN first pass; purge build at the 3-warning structural baseline (zero new);
verify-docs PASS serverless+idle; served 9/9 anchor ids + key sentences + both raster
proves; curl 200 x2; both ggarch blocks byte-identical (spliced from git show, identity
re-proven). Anchor census: 14 -> 9 (every dissolved anchor zero-inbound in both forms).
NEXT: session 61 = the reviewer's ledger read at 12e74d9658; then at the reviewer's word
round 5 = action.md (script.md's facade refs riding), then charm, subnet, resource-charm,
ssh-key. MANDATORY break after ~3 reviewer interventions. The split-form FLAG (addendum
164) still parked -- retire or re-scope at the reviewer's word. PENDING unchanged (rounds
(a)/(b), user-secret access-level, ADR-013 stamp, P0-1 pick, +BUBBLE-UP SURFACES, the
designations-split proposal, the S3-policy-JSON rehome, the 3.x version-history corpus
sweep; router-nondeterminism rider parked). Chain + gotchas: HANDOFF Appendices A-C.

**SESSION 59 (2026-09-28, CLOSED): THE LEDGER RATIFIED + THE STORAGE-LABEL MICRO-ROUND + ROUND 3 (application.md carrying application-config) + THE TRUNCATION ARTIFACTS — juju = origin = f7c5655fd8 (two commits, both pushed); ggarch b264386 unchanged.**
LEDGER READ: addendum 173's eleven RATIFIED, all re-verified against repo ground (errors.go
:18,32,36; createsecret.go:21,110,31-32; client.go:152-154; cmd/juju/model/config.go:376-378;
0018-secret-backend.sql; runhook.go:85; 0050-secret.PATCH.sql). The three load-bearing laws
stand for the pages ahead.
MICRO-ROUND EXECUTED (16e7e3f5b3, 2+/0-): the restore option -- (storage-directive) stacked on
the declaration-layer h2, (storage-provider) on the storage providers h3; zero referrer edits;
bare-form census = exactly the 7 warnings, display-form 0; purge build 1 warning (the 7
storage-label warnings GONE); served both ids + all referrer hrefs PASS; CLOSED.
ROUND 3 LANDED (f7c5655fd8, 277+/158-): application.md on the machine+controller pattern --
per-layer rules-and-errors h3s (page-level rules h2 dissolved; 17/17 Triggered-when/
Remediation); the configuration h3 expanded to carry application-config per addendum 169 (the
charm schema instantiated; the write law; trust interception; the 16 MB cap
core/quota/fixed_limits.go:21; the SHA-256 config hash as the config-changed trigger; the
config-get read; YAML unsupported; synthetic refusal); hooks/hook-commands as the execution
runtime surface; table-name-first record bullets (14); client-agnostic. TWELVE grounding
corrections caught pre-write (addendum 174): four error strings to the raisers (application
is not alive :46; invalid application config :271; scaling state is inconsistent :79;
incompatible base for charm :86) + application is dead entered; the dead gate on the removal
service's counts (removal/service/application.go:293-303); the config-write law
(UpdateApplicationConfig); the 16 MB cap; the config-hash law (hashConfigAndSettings, sorted
keys+values+trust); the default fallback + nil-hiding read; the YAML/synthetic refusals; the
refresh transactional law (FilterApplicationConfig drops undefined keys); the scale law
(negative/inconsistent + the k8s-only DDL comment); the expose wildcard fallback; the status
leader gate + the severity order (statusSeverities 100..40); TWO unraised constants left out
(InvalidApplicationState, ApplicationNotSubordinate -- zero raisers repo-wide).
THE TRUNCATION ARTIFACTS (both latent, both byte-restored from pre-skeleton ground):
application.md's machine slide-captions cut at b3ad26c793 (old[:768]+U+2026; 791-char line
restored); charm.md:327's reactive sentence cut at e051d2a984 (858-char line restored); corpus
sweep proves only these two. Promoted to Appendix B (the 768-CHAR TRUNCATION ARTIFACT gotcha).
Gate: style CLEAN after two self-catches (prose em-dash pair; colon-outside-bold lead-ins);
two purge builds at the structural baseline (1 then 2 warnings, zero new); verify-docs PASS
serverless+idle; served 18/18 anchor ids + key sentences + the raster prove (the raster caught
a splice duplication the strip-tags check missed; fixed pre-commit); curl 200 x3. ggarch
blocks 1+2 byte-identical, block 3 = the named correction.
NEXT: session 60 = the reviewer's ledger read at f7c5655fd8; then round 4 = unit.md, then
action (script.md's facade refs riding), charm, subnet, resource-charm, ssh-key. The
split-form FLAG (addendum 164) still parked -- retire or re-scope at the reviewer's word.
PENDING unchanged (rounds (a)/(b), user-secret access-level, ADR-013 stamp, P0-1 pick,
+BUBBLE-UP SURFACES, the designations-split proposal, the S3-policy-JSON rehome, the 3.x
version-history corpus sweep; router-nondeterminism rider parked). Chain + gotchas: HANDOFF
Appendices A-C.

**SESSION 58 (2026-09-28, CLOSED): THE ENTITY-PAGES ROLL, ROUND 2 (secret.md) — juju = origin = 03ef9a6a4b (one commit, pushed); ggarch b264386 unchanged.**
LANDED (03ef9a6a4b, 301+/246-): secret.md on the machine+controller pattern — the integrated
one-object intro; per-layer rules-and-errors h3s (declaration/persistence/execution);
table-name-first record bullets; the state machine kept as the page's one state-machine view,
its writers named in prose; the watchers h3 as the execution runtime surface; client-agnostic.
ELEVEN grounding corrections caught pre-write (all named in addendum 173's ledger): three
error strings corrected to the raisers (domain/secret/errors/errors.go); the data-key regex
re-grounded (createsecret.go:21,110) with the 1 MB law; the user secret's "name" = the owner
label (no separate name validation exists; the (secret-name) anchor dropped); the
secret-backend model config key REMOVED (cmd/juju/model/config.go:377) — per-model operation;
backend records in the controller database (0018-secret-backend.sql; built-in
<model name>-local); peer-units claim narrowed to the owner application's units
(access.go:414-448); rotate/expire/remove leader-gated CONDITIONALLY (runhook.go:85,
app-owned only); user-secret grant path grounded (checkCanWrite; VIEW role, application
subject, model scope); secret_reference owner lazy (0050-secret.PATCH.sql); track/peek stated
once; backend-table typos fixed. Both ggarch blocks BYTE-IDENTICAL. 21 anchors censused BOTH
ref forms pre-write; 9 kept, rest dissolved all zero-inbound; h2 ladder anchors kept after a
self-catch (served anchor-id check caught the drop; restored + re-purged + rebuilt clean).
Two purge builds at the 10-warning baseline (3 structural + 7 PRE-EXISTING storage-label,
zero new); verify-docs PASS; served checks ALL PASS; curl 200.
THE STORAGE-LABEL MICRO-ROUND remains OFFERED (reviewer's call): restore
(storage-directive)/(storage-provider) as stacked anchors on the re-formed storage.md, or
re-point the referrers (manage-storage.md:39, manage-storage-pools.md:21, the reuse snippet
storage-provider.md:3 x5); 7 dormant warnings on purge builds.
NEXT: session 59 = the reviewer's ledger read at 03ef9a6a4b; then at the reviewer's word the
storage-label micro-round and round 3 = application.md carrying application-config (no
standalone config page — config-get/set -> application config per addendum 169), then the
target list's order (unit, action with script.md's facade refs riding, charm, subnet,
resource-charm, ssh-key). The split-form FLAG (addendum 164) still parked — retire or re-scope
at the reviewer's word. PENDING unchanged (rounds (a)/(b), user-secret access-level, ADR-013
stamp, P0-1 pick, +BUBBLE-UP SURFACES, the designations-split proposal, the S3-policy-JSON
rehome, the 3.x version-history corpus sweep; router-nondeterminism rider parked). Chain +
gotchas: HANDOFF Appendices A-C.

**SESSION 57 (2026-09-28, CLOSED): THE ENTITY-PAGES ROLL, ROUND 1 (relation.md) + THE TARGET LIST + THE UNNAMEABLES RETIRED — juju = origin = 5062a7c02e (one commit, pushed); ggarch b264386 unchanged.**
THE TARGET LIST (mechanically derived per the session-56 close directive, proposed in the FIRST
delivery ledger; the reviewer continued with secret.md — the list stands as proposed): 9
DDL-grounded targets in order — relation (DONE, 5062a7c02e), secret, application (carrying
application-config; no standalone config page exists — config-get/set → application config per
addendum 169), unit, action (script.md's facade refs ride), charm, subnet, resource-charm,
ssh-key. Markers: the `### <Layer> rules and errors` h3 census matches exactly the 11 re-formed
pages; every other entity page carries the banned page-level `## X rules and errors` h2 or the
records/machinery shape. EXCLUSIONS with mechanical reasons: script.md (facade over the action
machinery — its own text: no record/states/rules of its own), bundle.md (no DDL), access.md
(the associative-entity exemplar per ADR-013), zone.md ("a value, not an entity" — its own
text), agent.md + database.md (software pages), watcher.md + worker.md (runtime concepts),
hook.md + hook-command.md (cross-cutting execution surfaces per addendum 169), status.md
(concept; status records are satellites), resource-compute.md (16-line stub).
LANDED (5062a7c02e, 312+/307−): relation.md on the machine+controller pattern — per-layer
rules-and-errors h3s; table-name-first record bullets; the one-object intro; hooks+hook-commands
as the execution runtime surface; client-agnostic; NINE grounding corrections caught pre-write
(either-container scope law; firewaller NotImplemented; juju-info author-declared kept;
idempotence service-folded; precedence claim dropped; bases/CMR-to-CMR/quota rules added;
resume→joining; suspended-message retention; requirer-first keys); 8 ggarch blocks
byte-identical; 11 anchors kept / 9 dissolved (BOTH ref forms censused — the form-only census
missed subordinate-relation's two display-text referrers; the two-form census is now reshape
discipline); verify-docs PASS; served key-sentence checks x12 PASS. SURFACED (pre-existing,
micro-round offered, reviewer's call): 7 storage-label warnings — storage.md's session-55
re-form dropped (storage-directive)+(storage-provider); referrers manage-storage.md:39,
manage-storage-pools.md:21, reuse storage-provider.md:3 x5; dormant since session 55 (its
census missed the display-text ref form).
THE UNNAMEABLES RETIRED (supersedes the session-55 flag at the 55-block's UNNAMEABLE QUEUE
ITEMS and session-56's NEXT line): kubernetes-info + bindable-subnets-class are NOT REAL. The
reviewer: "I don't recognize them. Are they real?" Answer: NO — zero repo ground (no code, no
DDL, no docs token; diagrams.md today carries neither), and their only existence is the
archive's own sweep-plan lists (first at SESSIONS addendum 149, "the remaining entity pages
per the diagrams.md catalogue" — the catalogue itself does not contain them). RETIRED; nothing
owed; no pages to write.
NEXT: session 58 = secret.md (the reviewer's order: "Continue with secret.md"), then the target
list's order; the storage-label micro-round offered; the split-form FLAG (addendum 164) parked
(retire or re-scope at the reviewer's word). PENDING unchanged (rounds (a)/(b), user-secret
access-level, ADR-013 stamp, P0-1 pick, +BUBBLE-UP SURFACES, the designations-split proposal,
the S3-policy-JSON rehome, the 3.x version-history corpus sweep; router-nondeterminism rider
parked). Chain + gotchas: HANDOFF Appendices A-C.

**SESSION 56 (2026-09-28, CLOSED): THE AUDIENCE-TAG DROP + THE CONTROLLER INTRO — juju = origin = 5bdfd7b0f0 (4aa3b9d18d + 5bdfd7b0f0, both pushed); ggarch b264386 unchanged.**
RULING 1 (reviewer, binding — AMENDS the queue, does not replace it): AUDIENCE TAGS ARE DROPPED FROM THE
DOCS. The tags are guesswork and produce false groupings (a reader reads the bits they care about: a
controller admin reads bootstrap; a charm dev working outside the 12-factor paradigm reads everything
about charms, hooks included). The MACHINERY STAYS untouched (docs/scripts/audience.py, the conf.py
extension entry, css/audience.css); only the rendered tags go: strip EVERY {audience} directive block
from every SOURCE page. Session-start census 32 grep hits = 28 docs/reference/*.md + 3 docs/howto/*.md
(compile-and-run-juju-agents-on-different-architectures.md, writing-workers.md,
debug-a-dqlite-core-dump-issue.md; predate the rewrite, same machinery) + 1 _build/review artifact
(_build/review/credential-structure-prototype.md; docs/_build/** is NEVER touched). After the round the
source census is 0. Check each stripped header for orphaned blank lines and sections whose only content
was the tag. One build for the sweep; verify on the SERVED pages: "For:" count = 0 corpus-wide (the
chip is extension-rendered; grepping sources is not the check).
RULING 2 (reviewer, binding): controller.md INTRO, three fixes, exact replacement text in the ledger:
(a) PURGE the entity-only disclaimer sentence ("The worker tree, high availability as a running system,
and upgrades are the controller agent's story; this page carries the entity." — it contradicts the
integrated DPE page, which documents execution-layer operations and watchers right below); (b) FRAME
the software-to-entity transition causally in the intro: the software (the jujud process running
Dqlite and the API server) boots first, and through its bootstrap lifecycle materializes its state as
the singleton controller record and the controller application in the database. No new facts — the
facts are already on the page; reframe only. (c) Embrace the full dual nature fluidly: software AND
entity, one integrated object.
LANDED per the round order, both rulings EXECUTED (postmortem = SESSIONS addendum 171; the intro's
exact replacement text is in the session-56 delivery ledger): (1) 4aa3b9d18d the sweep — 71 {audience}
blocks stripped from the 31 source pages, pure deletion 180-/0+, no section's only content was the
tag, served "For:" count 0 corpus-wide, machinery untouched, verify-docs PASS; (2) 5bdfd7b0f0 the
intro — the entity-only disclaimer purged, the software-to-entity transition causal (boots first;
the bootstrap lifecycle materializes the singleton controller record + the controller application),
one integrated object; ONE adjacent named edit (the meta description's "as an entity" -> "as
software and entity"); gate CLEAN; served strip-tags checks x6 PASS. Appendix A 2.5's audience-chip
gate item is SUPERSEDED by ruling 1; the per-section-tags design call (Appendix C PENDING) is MOOT;
the split-form FLAG (addendum 164) loses its "tagged" half — reviewer to retire or re-scope.
NEXT: the reviewer's ledger read at 5bdfd7b0f0 + the two unnameable definitions (kubernetes-info,
bindable-subnets-class); THEN the queued entity rounds (relation -> secret -> application-config,
addendum 169 spine rule) and/or the split-form answer. PENDING unchanged (rounds (a)/(b),
user-secret access-level, ADR-013 stamp, P0-1 pick, +BUBBLE-UP SURFACES, the designations-split
proposal, the S3-policy-JSON rehome, the 3.x version-history corpus sweep; router-nondeterminism
rider parked). Chain + gotchas: HANDOFF Appendices A-C.
CLOSE DIRECTIVE (2026-09-28, terminal, session-56 close — reviewer verbatim): "break -- give me the
prompt. Let's focus on rolling the machine.md and controller.md pattern to all of the other 'entity'
reference docs." Session 57's round = THE ENTITY-PAGES ROLL: machine.md (the compression: table-name-first
bullets, no narrative filler, rules/errors in dedicated sub-lists) + controller.md (the DPE entity page:
declaration/persistence/execution h2s, per-layer rules h3s, the integrated one-object intro) are the pattern
references; derive the target list mechanically (the entity reference pages not yet on the pattern — cross-check
the sweep records so no re-formed page re-opens; the entity test per the records: a lifecycle in the DPE sense);
order per the spine rule (addendum 169; relation -> secret -> application-config was the queued head); each a
grounded DPE round; propose list + order in the FIRST delivery ledger for the reviewer's read.

**SESSION STATE (2026-09-27, session 55 CLOSED — THE SWEEP CLOSED: juju f2d0ecbe80 pushed; ggarch b264386 unchanged):**
(0) LANDED (1c41bfbe19, 154dc220f5, 7ee36d0281, f2d0ecbe80): the controller shape bullets IN
(declaration application clause + persistence application/origin/units bullets, all constants
verified pre-write); the user+ label is PLURAL ("Juju-and-charm users+", one map entry in
scripts/audience.py, corpus-wide — the reviewer's mid-round ruling); SEVEN light pages re-formed
on the locked template (offer, storage, constraint, placement-directive, user, cloud, credential)
with per-layer rules h3s grounded against the raisers; THE MODEL ROUND (the E refinement's home):
the model's execution layer names actors and loops, not locations (per-model workers, the
Undertaker, the migration master), rules h2 dissolved into per-layer rules h3s, layer chips per
the corpus map. verify-docs PASS every round; tree clean; server serving.
(1) GROUNDING CORRECTIONS (seven, all named in addendum 170): offer creation is idempotent
(identical = no-op success; differing = offer already exists); offer already consumed checks the
CONSUMING model's application_remote_offerer row; username not valid (not "user name not
valid"); user is the last model admin for 1 or more models; credential is not valid for one or
more models; model constraints not found; model credential not valid. Three ungrounded claims
DROPPED (storage charm-floors, rootfs fallback, the unraised singular model constraint not
found).
(2) UNNAMEABLE QUEUE ITEMS (FLAGGED for the reviewer): kubernetes-info and bindable-subnets-class
have NO ground truth anywhere (no page/anchor/code/DDL/ggarch node — names exist only in the
sweep-plan lists). Definitions (entity + locus) owed before any page can be written.
(3) SWEEP QUEUE: CLOSED. The light pages are done; the model round closed the sweep. NEXT in the
reviewer's order: the queued ENTITY ROUNDS under the spine rule (addendum 169) — relation,
secret, application-config, each a grounded DPE round (DDL + raisers; hooks/hook-commands as the
entity's execution-layer runtime surface, per addendum 169) — and/or the split-form answer (the
execution h2 untagged-vs-tagged FLAG stands from addendum 164).
(4) PENDING with the reviewer: rounds (a)/(b), user-secret access-level, ADR-013 stamp, P0-1
pick, +BUBBLE-UP SURFACES, the designations-split proposal, the S3-policy-JSON rehome, the 3.x
version-history corpus sweep; router-nondeterminism rider parked. Chain + gotchas: HANDOFF
Appendices A-C.

**QUEUED (session 39, reviewer-requested): the provider layer + the per-cloud pages connection.**
Facts grounded: `internal/provider/{ec2,gce,azure,openstack,vsphere,oci,maas,lxd,unmanaged,
kubernetes}` is the per-cloud adapter code (all/common/dummy are non-type packages); the Types
chapter's seeded list maps 1:1 onto the type packages; the 14 per-cloud pages under
docs/reference/cloud/list-of-supported-clouds/ (9 machine + 5 k8s products; the 5 k8s products
all share the `kubernetes` type package) ARE the provider packages' user-facing surface
(bootstrap resources, constraints, placement directives, config keys = provider behavior) — but
nothing states that mapping. The cloud.md side links OUT (persistence → per-type definition
shapes; Types h4s → machine/kubernetes lists) and the per-cloud pages link back only to the
generic `cloud` page. THREE connective fixes, one round: (1) cloud.md execution: 2-3 sentences
naming the provider layer as adapter code, one per cloud type, exercised per operation (NOT the
cloud's own machinery — the "no machinery of its own" facet claim stands), with the line that
each type's adapter is what the per-cloud reference pages document; (2) one sentence reconciling
the CLIENT-side definition (clouds.yaml/credentials.yaml, what the per-cloud pages document)
with the CONTROLLER-db record (what cloud.md persistence documents) — the seam is currently
unnamed and the two could be conflated; ground the add-cloud upload flow before writing;
(3) optionally state the 5-k8s-products→1-type mapping in the kubernetes-cloud h4. SEQUENCE
after machine.md (round 14) lands: the machine rider's provisioning story exercises the same
provider-mention pattern, so write it once, consistently.

**FLAGGED (session 38, not fixed): user-secret access-level mismatch.** secret.md's user-secret
h4 and the CLI help (cmd/juju/secrets/add.go:57 "only the model admin can manage it") say model
ADMIN, but the Secrets facade enforces model WRITE access for user-secret mutations
(apiserver/facades/client/secrets/secrets.go:237 CreateSecrets, :298 UpdateSecrets, :358
RemoveSecrets, :407 grant/revoke -- all checkCanWrite = permission.WriteAccess; no deeper admin
check found in the bodies). session 38's new declaration do-sentence therefore says model write
access, grounded in the facade; the pre-existing user-secret h4 claim was left untouched.
Reviewer call needed: fix the h4 (and possibly the CLI help text) or re-gate the facade.

## TRIAGE (session 25, 2026-09-26 — main context, proposed for reviewer ratification)

Grounded facts gathered this turn:
- "Types of X" heading forms: 21 singular ("Types of action…"),
  exactly 2 plural-noun deviations — agent.md:54 "Types of agents",
  cloud.md:61 "Types of clouds". Unify = two headings + refs.
- charm-dev tags on rules/constraint sections: 15 pages carry a
  charm-dev chip on the rules/validity section (action, cloud,
  constraint, credential, machine, placement-directive, relation,
  script, secret, bundle, charm, model, application, offer,
  resource-charm). Several tag validity rules charm-dev that are
  actually juju-side invariants (cloud name unique; credential key
  unique) — the reviewer's "often not correct" is grounded.
- Watchers in user-facing surfaces: debug-log.md and log.md mention
  watchers NOWHERE (grep zero). The honest user-facing hook today =
  charm-dev events (relation-changed etc. are watcher-driven), not
  debug-log. Watcher.md justification must lean on the charm-dev +
  juju-dev audiences plus the "<entity> watchers" section collision.

MERGES / SUPERSESSIONS (new comments resolve older items):
- Crow's foot / ERD edge grammar — FINAL VERDICT — SHIPPED (session 45, ggarch eef5cfb,
  0.26.14; see SESSIONS addendum 148). Original ruling preserved below (reviewer, session-44
  close discussion, terminal; SUPERSEDES the earlier arrows+labels call):
  the ERD slices adopt the ARCHITECT'S OWN IDIOM (evidenced by
  ~/git/excalidraw/excalidraw-cmr.svg — the Juju architect's hand-drawn
  CMR ERD: zero arrowheads, no verb labels, `1`/`m` at BOTH ends,
  dashed = optional/uncertain, domain-cluster colors, open questions as
  annotations). RULING: NO arrows, NO verbs on data edges; BOTH-END
  cardinality (1 / m at each end, hand-placed); dashed = nullable.
  FK direction moves to its honest homes: the DDL, the fk: field badge
  (the child half's count witness), and ONE walkthrough-prose sentence
  per association ("the subnet row holds the space pointer"). Legend
  sharpens accordingly. Engine round (draw-only + grammar surface):
  renderer.py:1056-1109 (_crowfoot_kind/_render_crowfoot) GONE; the
  :1437 suppression REMOVED WITHOUT restoring marker_end (data edges
  render bare); edge LABELS on data edges — the verb — move out of the
  rendered slice into the walkthrough prose (the grammar keeps the
  label string for search/JSON; the ERD renderer drops it or the views
  stop declaring verbs — reviewer verdict carries: NO verbs RENDERED);
  both-end cardinality = NEW grammar surface (end labels at each
  endpoint; session-47 reviewer feedback AMENDS the placement: ON the
  line at each end, not outside the box face — see
  build/review/feedback-erd-sweep-round2.md item 3); dashed style
  driven by null: on the fk field (an honest
  absence), not hand-declared. 18 test_renderer crowfoot tests retire;
  new tests: both-end cardinality renders, data edges draw no arrowhead
  and no verb label. SKILL.md "Data model views" section + SPEC.md:506
  + :2204 rewrite. Regression gate (rule 3): audit baseline before,
  per-view renders; glyph strokes vanish, no new crossings. SEQUENCING:
  FIRST (before the template pick and the 18-page sweep) so the sweep
  renders in the final notation — no global re-look.
- BOTH-ENDS CARDINALITY — ABSORBED into the final edge-grammar verdict
  above (session 44 close): the excalidraw idiom IS both-end
  cardinality; it ships WITH the crow's-foot round, not as a later
  iteration. Residual design freedom for the round: whether the `m`
  end may read `0..m` where the schema says nullable (the reviewer's
  `?` in excalidraw-cmr) — decide in-round with the walkthrough prose.
- Node cues: session-25 batch 2 + batch 3 brainstorm + round-24 V1 P2
  + round-29 verdict 2 ARE ONE DESIGN ROUND (CUE DESIGN). Inputs now
  on the table: phonologist feature decomposition (people / software
  {Juju | Juju-adjacent | external} — process-vs-software question
  open / deployment nodes / records); the REAL Juju logo from
  docs/.sphinx/_static/logos/ replaces the fake "J" badge; strong/weak
  logo split; future logos (AWS, K8s) contemplated not designed;
  preattentiveness bar = the excalidraw orange-border precedent
  (under-discriminating but instantly legible).
- Sequence alt/loop detail: merges with the ADR-010 build-up
  slideshow amendment (round 28 7.1-PS + the ratified kinds-differ
  test) and the hook.md pair→carousel item. Principle: basic version
  first; complexity rides a build-up slideshow when needed.
- Arrow-label coherence: extends V2 (the unlabelled-arrow lint landed,
  add. 86). Now: a coherence sweep (label reads as one statement
  across the ends) over the chosen diagram set, in the language
  round's bar.
- Dqlite HA upside-down triangle: NEW small item; declared
  arrangement beats synthesis (ADR-007 ladder); answer "can
  autolayout/manual produce it" = declared positions certainly, synthesis
  to be probed. Rides the diagram-set polish.

PRIORITIES (time/tokens finite; 4.1 PR = the epic vehicle):

P1 — cheap cleanups, PR follow-up commits (each small):
1-4. DONE (addendum 115, 4f389a8332 + 5c2f4cf32f): headings unified; constraint.md CLI-agnostic; 11 rules-section
   charm-dev chips removed with evidence (4 kept); watchers-overload verdict = not overloaded; agent-vs-entity =
   no edit; NewMachineAgentCommand PROVEN correct; 10 copyright years fixed. Baselines 62 For: lines, 16 warnings.
5-7. DONE (addendum 116, cd6cfd3d42 + d1401e84ba + 63e62c9b4a): entity-lifecycle + writing-workers second pass
   (annotations, speculation, dead refs, wrong symbol homes cleaned; walls of text STAGED for reviewer);
   principles.ggarch folded into juju.ggarch (regression gate identical, single gated file now);
   stale config pages folded into the generated key list (redirects repointed; drift corrected at Go source;
   verify-docs PASS). Structural staging for the reviewer is itemized in addendum 116.
8. DONE (session 30, 642572e269, PUSHED: origin = local = 642572e269): docs-rules file gained the ggarch toolchain subsection
   ("### The ggarch toolchain", AGENTS.documentation.rules.md ~394-404: repo pointer + SKILL.md + ADR-001-011 +
   diagrams.md catalogue rule + check-ggarch/ggarch-gate.yml verification + primitives-not-caption-prose rule;
   contributor-guide hook). File is Sphinx-excluded (conf.py agents/**) — no rendered surface, verify-docs n/a.
9. Diataxis defense + the primitives/entities/processes/tools
   framework + the AI-suitability verdict: written into the PR
   description + the architecture grounding paragraph + an update to
   build/review/ai-impact-of-entity-reference.md (the "richer now"
   question answered with the follow-up-7 record). Mostly writing;
   reviewer-conversed, not blocking.
   DONE (session 30): build/review/pr-description-draft-4.1.md written
   (Diataxis defense §2, primitives/entities/processes/tools framework
   §3 with the agent-vs-entity verdict, AI-suitability verdict §4,
   architecture grounding paragraph §5, pre-empts §6, baselines §7);
   ai-impact record gained the closing answer section (weaknesses ->
   follow-ups 6/7). No juju-repo commit (records + draft only).

P2 — after the PR ships or as tagged follow-ups (unchanged parks):
+DOC-GUARD (session 31, reviewer question "prevent doc staleness by
   watching the sources"; feasibility analyzed, NO action yet): tiered
   staleness guardrail for reference pages, per
   ~/git/misc/juju-reference.md's four-layer source model (doc.go =
   framing, service = rules, facade = operations, schema = shape).
   T1: schema-generated enumerations (rotation values etc.) — extend
   autogenerate-docs.py input classes; T2: symbol-keyed quote guard
   (go/doc extraction vs quoted doc.go blocks, replaces line-range
   markers); T3: symbol-existence lint for paraphrased service rules;
   bookkeeping = per-claim multi-source comments in the .md. Guardable
   classes differ per layer (quotes diff; schema generates; rules lint);
   conceptual framing stays review-caught. All inside verify-docs, no
   new infra. Short-term v0 candidate: source-marker comment + grep-diff
   script.
+333 tags (follow-up-6 rulings owed), per-section llms (f-up 7),
entity-lifecycle rehoming (DEAD — the page was dissolved this session,
adf43b77e8), writing-workers full rewrite, charm-
lifecycle story, ERD-C2 (abstraction-level trade-off page) + C3
(three Relation-attributes defects — C1 now closed by the new
direction), round-25 leftovers (legend schema-association symbol,
sequence BLOCK_PAD, charm-type fill V1 — badge rethink absorbed by
CUE DESIGN), port-set landing / census wiring / determinism flake,
round-33 flags 5/6/7/9, machine-star verdict, status.md slot-4,
script+action joint treatment, charm-maturity removal (on record,
add. 107 (b)), create-backup/download-backup 3.x sweep, caption
[Type] format round (7.1 reopened; the 129-caption sweep waits;
touches the chosen set's captions only if ratified before the PR),
build-up ADR-010 amendment (lands with the sequence simplification if
slideshows are used).

DEAD / absorbed (no action): ERD-C1 (closed above), controller
storage revert question (closed KEEP, add. 90), the five session-13
caption/label decisions still formally open — fold into the caption
round when it fires.

REVIEWER INPUTS NEEDED to unblock P0: (a) the architecture.md design;
(b) the diagram-set pick; (c) crow's-foot ratification — RESOLVED
(session 44 close, see the merges block: drop glyphs, keep labels,
before the sweep); (d) watcher.md ruling — RESOLVED session 31.
Remaining: (a) and (b) are the two big ones.
NEW (session-27 close, reviewer Q&A): (e) entity-lifecycle ruling —
dissolve into the per-entity pages (unit/application/model already
carry the removal sections; the page's own see-also links point there)
vs keep-with-era-note; if dissolve, it is a STRUCTURAL round, not
text; (f) the principles drafts' six topology demos: catalogue policy
— they are NOT entries in diagrams.md (the preamble delegates them to
"the principles drafts"); folding them into the catalogue rides the
P0-1 design (the drafts dissolve into architecture.md).
RESOLVED (session 31): the session-27 lettering vs the session-25
lettering differ; session 31 received and executed both text rulings —
watcher.md absorb (d here, (a) in the session-31 lettering) = YES ->
watcher.md created + boilerplate dedup (d4c31acf61, red-thread fix
c7b048f66e); entity-lifecycle dissolve (e here, (b) in session-31
lettering) = YES -> page deleted + redirects repointed (adf43b77e8).
Still owed to unblock the remaining agenda: the architecture.md design
(a above) and the diagram-set pick (b above) + riders (c)/(f).

SESSION-32 PROMPT CORRECTION (addendum 127): the prompt as issued to
the reviewer carries one stale range — "HANDOFF.md:129-180 — rules
1-11" is WRONG: :129+ is State (rules 1-11 are :1-128). The VALID
ranges, recomputed after the rule-9/11 sharpenings (HANDOFF = 665
lines): rules 1-11 = :1-128; State (incl. PRIORITY OVERRIDE) =
:139-175; rules 12-15 tail = :-70; SESSIONS addenda 121-127 =
:7957-8095; TODOS full = :1-147. Use THESE; any range read that
truncates or misses its anchor: ONE recompute from wc -l + anchor
grep, never a whole-file re-read.

## REVIEWER NOTES (session 32) — reference-doc comment batch, recorded verbatim (triage in parens)

1. CONTRIBUTING.md mentions documentation.ubuntu.com, but the docs are now at
   https://canonical.com/juju/docs/juju-cli/ (TEXT → landed 2b9fc85e54).
2. {ref} in captions doesn't work. It should. (TEXT/BUILD → C2 round)
3. "The controller, models, machines and units are what agents serve – one process per entity (see
   controller, model, machine, unit)." >> "x is/are what ... <verb>" grammar is very grating, screams AI.
   Rephrase actively, e.g., "Agents serve entities: ... There is one agent process per entity."
   (TEXT → C3 round; apply the pattern-kill across docs, not just this one sentence.)
4. Various entity reference docs, in the records bit, use multiple different types of ERDs (see charm.md).
   Why different types? What does each achieve? (CONNECTED TEXT/DIAGRAM → C4 analysis)
5. The Dqlite HA diagram seems to be in multiple docs. RULE: no diagram allowed in more than one doc. Two
   tightly-connected entities may have almost-identical versions but must emphasize the main entity in each
   case (preattentiveness goal). (DIAGRAM → recorded rider; act on the diagram round)
6. charm.md: why are Charm channels under operations? Maybe doesn't belong at all (charmcraft/charmhub
   territory). Any case to cover charm channels in Juju? (TEXT → C6 analysis)
7. controller.md top "For: Juju developers" tag is wrong — a controller is Juju + charm user material.
   Idea: per-section tags that bubble up (a page-level tag surfaces all child-section tags).
   (TEXT fix now C7; bubble-up design recorded as an idea)
8. "The rules a charm URL must satisfy:" — satisfy in order for what? Who needs this, why? (TEXT → C8)
9. action.md lede "Actions are defined by a charm to allow a user" never says what an action is. Ledes
   should always be defining statements. (TEXT → C9)
10. Node labels should support hyperlinked text. Mermaid allows this (ggarch should too). (DIAGRAM/ggarch
    feature → recorded rider)
11. "access to credentials is not a permission object of its own: ownership plus the cloud-level
    add-model/admin access is what governs their use." — rewrite accessibly: authn vs authz split, what the
    credential lets you do on the cloud depends on how it was created on the cloud; what it lets you do
    through Juju depends on the user's Juju access. Short sentences, plain language. (TEXT → C10)
12. Model-records paragraph: "<statement>, and ... is the ... defining fact" — empty "and" clause, screams
    AI. Story order: model entered to come into existence → comes into existence (workers, model db) →
    some info goes to its model db. Controller db first. (TEXT → C11)
13. cloud.md "See more: List of supported machine clouds" should end the Machine cloud section. (TEXT → C12)
14. Records-section coherence across entity reference docs: how do identity / <entity> in the data model /
    <entity> states / types of <entity> relate? credential.md walk-through: identity mentions cloud, user,
    name + tangentially model + states; data model shows cloud, user, model; states picks up identity's
    states; "types of credential" interprets type technically vs types-of-charm phenomenological; nested
    "Client vs. controller credential" is purely phenomenological, preserves old content, not fitted to the
    new framing. Confusing now; will read as confusing to everyone. PS why did we step away from
    declaration / persistence / execution of intent? Opportunity: per entity, link how-to guides (juju repo
    AND terraform-provider-juju) for declaration (client stuff), data model for persistence, machinery
    details for execution. HATES the word "machinery". (TEXT → C13, the big analysis round)
15. BTW: entity reference docs combine content for all audiences incl. Juju dev — innovative; cover anything
    that bubbles up from lower levels (e.g., doc.go inside some package). (No action — context.)

DIAGRAM RIDERS RECORDED FROM THIS BATCH (no standalone action; ride the diagram round):
- Dqlite HA one-doc rule (comment 5) — new rule: a diagram lives in exactly one doc; near-identical twins
  allowed for tightly-connected entities, each emphasizing its main entity.
- ggarch node-label hyperlinks (comment 10) — feature request; verify Mermaid's exact syntax first.
- ERD variety (comment 4) — analysis feeds the diagram round; multiple ERD styles across records sections
  need a rationale or unification.
- MODEL-REMOVAL CLIENT ACTOR (session 43, first-hand verified): `behaviour "Model removal"`
  (docs/juju.ggarch:1453) opens `user -> controller` — the client actor is missing;
  `behaviour "Model migration"` (:1536) routes `user -> client -> controller`, as do Bootstrap
  and Deploy. Fix when the diagram round fires: insert the client hop (call + return).
- FLOATING-EDGE ROUTING DEFECT (session 43, first-hand verified, ENGINE class):
  FIXED + PUSHED session 44 (ggarch 587a37d, 0.26.13). Root cause was NOT route-vs-position
  ordering: the field-qualified mid-y flatten in router._pinned_field_anchors averaged the
  two field rows and, for a positions-relocated box, the average landed off-box (the stub
  was the pinned anchor itself). Fix: flatten only when the averaged y lies on BOTH spans;
  else each endpoint keeps its own field row (honest L). Audit baseline diff clean; pytest
  409 passed; all six slices verified connected by rasterize-and-look (before/after PNGs in
  build/review/floatingedge-*).

## SESSION 32 WORKING NOTES (analysis answers; updated as rounds land)

C4 ANSWER (ERD variety across records sections): there is ONE ERD grammar everywhere (record nodes +
schema-association edges, ADR-011 §3), used at two scopes: (1) "X attributes" views — the entity's own
stored tables and their FKs (the "<entity> in the data model" figure: charm/unit/secret attributes);
(2) "X origins/chain" views — the same grammar spanning MULTIPLE entities' records to show cross-entity
pointers (charm origins, credential chain). Genuine "Topology" views are runtime arrangements (who runs
where, who relates to whom: relation shapes, machine designations, deployment topologies). DEFECT FOUND:
record-pointer views were captioned "Topology" (charm origins, credential chain) — the wrong kind label,
which is what made the records figures read as "multiple different types of ERD". FIXED this session
(caption relabel). Remaining polish rides the diagram round: machine.md:60's caption leads with the
records story but the figure is runtime — reorder the caption, not the kind.

C6 ANSWER (charm channels under operations): channels are a Charmhub concept; Juju's model-side touch is
exactly two things — deploy/refresh take a channel as input, and the tracked channel is recorded per
application (application origin). The track/risk/branch taxonomy + the Charmhub-admin guardrail regex were
store-side content that had drifted into the Juju reference page. Case FOR covering channels in Juju:
users invoke them through the Juju CLI, so a minimal definition + the two touchpoints stay. Slimmed
accordingly; taxonomy linked out to Charmhub/charmcraft docs; guardrail subsection deleted (labels
charm-channel-track / charm-channel-track-guardrail had no inbound refs).

STANDING WARNING ATTRIBUTED (session 32, pre-existing, not from these rounds): explanation/juju-architecture.md
is orphaned ("document isn't included in any toctree" — explanation/index.md's toctree lists
architecture.md but not juju-architecture.md, while the index "Juju at a glance" bullet still
{ref}`s juju-architecture). Surfaced by doctree staleness (incremental builds hid it since session 31's
clean-build count). Owner call needed (include in toctree vs retire the page) — rides the P0-1
architecture.md work.

For: line count: 62 -> 61 (controller.md: page chip juju-dev -> user; two redundant per-section user
chips dropped under the page chip convention; watchers section gained its juju-dev chip, which it was
missing).

C13 ANALYSIS (records-section coherence; PROPOSAL, needs ratification before any mass edit):

Why declaration/persistence/execution was stepped away (reviewer's PS): ADR-011 (round 25, session 11)
records it -- two workflow-shaped orders ("existence arc"; "life spine mirroring the how-tos") were TRIED
AND REJECTED; the reviewer's own framing settled it: "howto sections are methods; entity reference
sections are attributes" (Go composition; the ERD-attributes parallel). So the paradigm was not silently
dropped -- it lost an explicit ruling. It returns today as a cross-LINKING layer, not a section skeleton:
declaration = the client surface (per-entity See-also to the how-tos: juju CLI howtos exist via ibnote;
ADD terraform-provider-juju resource links where a TF resource exists); persistence = the data-model slot
(already exists); execution = the machinery umbrella (already exists). Do NOT re-open the section order.

The coherence defects (credential.md walk-through generalized):
1. Slot contracts are undocumented, so sections pre-empt each other: identity narrates cross-db facts
   (the model-db read-only copy -- belongs in the data model slot) and names state flags
   (revoked/invalid -- states slot elaborates them); the data-model figure has a different scope
   (cross-entity chain) than the identity enumeration; states re-pick identity's flags.
2. "Types of X" is dual-use ACROSS pages: for credential/cloud it is the STORED discriminator (auth-type
   enum; cloud type enum); for charm it is interpretive kinds (substrate/function/role, explicitly "not a
   partition"). Two different section meanings under one title.
3. Phenomenological leftovers nest under technical sections: "Client vs. controller credential" sits
   under Types of credential but is about WHERE the credential is known (client-side awareness vs
   controller-side record), not a stored type. Same pattern risk elsewhere.

PROPOSED FIX (per-entity pass after ratification):
a. Write the slot contracts into ADR-011 (one line each): identity = what a record of X is, its natural
   key, where it lives (NO forward references); data model = the stored tables + the FK slice (cross-db
   and cross-entity facts belong HERE); states = life/status with owners; types = the stored discriminator
   IF one exists (say so explicitly when the taxonomy is interpretive instead).
b. Move misfiled content per contract (credential.md: model-db copy -> data model; client-vs-controller
   credential -> framed as where-the-credential-is-known, under records or a note, not under types).
c. "Machinery" (the reviewer hates the word): the umbrella layer name comes from ADR-011 round-32;
   renaming is one TITLE law edit + a page sweep -- propose "The X's engine" / "How X runs" / keep?
   REVIEWER PICK NEEDED before the sweep (the word appears across all entity pages + workers/architecture).
d. Declaration layer: per-entity how-to links (juju CLI + terraform-provider-juju), riding the per-entity
   pass; NOT a new section.

## STRUCTURAL DOUBTS UNDER THE LENS (session 33, reviewer Q "does the lens cast doubt on the structure?"; ANALYSIS — no edits until verdicts)

Sources weighed: ADR-011 (adopted, 3 amendments), ADR-012 (proposed), ~/git/misc/juju-reference.md
(the four-layer source model: doc.go / service / facade / schema), the live pages (credential.md read in
full; reference/index.md). Goal axis: groundedness + preattentiveness.

**Net: the lens does NOT topple the adopted skeleton.** Every slot maps to a projection (identity ->
schema grammar + ERD "where it lives"; data model -> ERD; states -> state machine at the seam; types ->
schema grammar OR taxonomy; operations -> sequence; watchers -> change-stream machinery; rules -> schema
grammar + service authority). The two-umbrella cut (records = what it IS, machinery = what HAPPENS) is
the preattentive layer; the projections are the filing rule one level down — they compose, per ADR-012 §3.
Four findings, one structural:

- **D1 (STRUCTURAL, needs verdict — amends the adopted §8):** "Entities related to the X" is a residual
  bucket, not a projection. Evidence on credential.md: all three §8 bullets are FK-shaped facts ALREADY
  carried by the data-model figure/caption (cloud defines auth types; user owns; model uses one pair) —
  near-duplicate of the data-model slot. Round 33 rejected folding §8 into the INTRO; that is not this.
  Proposal: rehome each §8 bullet by projection (FK-shaped -> data model; service facts like removal
  ownership -> machinery/states), slim §8 to navigation/see-also. Preattentive gain: the records TOC
  stops promising a second cross-entity list.
- **D2 (slot declaration, no structure change):** "Types of X" is not ONE slot — credential/cloud tell
  the stored discriminator (schema grammar); charm tells interpretive kinds ("not a partition"). One
  invariant title over two projections. Resolution = the C13 contract line (page DECLARES which
  projection), not a rename; predictability law holds.
- **D3 (same pattern, states):** the states slot is a state machine where a life enum exists; a
  standing-flags prose where none does (credential: "two standing flags rather than a life cycle" —
  recorded phrasing already holds). The contract should name the degenerate case explicitly.
- **D4 (§5 conflation — fix within the pass):** operations prose mixes the SERVICE's mutations with the
  CLIENT's operations. Evidence: credential.md §5 opens "Adding a credential (`juju add-credential`)
  inserts the record" — a CLI command inside the service story, and no location-qualified scope-phrase.
  The four-layer model assigns the operation surface to the FACADE layer; the lens assigns the client
  surface to DECLARATION (links) and execution to machinery. Fix: §5 stays service-side
  ("In the controller, the credential service…"); juju CLI + terraform-provider-juju pointers ride the
  declaration links (the top ibnote), per C13 — not a new section.
- **D5 (verification protocol for the pass — addition, not structure):** the four-layer model supplies
  the pass's CHECK side where ADR-012 supplies the FILING side: doc.go -> framing/intro; service ->
  rules + transition owners; facade -> exposed-surface check on §5 (is the op client-visible, and if
  not, who performs it?); schema -> data-model completeness + enum values (the secret.md simulation
  found rotation values/auto_prune/pending_delete missing — the method works).
- **D6 (no doubt, confirmed):** topology stays deliberately homeless (beats where the argument needs
  concreteness) — right under the do-not-force law.
- **D7 (genuine platform gaps the lens exposes; rides P0-1, reviewer's call):** the access-control model
  has no page although credential.md already smuggles access-grant facts (the ERD caption carries the
  permission-table fact AND the rules section repeats it — cross-slot duplication is the symptom of a
  missing home); annotation/port/ipaddress/operation gaps per the misc note's table.
- **D8 (no doubt, confirmed):** the TOC story (records/machinery) leaves states narrated as
  record-condition while the lens names it the schema-SERVICE seam — the recorded phrasing ("life is the
  record's condition") resolves it; do not relitigate. Machinery-word rename still awaits the pick.

VERDICTS NEEDED: (D1) slim §8 to navigation + rehome its substance — yes/no; (D2/D3) ratify the contract
lines as amended (types declares its projection; states names the degenerate case); (D4/D5) fold into
the per-entity pass protocol; (D7) whether the access gap gets a page in this PR or rides P0-1.

## REVIEWER REACTIONS (session 33, one-by-one round on the structural-doubts analysis) — verbatim >> notes + triage

1. On "the two-umbrella cut is the preattentive layer": ">> The thing is that the two umbrella cut is in
   fact NOT particularly preattentive. In fact, the way content repeats looks like crossed wires looks
   like bad abstraction or bad signposting. If I'm confused, the users won't even try."
   -> TRIAGE: the repetition is the evidence against the cut as-presented. Response owed: umbrellas
   = the persistence/execution stages of the intent pipeline; they survive only if the filing rule
   (one claim, one stage) is airtight. Verdict pending: keep+enforce vs drop.
2. On D1: ">> I've always thought we should try to fold this into the doc lede, before we dive into any
   sections." -> VERDICT-SHAPED: fold §8 into the lede. Round 33's objection (bullets carry substantive
   cross-facts) is met by rehoming the facts (FK-shaped -> data model; service facts -> machinery), not
   by keeping §8. Lede = definition + the entity's position + declaration links.
3. On D2/D3: ">> I don't understand what you are saying." -> REWRITE PLAINLY (done in reply): Types = a
   stored column's values (credential) vs judgment grouping with no column (charm); states = life cycle
   with owners vs standing flags with no life (credential).
4. On D4: ">> Are you saying the four-layer model of grounding is wrong?" -> NO — the four-layer model
   is the source side and is what EXPOSES the blur: §5 merges facade (client ops) into the service story.
5. On D5: ">> I understand what you're suggesting." -> no action.
6. On D7: ">> So what are you suggesting?" -> CONCRETE: one home for the grant fact (data model; it is a
   schema fact — the grant table); the access-control model (access domain) is a missing page — access.md
   proposal, this PR vs P0-1 = reviewer's call.
7. Overall: ">> I can't give verdicts when I don't understand what you're proposing." -> the previous
   reply was too dense; clarity is this round's deliverable.
8. PS: scaffold the five projections; the real question is how the four-layer model, the five
   projections, and declaration/persistence/execution connect logically — "I feel if we figure that out
   that will unlock the preattentive presentation too."

### THE UNIFICATION (session 33 answer to PS 8; the three frameworks are three views of one pipeline)

An intent enters Juju and becomes reality in three steps; each step has exactly one source layer, and
each stop answers its reader-questions:

| Intent step | What happens | Source layer (four-layer model) | Reader questions (projections) |
|---|---|---|---|
| DECLARATION | a client states what it wants | facade | what can clients do? -> answered by LINKS to how-tos, never a reference section |
| PERSISTENCE | the service validates; the schema stores it | service + schema | what is stored? (ERD) what may change, who may change it? (state machine) what kinds? (taxonomy) |
| EXECUTION | workers act on the stored facts | service + runtime | what runs where? (topology) how does a change happen? (sequence) |

doc.go is the shared VOCABULARY all three steps speak (the intro/lede). So: the four-layer model = WHERE
truth lives (sources); the five projections = WHAT the reader can ask (questions); D/P/E = the ORDER an
intent visits the layers — the bridge assigning each question to its source. Corollary (the anti-crossed-
wires rule): ONE claim, ONE stage, ONE section — a repeated claim is a claim whose stage was never
decided. The repetition the reviewer flagged is the visible symptom of undecided stages, not of a wrong
source model. SCAFFOLD proposal: teach the pipeline ONCE, centrally (a short "how an entity page is
organized" block — reference/index.md or the architecture page); pages keep nominal titles; the scaffold
does the preattentive work once instead of per-page.

VERDICTS NOW PENDING: (i) umbrellas keep+enforce-filing-rule vs drop (reaction 1); (ii) confirm the D1
lede fold (reaction 2 instinct); (iii) access.md new page this PR vs P0-1 (reaction 6); (iv) scaffold
location: reference/index vs architecture page (PS). Plus still owed: C13 ratification, ADR-012 verdict,
machinery word pick, per-section tags.

## THE TENSION MAP (session 33; reviewer: "the right answer should fall out once we've examined all the tensions")

**A. Skeleton tensions**

A1. Invariance vs projection-purity. The naming law fixes the SAME slots on every page; ADR-012 says
    every section is the prose of ONE projection. But the projection a slot serves SHIFTS per page:
    types = stored enum (credential) vs interpretive taxonomy (charm); states = life machine (most
    entities) vs standing flags (credential); machinery sentence = OWN/DELEGATED/NONE. A fixed skeleton
    cannot be projection-pure — it can only be projection-DECLARED. Tension between ADR-011 invariance
    and ADR-012 purity; fall-out: declaration-in-slot, not rename.
A2. The TOC tells a two-stage story (records/machinery) but the pipeline has three stages. Declaration —
    the first stage, the one every user performs first — has no home in the TOC; it is currently a stray
    ibnote. The page's own narrative is missing its first step.
A3. The lede's law vs the lede's instinct. Round 33 ruled the intro stays a definition (folding §8 in
    was REJECTED); the reviewer now says "I've always thought we should try to fold this into the doc
    lede." A standing adopted ruling points one way, the reviewer's instinct the other — the tension is
    on the record, not buried. Note the round-33 REJECTION was of folding the bullets verbatim; the
    instinct can be honored by rehoming facts and letting the lede carry POSITION (one sentence), not FK
    detail.
A4. §8 is both navigation and records. Random access (round 33's own argument) wants a cross-entity
    list; the anti-repetition rule says the data-model slot owns cross-entity facts. A bucket cannot be
    both.

**B. Claim-filing tensions**

B1. Repetition vs random access. Anti-crossed-wires says every claim once; random access says a reader
    entering mid-page missed earlier claims. PRECEDENT ALREADY SETTLES THE MECHANISM: session 31's
    watcher dedup (d4c31acf61) replaced 14 verbatim boilerplate paragraphs with ONE link — the repo
    already chose links-over-repetition. Fall-out: claims state once at their stage; cross-links serve
    random access; §8's facts rehome rather than repeat.
B2. Dual-use slots (types, states). "Types of X" is a stored column's values on one page and a judgment
    grouping with no column on another; "X states" is a life cycle with owners on most pages, two flags
    with no life on credential. One invariant title over two claim kinds. Fall-out: the contract names
    the two cases; each page says which it is doing.
B3. Seam claims have no single carrier. The bubble-up principle wants every claim generated from ONE
    lower carrier; but the state machine is BY DEFINITION the schema/service seam (states from DDL,
    transitions from service rules), and access grants span facade+service+schema. Some claims are
    inherently cross-layer synthesis — pretending they have one carrier is false grounding. Fall-out:
    the contracts mark seam claims as synthesis, honestly.
B4. Cross-cutting concerns have no slot at all. Juju's access-control model (the access domain:
    add-model/admin/register) appears on no page as itself — so its facts LEAK into every entity page
    that touches them (credential.md carries the grant fact in two places). The skeleton slots are all
    per-entity; there is no home for a cross-entity concern. PRECEDENT: removing-things/upgrading-things
    are cross-cutting pages ALREADY outside the entity skeleton. Fall-out: access facts get one home;
    whether that home is a new page (access.md, the removing-things pattern) is the open call.

**C. Presentation tensions**

C1. Client-agnostic law vs the declaration layer. ADR-011: reference is client-agnostic, CLI mentions
    are examples only; the declaration layer wants per-entity client-surface links. Links, not prose,
    keep the law intact — the ibnote is the existing sanctioned carrier; declaration rides it.
C2. Groundedness vs preattentiveness. The four-layer note says schema/service are "too
    implementation-detailed to expose directly" — yet their facts are what the page must carry. The
    existing resolution is the location-qualified scope-phrase ("In the controller database, a
    credential is…"): the CARRIER is named in user vocabulary. Tension resolved in principle; the pass
    enforces it (credential.md §5 currently lacks its scope-phrase).
C3. Nominal titles vs question scaffold. The naming law: noun titles only. Preattentive scaffolding
    wants the reader to navigate by questions (what is stored? what happens?). Question-form titles
    break the law. Fall-out: the scaffold lives ONCE, centrally (index or architecture page), teaching
    the pipeline that the titles already embody; the page order itself is the per-page scaffold.
C4. One truth, N surfaces (PARKED, +BUBBLE-UP SURFACES): CLI help vs docs vs generated config lists.
    Not reopened; noted for completeness.
C5. Per-section audience tags (comment 7): fine-grained routing vs chip chrome. PARKED on reviewer's
    design call.

**WHAT FALLS OUT (the answer the tensions point to, pending verdicts):**

The page IS the pipeline, and always quietly was. The adopted order — lede → records → machinery →
rules — is declare → persist → execute → law. Nothing was rejected in ADR-011 that needs resurrecting:
what was rejected (twice) was workflow-shaped SECTION ORDERS ("existence arc", "life spine"); the
adopted skeleton already realizes the pipeline as STRUCTURE. The three frameworks compose: four layers
= sources; five projections = questions; D/P/E = the route an intent takes THROUGH those sources, and
the page narrates that route top to bottom. The defects were never the skeleton — they were UNDECIDED
STAGES (a claim filed at no stage repeats itself into a second section: §8, the grant fact, the CLI
inside §5). Filing rule: ONE claim, ONE stage, ONE section; cross-links (not repetition) serve random
access, per the watcher-dedup precedent. What remains open is TASTE, not structure: (1) umbrellas stay
as the pipeline stage names (with the machinery word awaiting the pick) or drop to flat slots;
(iii) access.md now vs P0-1; (iv) scaffold location (index vs architecture page — or contributor-facing
only).

## REVIEWER REACTIONS round 2 (session 33; on the tension map / what-falls-out) — verbatim + triage

1. "I've always tried to avoid false groupings. Is there any sense in which the umbrellas are forced
   groupings? (I feel they might be, a little bit, but not sure.)" -> ANSWERED below: the umbrellas are
   honest as STAGES (persistence/execution) but forced as MEMBERSHIP — two members strain under the
   name (states: its transitions are execution, its condition is persistence — ADR-012 itself calls the
   state machine the SEAM; types: on charm it is interpretation, not a record fact). Forced exactly
   where the two-bucket compression meets the five-question model.
2. "The case for folding into the lede is that you get the tl;dr really fast. Knowing the neighbors is
   triangulation, and triangulation helps understanding." -> VERDICT (2): §8 folds into the lede.
   Round 33's letter is superseded; its spirit (don't lose the substantive cross-facts) is met by
   rehoming them (FK-shaped -> data model; service facts -> machinery/states). Round 33's random-access
   objection is met by cross-links (watcher-dedup precedent), not repetition.
3. "What;s access.md??" -> the missing reference page for Juju's access-control model (the `access`
   domain: who can do what on which object — access levels add-model/admin/register on
   clouds/models/controllers). misc note lists it as a genuine gap. Its facts currently leak into
   credential.md (twice), cloud.md, model.md. Question back: build it in this PR or ride P0-1?
4. The four open asks restated: (i) umbrellas keep/drop; (ii) lede fold — now effectively confirmed by
   (2); (iii) access.md timing; (iv) scaffold location (reference index vs architecture page vs
   contributor-only). Machinery word pick still owed.

## REVIEWER REACTIONS round 3 (session 33) — verbatim (trimmed) + verdicts + the prototype

1. Umbrellas: "I think I'd be less bothered if they matched 'persistence' and 'execution' better. Sure,
   you can retrieve that from 'records' and 'machinery' but you might also miss it."
   PS: "I'd also be less bothered if, like you say, the declaration was a section with a See link rather
   than just the See link. That would also be an opportunity to link to the relevant how-tos in both
   client docs -- juju (repo-internal) and terraform-provider-juju (see conf.py for the intersphinx
   prefix and build-a-charm for an example intersphinx link there -- the anchors in that repo will have
   the same shapes as in juju, manage-clouds, manage-x, ...). WDYT? ... I might not get it till I've
   seen a prototype with your comments."
   -> VERDICTS: (a) umbrella titles must CARRY the stage meaning; candidates: "The X's persistence" /
   "The X's execution" (nominal, entity-possessive, no code vocabulary — naming law holds; kills the
   machinery pick in the same stroke). Pending final confirmation on the prototype.
   (b) DECLARATION BECOMES A SECTION ("The X's declaration") carrying the See links. This SUPERSEDES
   C13's "NOT a new section" line and amends ADR-011's client-agnostic presentation (links only, no CLI
   narration — the lxd.md See-also pattern is the sanctioned carrier). Reviewer steer, precedence rule
   15c. GROUND VERIFIED: docs/conf.py:449 intersphinx 'tfjuju' ->
   documentation.ubuntu.com/terraform-provider-juju/latest/; the pattern is ALREADY USED in
   reference/cloud/list-of-supported-clouds/lxd.md ("Terraform Provider for Juju | Manage credentials
   <tfjuju:manage-credentials>"); TF howto anchors confirmed same shape
   (docs-rtd/howto/manage-users.md:7 (manage-users)=, :27 (manage-user-access)=). NOTE: the TF howtos
   live in docs-rtd/ in the local clone, not howto/ — the reviewer's path was close but the dir
   differs; the DEPLOYED anchor names are what intersphinx resolves.
2. access.md: "it makes sense. Right now we have user.md which has a section about access. That's fine
   in the sense that access is ultimately always about users, but there are tensions between how we
   handle this in the terraform docs (see .../manage-users.md) and the jaas docs
   (see .../manage-permissions.md). BTW what's access in our reference = dictionary of primitive
   concepts, entities, processes, and tools framework? I feel our framework is missing a generalization.
   (Originally I defined an entity as anything that has a lifecycle story... Now not sure anymore.)"
   -> EVIDENCE GATHERED: juju user.md:64 (user-access-levels) = the current home (access levels as a
   USER attribute); TF docs-rtd/howto/manage-users.md:27 "Manage user access" = a See-more list to
   per-object access howtos (manage-access-to-a-controller/cloud/model/offer/role/group); the TF
   provider models access as RESOURCES (resources/access_model.md, access_offer.md, access_secret.md,
   jaas_access_cloud.md...); JIMM docs/howto/manage-permissions.md models it as PERMISSION TRIPLES
   (subject tag x permission x object tag) with a hierarchy note (controller admin entails cloud admin
   entails can_addmodel). Three vocabularies, ONE underlying record.
   -> THE GENERALIZATION (answer to "what is access in our framework"): access is an ENTITY by the
   original definition (it has a lifecycle story: granted -> revoked) — but of a class the framework
   does not yet name: the ASSOCIATIVE ENTITY. A record that exists to CONNECT a principal to an object
   with a role; its natural key is composed of its endpoints' identities (user x object x level —
   exactly like credential: cloud x user x name); its lifecycle is a create/destroy arc (grant/revoke),
   no rich state machine; its machinery is DELEGATED to the connected entities' machinery (the check
   happens when the object is used). Juju's associative entities: access grants, relation, offer
   (secret grants too). This explains the three-docset tension: each client docset projects the same
   association record through its own surface (TF = per-object resources; JIMM = permission triples;
   juju docs = user attributes). The reference page states the record + the triple + the hierarchy ONCE;
   every client howto links to it. access.md timing: NOW (this PR) — it is small and unblocks the
   credential/cloud/user/model rounds; reviewer confirm.
3. Scaffold: "If you need a doc to explain the structure then you've got a bad structure... It's
   precisely the point of preattentiveness... clustering nodes of the same type etc. can help... if
   you're AI too, in the sense that clustering is a form of pre-processing... I never said anything
   about 'Juju howtos are entity lifecycle stories'... but that should be visible at a glance. I've
   done user research where I asked people to predict where they're going to find something and they
   were very good very fast, suggesting the basic pattern was in fact preattentive."
   -> VERDICT: NO explainer doc (ask (iv) answered: nowhere). The STRUCTURE is the scaffold; clustering
   (the umbrellas) + a self-evident order do the preattentive work. With the declaration section added,
   the TOC reads declaration -> persistence -> execution: the pipeline is the page, visible at a glance,
   nothing to explain.

### THE PROTOTYPE (session 33; the reviewer's requested "prototype with your comments")

Location: /home/dora/git/juju/docs/_build/review/credential-structure-prototype.md (the established
review-artifact home; NOT a docs source — Sphinx-excluded by being outside the source tree? NOTE:
_build is purged territory — copy to build/review if lost; it is scratch, never committed).
The prototype restructures credential.md per the round-3 verdicts with <!-- COMMENT --> blocks naming,
for every section: the intent stage, the source layer, the projection, and what moved from the current
page. It also demonstrates: the lede triangulation (§8 fold), the declaration section with the lxd.md
link pattern, identity with no forward references, the grant fact's single home (data model), the
degenerate states case, service-side operations with the scope-phrase, and the dropped §8.
OPEN IN THE PROTOTYPE: umbrella titles (persistence/execution proposed), anchor strategy (keep old
anchors vs rename + doctree purge — full-sweep decision at verdict), ADR-011 amendment text needed
(declaration section + title law) once confirmed.

## SESSION 33 SYNC (post-round-2): verdicts 1-2 received ("ok" x2) — structure RATIFIED. Rounds landed:
Round 1 (ggarch, PUSHED 212c351/2d07a83/8b3e264): ADR-011 session-33 amendment (declaration section,
persistence/execution titles — machinery RETIRED, §8 dissolution, filing rule, slot contracts,
service-side ops); ADR-012 -> ADOPTED + unification table; ADR-013 the associative entity (PROPOSED).
Round 2 (juju, PUSHED 994f873bce): credential.md restructured per the prototype; build clean (2 known
redirect artifacts only); rendered surface verified; verify-docs PASS; tree clean; staging = origin =
994f873bce. NEXT: round 3 = access.md (ground in domain/access first; register in reference/index.md;
also points user.md's access-levels section at it). Break line: mandatory after round 3.

## REVIEWER FEEDBACK on the landed credential.md (session 33, attachment with >> inline) — verbatim triage

1. {important} cloud-scoping block: ">> This should become unnecessary if the lede is clear."
   -> PAGE EDIT: delete the block; the lede already scopes to the cloud.
2. Declaration title article: ">> Why do we say 'The'? Why not 'A'? We're talking generically, right?
   'The' also strongly suggests uniqueness or salience, and neither applies here."
   -> NAMING ROUND (pending pick; sweeps every page): proposal = generic forms. Candidates below.
3. Declaration links: ">> Use ibnote -- this is an information backgrounding note. We want the links
   there but unintrusive." -> PAGE EDIT: See-also wrapped in {ibnote}.
4. Identity opener: ">> We should start by saying that a credential has a record in Juju's databases.
   Specifically, in the controller database etc. (though I think it's also in the model db for a
   model using it, or...?)" -> PAGE EDIT: opener rewritten: record-existence claim first, then the
   controller location; the model-db copy stays in the data-model slot (the chunking answer explains).
5. ">> What's the difference between the credential's identity and the credential in the data model?
   Isn't this related to the data model? How does it relate to the five projections? I really don't
   understand this at all." + ">> Exactly what I was saying. You have identity mention the controller
   db. Now this. It's confusing chunking. How does each of these sections under Persistence relate to
   the 5 projections?" -> THE CHUNKING ANSWER (in reply + contract): under persistence, the four h3s
   are four projections of the record: identity = schema GRAMMAR (what CAN exist: the key shape +
   required attributes — what you POINT AT); data model = ERD (what IS stored: tables, FKs, copies —
   what SURROUNDS the record); states = the SEAM (what may change, who may change it); types =
   TAXONOMY (declared: stored discriminator vs interpretive). The confusion was prose-level: identity
   narrated locations/copies (data-model business). Fix: identity carries record+key+uniqueness only;
   the data-model slot owns the footprint.
6. ">> So the data model covers the client too? I always associated it with the Dqlite schemas... now
   I wonder if the data model is bigger and might encompass the client too? The client isn't really
   persistence in the bigger Juju sense though. Info stored on the client is local. How do we sort
   this out?" -> DECISION: the data-model slot = Juju's databases ONLY (the schema layer's stored
   vocabulary — the four-layer model's schema row). Client-side knowledge is NOT persistence; it
   belongs to the DECLARATION stage (the client holds what it declares; bootstrap uploads). The
   client-vs-controller paragraph MOVES to the declaration section. The four-layer model sorts it:
   the client is not one of the four layers; its local store is the client's business, surfaced at
   declaration.
7. ">> Sounds wrong. Reminds of death sentences lol. If we stick to declaration, persistence,
   execution (which I kinda want to, though open to equivalent rephrases, e.g., declaration = things
   you can do, persistence = what Juju stores, execution = what happens in the background), we must
   however make them work well at the phrase level." -> NAMING ROUND: keep D/P/E as the backbone;
   phrase-level candidates below (execution is the problem child).
8. ">> This title strongly evokes the declaration of intent. People associate operations with 'I'm
   doing something' whereas this is trying to be about 'what's happening in the background when you
   do x'. Not sure how to resolve but I don't like it." (on "Credential operations") -> NAMING ROUND:
   candidates: The X's service (names the actor; metalanguage risk flagged) / The X's changes / keep.
9. ">> Isn't this about the schema (what CAN exist etc.) in the five projection model? Also, who
   needs to know this?" (on rules-and-errors) -> ANSWER: it is a MIX — grammar (uniqueness, enum
   membership), service authority (invalid-rejection), facade/authz (the access consequence). And the
   who-needs-it test exposes that this section's bullets DUPLICATE facts already stated at their
   stage (invalid-reject = states verbatim; enum membership = types; natural-key unique = identity).
   CONTRACT LINE ADDED: rules-and-errors = the enforcement surface — ONLY claims not already stated
   at their stage + the error taxonomy (the part users actually meet). The reader populations: charm
   devs meeting the errors, Juju devs maintaining the validators (the round-26 relevance bar).
   PAGE EDIT: bullets 1-3 removed (each now lives at its stage); access consequence + errors kept.

NAMING CANDIDATES (the round that sweeps ALL pages; awaits the pick):
- Umbrella h2s: (A) The X's declaration / The X's persistence / The X's execution [D/P/E kept;
  "execution" is the flagged phrase]; (B) The X's declaration / The X in Juju's databases / The X in
  operation [nominal, gloss-adjacent]; (C) question-form: How you declare the X / What Juju stores /
  What happens in the background [preattentive; breaks the nominal-title law].
- §5 title: The X's service (actor-naming; "service" borderline metalanguage) / The X's changes /
  keep X operations.
- Article: generic forms where the section talks generically (The -> bare or "A"); red thread
  (entity name in every title) unchanged.

## REVIEWER NOTES (session 36, post-close) — chain-spine rounds 4-6 feedback, recorded verbatim (triage in parens)

1. model.md lede: "this is a scenario where you have a 'multicloud controller' and where you may
   have 'cross-model relations (integrations)'" — ">> CMR is orthogonal to multicloud controller
   -- drop the 'and where...'" (TEXT fix, session-37 opening batch).
2. "Models in the execution layer": ">> What's there to say really? The model watchers, I
   suppose. But: The per operation subsections feel like they're taking us back to the
   declaration layer. The sequence diagrams actually allude to all the layers: The user sends
   commands to the client (BTW the client is missing from the model removal diagram), the client
   sends that declaration of intent to the controller, the controller persists it and the agent
   machinery gets to work. The only difference from something like application operations is that
   this agent work happens in the controller rather than on some other unit, and does not involve
   the unit agent but model agents. All in all I wonder if these per operation sections need to
   exist. I actually think not. Fundamentally what we want to communicate is the thingie about
   the model agent (I think that one shows up in debug-log -- check). Though removal does not
   involve the model agent -- hmm. Hmm. Help me think. Maybe it's okay that declaration and
   persistence elements (the client and the controller are still in the picture as context? the
   controller needs to be because it's part of the execution. but also part of the persistence.
   Do we need to zoom in on the controller? What if this slideshow was at the top of the entire
   doc, right beneath the title, as a story preview? It could combine a view of the declaration
   (a user talking to a client), of the persistence (maybe one model ERD to rule them all?), and
   of the execution, where the execution could have multiple slides? Help me think. What would
   the 'Model in the execution layer' be left with if we removed the diagrams? What's the story
   there, really? Model agent and what?"
   (DESIGN round — worked artifact required, no verdict asked; touches: whether per-operation
   subsections exist at all; the model-agent story — CHECK debug-log.md for where the model agent
   surfaces user-facing; ggarch DEFECT: the model-removal sequence lacks the client actor; the
   slideshow-as-story-preview-at-top idea = P0-1 territory, ADR-010 slideshow grammar + the
   architecture.md canonical-home pending call; connects to the non-entity/chain-walk spine
   investigation. Rides the P0-1 design conversation, not a unilateral edit.)
3. Model migration "For: Juju developers" chip: ">> model migration is for SREs etc. It's just
   that diagram that was estimated to be 1/5 for users and 5/5 for Juju devs. Drop the tag."
   (TEXT fix, session-37 opening batch.)
4. "The rules a model must satisfy": ">> Where are these rules enforced and by whom? I feel we're
   missing a generalization here." (DESIGN/slot-contract gap — the rules-and-errors slot lacks
   the enforcement-location/actor generalization; feeds the ADR-011 slot contracts; analysis
   round across the landed pages before any template change.)
5. charm.md Types of charm under persistence: ">> What does this have to do with the persistence
   layer? This is the kind of taxonomy that's phenomenological and has nothing to do with the
   data model etc., unlike credential types, which did. We should find a different way to handle
   this. If we can't think of a good solution, we could move the whole section as is to the end
   of the doc for a future iteration (you can insert a small TODO comment in the .md describing
   the issue)" (VERDICT: the D2 declare-which fix is INSUFFICIENT for the phenomenological case —
   session 37 round 0 decides: better home or the sanctioned fallback = move the section as-is to
   the end of charm.md with a TODO comment. Do not re-pin the round-6 placement.)
6. charm declaration sentence "You declare a charm by adding it to a model": ">> This is a very
   weak and confusing claim. Compare to this infinitely better one from credential.md: 'You add,
   update, or remove a cloud through a Juju client; adding a cloud requires controller superuser
   access.' (This one could use a link to the section in user.md that defines controller
   superuser access (or in the new access.md doc that we wanted to create), but otherwise it's a
   very nice first sentence -- concrete (you don't just repeat the declare root from the section
   title but rather give it tangible content with add, update, etc.), informative, etc."
   (TEMPLATE refinement for ALL declaration do-surface sentences: concrete verbs + the access
   requirement + a link to the access-level definition (user.md now / access.md later); applies
   to charm.md immediately and as an audit across the six landed pages. NOTE: the quoted sentence
   is cloud.md's declaration opener (round 2); the pattern, not the page, is the point.)
7. OVERALL QUESTION: "How did working with the new spine feel? Did it feel like things were
   falling into place more or less?" (Answered in the terminal; see SESSIONS addendum 138.)



## REVIEWER NOTES (session 37, mid-run) — independent degradation check on the 7 landed pages; recorded verbatim (triage below)

Structural spine PASSES on all 7 landed pages — "this is triage only, no re-open of the spine".

1. LIVE BROKEN REF (the session's own defect class — dead anchor with inbound ref):
   (data-model-full-spine)= sits at database.md:42 immediately before a {ggarch} directive,
   not a heading, so it renders no target. Inbound refs: model.md:52, controller.md:52,
   bundle.md:52. Repair = move the anchor onto the following heading in database.md
   (the-charm-origins precedent: repair by stacking onto a heading). Highest priority of this
   batch.

2. cloud.md — 3 omissions vs the current contract (contract-evolution lag from round 2, not
   decay):
   a. Rules chapter: enforcement bullets only, no error taxonomy and no facet-honest statement
      of absence (credential.md pattern absent).
   b. Persistence: the add/update/remove do-verbs from the declaration never reappear as
      recording acts — only the bootstrap seed is named. Siblings name the performing service
      (credential.md: "the credential service ... performs the writes"; model.md: "the model
      service ... performs the writes").
   c. Declaration chapter carries no client-vs-controller material beyond the do-sentence
      (credential.md carries the client-side/controller-side paragraph). Flag for triage, not
      force.

3. bundle.md — rules chapter title promises "errors", delivers two YAML rules, no taxonomy, no
   facet-honest absence statement. Grounded candidates in source: "bundle has an invalid type
   %q", "bundle machines not valid for Kubernetes bundles", "bundle declares an invalid base
   %q" (domain/deployment/charm/bundledata.go:510,514,523).

4. user.md:91 — unclosed code span: "Granted: Via `juju register." (opening backtick, no
   closer). Trivial fix.

NON-DEFECTS (no action): charm.md parked taxonomy = sanctioned be94aed469 treatment,
conformant; application.md "Application endpoint" h3 = intentional sub-entity home, 6 live
inbound refs; "client-vs-controller footnote" is implemented everywhere as the do-sentence
clients phrasing — no literal footnote syntax exists in docs/reference, so read the contract
item accordingly.

TRIAGE (session 37 addendum, on the record):
- Item 1: FIX (fix(database)) — verify the anchor + the three inbound refs first-hand, stack
  (data-model-full-spine) onto the following heading, inbound refs then point at a rendered
  target.
- Item 2a: FIX (docs, cloud.md) — write the cloud error taxonomy; ground the error names in
  domain/cloud + facade source before writing (no invented strings); if the domain has no
  typed taxonomy, say so facet-honestly and list the errors users actually meet.
- Item 2b: FIX (docs, cloud.md) — add the recording-acts sentence naming the performing
  service, credential.md/model.md pattern; ground the service name in domain/cloud.
- Item 2c: FLAGGED ONLY, no edit this batch (reviewer: "flag for triage, not force") — the
  non-defect note also reinterprets the contract item as the do-sentence clients phrasing, so
  the gap may be nil; parked for the next template conversation.
- Item 3: FIX (docs, bundle.md) — verify the three error strings at
  domain/deployment/charm/bundledata.go:510,514,523 first-hand, then add the taxonomy.
- Item 4: FIX (docs, user.md) — one-character class fix.
- NON-DEFECTS: no action; the footnote-contract reading recorded here for the next template
  conversation.
