# The general method — distilling reference docs that are Gricean for the reader (human or AI) and cheap for the maintainer

Session 101, 2026-10-22. Distilled from ~100 sessions of this project
(scout survey + direct reads of page-recipe.md, WORKING-RULES.md,
structure-discovery-plan.md, skeleton-v6.md, decisions-100.md,
grice-review-95.md). One-line answer first, then the loop.

**One line:** one fact, one home, stated once, in a place you can
predict before you read it — decided from the system's own schema,
grounded in its source with pointers, enforced by tools, and converged
by piloting on one small case with recorded verdicts.

## The loop (five passes)

1. **Discover the set before the prose (Quantity).** Pages and
   sections are decided by a structural rule, not taste: an entity
   with its own typed ID, facade, and lifecycle is a page
   ("the kind decides the level", page-recipe.md:69); a group is a
   section iff its lead table holds a NOT NULL foreign key into the
   page and no other page references it (structure-discovery-plan.md,
   the chunking rule — measured 100% stable across the corpus).
   Predictable chunking falls out of the schema: same fact, same home,
   every time — which is the maintainer's contract and the AI's map.

2. **Extract facts from the source of truth, never from old prose
   (Quality).** DDL scaffolding, facade extraction with ground
   pointers (file:line), then READ the code around each method — the
   extractor does not see helper-raised or cross-layer errors
   (page-recipe.md:7-12). A rule stays in a database-schema section
   only if the database itself enforces it; a rule a call applies
   moves to that call (:36). Say what is true, never what is absent
   (:32) — unearned negation is the classic Quality failure.

3. **Write against a fixed section grammar (Manner + cheap
   maintenance).** Lede (<= 3 sentences) -> `<Entity> database
   schema` -> change streams -> calls -> migration, each present only
   when its facts exist (:14-22). Opening sentences are definitions
   (:25); lists are built up to with a colon-ending intro (:68); base
   case before variants (:40); no metalanguage; closed vocabularies
   ("call" not "operation", "hook commands", "settings" never
   "databag"). Uniform anatomy per call: `Caller:` / `Rules:` /
   `Errors:` (:31). The reader learns the grammar once and reads
   every page; so does the reviewer.

4. **Enforce with tools, not vigilance.** `check_page_rules.py` on
   every page; `count_errors.py` with pinned totals
   (956/674/204/182 — never re-widen without the user); both docs
   builders at warning baselines; `ggarch check` on the models. A rule
   that cannot be checked gets a checker or gets dropped. The pinned
   totals are the refactor contract: sweeps (29 captions, 24 links)
   were provably non-regressive.

5. **Pilot, measure, record verdicts verbatim.** ssh-key.md took ~20
   rounds of user feedback before it converged; every surviving
   verdict became a cited rule in the recipe, every retraction is on
   record. Process law: present worked artifacts until the verdict is
   self-evident; do not ask for verdicts (TODOS.md:16-21). Measure
   before ruling — the caption/alt split, the llms bloat (84% of
   llms-full.txt was verbatim fenced model source), the density
   complaints ("bullets are not paragraphs in costume") were all
   measurements before they were rules.

## Why it satisfies both sides at once

Grice-for-the-reader and cheap-for-the-maintainer are the SAME
property: the schema decides the set (nobody re-argues the chunking),
the source grounds the claims (nobody re-verifies by prose), the
grammar fixes the shape (nobody re-invents the sections), the tools
pin the invariants (nobody re-checks by hand), and the pilot loop
records the verdicts (nobody re-litigates). The AI reader gains the
same map the maintainer does.

## Open tensions (honest)

- The schema cannot always read intent: the permission table's
  half-typed subject (`grant_to` typed, `grant_on` a bare string)
  needed a human judge (structure-discovery-plan.md, D-series).
- First-mention-linking does not reach captions yet (ggarch TODOS
  session-83 items 1-2).
- The old taxonomy sections (charm types) still have no home in the
  layered form (session 65, live).
- List pages vs entity pages, and how far the checker should reach
  into prose, remain argued per case.