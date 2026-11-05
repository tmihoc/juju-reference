# juju-reference

The working archive for the Juju entity-reference rework: [juju/juju PR #23661](https://github.com/juju/juju/pull/23661) (epic JUJU-9635), the reference epic JUJU-10585 and the error-contract epic JUJU-10586. The documentation itself is in the PR; this directory holds the method, the evidence and the queue.

**Start with `HANDOFF.md`.**

| Path | What it is |
|---|---|
| `HANDOFF.md`, `NEXT-PROMPT.md`, `TODOS.md` | Router, launch prompt, live queue |
| `method/` | The mechanism: `settled-results.md` (what the research established), `requirement-set.md`, `docs-decision-procedure.md`, `page-recipe.md`, `WORKING-RULES.md` |
| `method/evidence/` | Tests and decisions behind the mechanism (E83, the SSH decision) |
| `epics/` | The three epics: delivery plan, error contract, PR text, and `source-questions.md` (potential defects and questions for the Juju developers) |
| `tools/` | Page-rules checker, error counter, facade extractor, schema builder |
| `experiments/` | Two live inputs only: `e11` (the 4.1 DDL) and `e33` (the page manifest) |
| `memory-export/` | The user's standing preferences |
| `archive/` | Everything older: experiments E0 to E82, session records, skeletons, manifests, 64 launch prompts, 80 work notes. Paths inside keep their old layout. Read only to check an experiment's detail. |

All paths in these files are relative to this directory.
