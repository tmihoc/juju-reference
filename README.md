# juju-reference

The working archive of the Juju entity-reference rework: the method, the
research, the session records, and the tooling behind
[juju/juju PR #23661](https://github.com/juju/juju/pull/23661) (epic
JUJU-9635) and the error-contract epic (JUJU-10586).

Where things live:

- **Start here:** `HANDOFF.md` (the router: discipline, state, queue),
  `NEXT-PROMPT.md` (the launch prompt of the latest session; every earlier
  one archived under `prompts/`), `SESSIONS.md` (the session log),
  `TODOS.md` (the live queue).
- **The method:** `page-recipe.md` (the page form and its rules),
  `WORKING-RULES.md`, `error-contract-epic.md`, and
  `work/general-method-101.md` (the distilled five-pass loop).
- **The tooling:** `tools/` (the page-rules checker, the error-counter, the
  facade extractor, and the research scripts). The CI guard itself —
  `check_error_contract.py` — lives in the PR, not here.
- **The research:** `experiments/` (the skeleton studies E27-E48, with
  pre-registrations in `structure-discovery-plan.md`), the manifest files,
  and `skeleton-v5.md`/`v6.md`.
- **The session work records:** `work/` (decisions, sweeps, reviews),
  including `work/ggarch-state/` — a dated snapshot of the ggarch stream's
  live queue and session notes (the live files live in the ggarch repo,
  untracked there by convention).

Everything here is work-in-progress notes and research, not documentation;
the documentation itself is in the PR. The 4.1 code is the source of truth
for every claim the pages make.
