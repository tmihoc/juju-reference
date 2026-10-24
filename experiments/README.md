# Experiments (2026-10-19)

Scripts and inputs behind the results in `../structure-discovery-plan.md`. Paths inside the scripts point at /tmp and at the scratch worktrees under ~/git/misc; adjust them.

- `xtab.py`, `xtab2.py`: cross-tab of documented errors by the code layer that creates them.
- `e1.py`: co-change of code areas between two commits (run with a revision range).
- `e0.py`: span of statements by the files their anchors appear in.
- `sample.json`, `rules.json`: the 40 sampled errors and 40 sampled rules for the blind classification; the rater prompts were built from them (definitions in the plan).
- `rel_items.json`, `rel_order.json`: the 39 statements for the audience ratings and their shuffled order.
- `agent-test/`: the 16-question agent test (`build.py` builds the prompts, `questions.json` holds the questions with rubric facts, `set-a..d.txt` are the prompts: a = layered whole page, b = pilot whole page, c = layered chunked, d = pilot chunked).
- `gen/gen.py`: helpers that build a 4.1 SQLite schema from the SQL files and emit ggarch chip models.
- `build.sh`: purged Sphinx build (`build.sh <worktree> <builder> <warnings-log>`).
- `e7/`: sentence-classification experiments E7 to E10 (extract*.py build the samples, analyse*.py score them, rater*.txt are the blind prompts, `reader/` holds the access.md reader test and the red-team report).
- `e11/`: the software study (real 4.1 DDL, `inventory.py`, `artifacts.py`, `census.py`, `observe.py`, `errors_tier2.py`). See `../skeleton-research-summary.md`.
- `e13/`: out-of-sample recall (E13): `claims.py` extracts the claims from the upstream/4.1 pages, `judge13.txt` is the judges' instruction, `e13_*.json` are claims and verdicts, `analyse13.py` scores them.
- `e14/`: close scrutiny of the claims that E13 left as not derivable (E14): `scrutiny14.txt` is the instruction, `e14_batch*.json` the claims, `e14_out*.json` the verdicts, `analyse14.py` the summary.
- `e15/`: version stability (E15): `e15.py` replays the 4.0.15 and 4.1 DDL in SQLite and diffs typing and inventories (`v4015-*.ddl` are copies of the release DDLs; the 4.1 DDL is `../e11/*.ddl`), `d.py` and `d2.py` compare the changed set with the source diff, `e15_domain.py` compares domain typing under both owner maps (needs `git archive ac643a09f7 domain core` unpacked into the scratch dir named in the script), `e15_*.json` hold the outputs.
- `e17/`: schema features against Go-level parts (E17, E17b), stability with topic ownership (`e15b.py`), part presence (`e19.py`), page-to-domain tests (`pages.json`, E20, `e20b.py`), `topics.json` (assignment of schema topics to domains), `inventory_table.py` (writes `../part-inventory.md`). `e16/` held-out identifier recall (underpowered). `e18/`: claim gate layers (`gate.py`, `gate_flags.py`, `gate_enum.py`) and the authority census (`authority.py`).
- `e17/gen_inventory.py`: per-domain part inventory generated from the code (output for all 36 domains in `../domain-inventories.md`).

## Added in sessions 79 and 80 (E29 to E42)
All scripts take their DDL from `e11/*.ddl` (4.1) and `e15/v4015-*.ddl` (4.0.15) and replay it in SQLite through `e15/e15.py` (fixed in E39: `space` is a record, the table named like the group leads). Source tree: `~/git/misc/juju-v2-preview`. Run each script from its own directory. `e15/e15.py` imports are relative (`sys.path.insert(0,'../e15')`).
- `e29/`: page unit by life-coupling and noun (E29 `e29.py`, E29b `e29b.py` removal-code coupling, `explore.py` the labelled exploratory pass).
- `e30/`: exposure by call graph (Go program, `main.go`; `analyse30.py`). Needs `GOFLAGS=-mod=mod GOPROXY=off` and x/tools from the offline cache.
- `e37/`: call graph with statement classification (insert, delete, update; `main.go`, `e37.py` primitives), `e38.py` (withdrawn principle), `e38b.py` (not-null owners), `e38c.py` (identifying key; weak tables). Build `go build -o e37bin`, run `./e37bin ~/git/misc/juju-v2-preview tables.txt out.json`.
- `e33/`: page inventory and manifest: `e33.py` (first-token rule), `e33b.py` (writer domain), `manifest.py` and `render_manifest.py` (the reviewed manifest, `page-manifest.json`), `m3.py` (cohesion), `m4m5.py` (new-table fallback, existing pages), `e35.py` (character or leg), `e36.py` (kind or mass), `e33_ggarch.py` (diagram pairing).
- `e39/`: instrument audit: `audit.py`, `z7.py` (write classification), `z9.py` (address match), `fix.py`, `test_instruments.py` (run `python3 -m unittest -v test_instruments`; 8 tests), `baseline/` the numbers before the fix.
- `e40/`: the claims ledger: `rows.py` (one row per claim, with plan line ranges and the numbers to check), `check.py` (coverage, number and basis checks, contradiction list; writes `ledger.json`), `render.py` (writes `../claims-ledger.md` and the L4 selection), `check_v6.py` (every citation in `skeleton-v6.md` is a settled row bare or a partial row starred).
- `e41/`: page or section by mandatory single owner and no dependents (`e41.py`; `e41_posthoc.py` the labelled variant).
- `e42/`: deep blind placement: `score.py` scores `judges/io/m1deep_out_{a,b}.json` against the manifest and splits disagreements into those the weak-table rule already decides and open ones.
- `judges/`: judge prompts and their inputs and outputs. Saved prompts: `scrutiny27.txt` (E27, E32 claim check), `ledger_reader40.txt` (E40b), `placement42.txt` (E42). `io/` holds every input and output (`m1*`, `m2*`, `e32*`, `e33*`, `e35*`, `e38c*`, `z8*`, `e40*`, `m1deep*`) and the scaffolds. The prompts of the fit tests (E21 to E21d), the manifest audits (E33 I2, E34 M1 and M2), the character-or-leg judge (E35) and the existing-pattern checks were not saved as files; the inputs and outputs are, and the instructions are described in the plan entries.
- `logs/`: build logs of the call-graph programs.
- `e29/`: page-unit exploration (`explore.py`, `e29.py`, `e29b.py`): first-word and foreign-key signals, removal-code coupling. Run from the directory; needs `../e15`.
- `e30/`: call-graph exposure program in Go (`main.go`, `go.mod`, `tables.txt`, `viewmap.json`, `analyse30.py`); build `GOFLAGS=-mod=mod GOPROXY=off go build -o e30bin .`, run `./e30bin ~/git/misc/juju-v2-preview tables.txt e30_roots.json`; the tuning list is in the plan (E30). `e37/`: the same program with insert, delete and update classification (`main.go`, `e37.py` primitives, `e38.py`, `e38b.py`, `e38c.py` page or section, `fn_stm.json` per state function sets).
- `e33/`: page inventory and manifest (`e33.py`, `e33b.py`, `manifest.py` then `render_manifest.py`, `m3.py`, `m4m5.py`, `e33_ggarch.py`, `e35.py`, `e36.py`); outputs `page-manifest.json` and `../../page-manifest.md`. `manifest.py` rewrites `page-manifest.json`: always run `render_manifest.py` after it.
- `e39/`: instrument audit (`audit.py`, `z7.py`, `z9.py`, `fix.py`, `test_instruments.py`; run `python3 test_instruments.py`; `baseline/` holds before and after outputs of the reruns).
- `e27/`, `e13/`, `e14/`: claim judging with the close-scrutiny prompt (`judges/scrutiny27.txt`).
- `judges/`: judge prompts (`prompts/`), inputs and outputs (`io/`); `logs/`: build and analysis logs.

