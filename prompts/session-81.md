# Launch prompt for the next session (overwritten at the end of every session; every version is archived in prompts/session-<N>.md)

Written at the end of session 80, 2026-10-20. The user starts a new chat with: "Read ~/git/misc/juju-reference/NEXT-PROMPT.md and do what it says."

---

You are continuing a research project on the structure of Juju reference documentation. Work in `~/git/misc/juju-reference` (not the main checkout `~/git/juju`, which you must never touch). The code under study is the worktree `~/git/misc/juju-v2-preview` (Juju 4.1; branch `wip-entity-reference-pilots` holds the pilot pages and must never be pushed).

## Read first, in this order
1. `HANDOFF.md` (state, discipline, next step, environment). The "State at the end of session 80" block is current.
2. `skeleton-v6.md` and `claims-ledger.md` (what is supported: a bare `Cnn` is settled, `Cnn*` is partial).
3. The last entries of `structure-discovery-plan.md`: E40 to E44.
4. `TODOS.md` live queue. `WORKING-RULES.md` and `memory-export/MEMORY.md` for the user's standing preferences.

## Standing directives from the user
- Never ask for verdicts or offer option menus. Investigate and let the right decision come out from first principles.
- Always choose the best next thing, optimising for an early result without compromising first principles.
- Readers are both human and AI, more likely AI. Performance against AI readers is enough for a reader test.
- Pre-register before running anything (question, criteria, thresholds, caveats in the plan); report fails as fails; label every post hoc reading.
- Code is the source of truth. Existing pages, how-tos and Terraform docs are precedent, which is weak evidence.
- Compute numbers by script; never write a count into the plan from memory (two such errors were made in session 80).
- Propose before changing the skeleton or adding a section to a page. Ask before any push; push to origin only.
- Run git network, Go, Sphinx and shell commands with the sandbox disabled.

## Your task: E44, the AI reader test (already pre-registered in the plan; follow it exactly)
1. Check that subagents can run at all: launch one trivial `task` agent that writes a one-line file. If it fails with a 402 credit-limit error, stop and tell the user; do not work around it and do not run judges in-session.
2. Write the 12 questions per page for `machine`, `controller`, `access`, `ssh-key` from the 4.1 code (file and line for each ground truth, 2 of 12 unanswerable, at least a third answered outside the section a keyword search hits first). Check every ground truth in the code before it is used; drop and list any question whose answer is false.
3. Save the three prompts to `experiments/judges/`: `reader44.txt`, `grader44.txt`, `questions44.txt`. Put inputs and outputs under `experiments/judges/io/e44_*`. Put scripts (chunkers, retrieval, scoring) in `experiments/e44/`.
4. Run the conditions and the second independent question set as the entry specifies. Score with a script. Adjudicate disagreements against the code.
5. Record results in the plan (E44 results), add or update ledger rows in `experiments/e40/rows.py`, rerun `check.py`, `render.py` and `check_v6.py`, update `skeleton-v6.md` only as the ledger changes, then update `HANDOFF.md`, `TODOS.md`, `SESSIONS.md`.
6. Then continue the live queue in `TODOS.md` (the pipeline command is next). Phase 2 of E44 (a `space` page written under v6 and claim-checked) follows once phase 1 is read.

## Known weak spots, do not hide them
- 49 of 63 ledger rows have had no second reader, including all 17 settled rows cited bare in v6.
- All judges are the same model family as the author.
- Ten page groups split between the judges and the schema rule (E43); charm, subnet and resource are two-way cases for the user. Agent and Failure parts have no surviving rule.

## End of session
1. Write the next launch prompt to `NEXT-PROMPT.md` (overwrite) and copy it unchanged to `prompts/session-<N>.md`, where N is the session it launches. Never edit an archived prompt.
2. Append the outcome to `SESSIONS.md` with a one-line pointer to the prompt file that launched this session (`Launched by prompts/session-<N>.md`).
3. Tell the user the one-line start.
