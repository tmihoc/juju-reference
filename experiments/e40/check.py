"""E40 ledger checks (criteria fixed in structure-discovery-plan.md, E40).

Usage: python3 check.py   (run from experiments/e40)
Writes ledger.json and prints the four criteria and the contradiction list.
"""
import json
import re
import sys
from pathlib import Path

from rows import ROWS, CONTRA_B

ROOT = Path(__file__).resolve().parents[2]
PLAN = (ROOT / "structure-discovery-plan.md").read_text().split("\n")
SKEL = (ROOT / "skeleton-v5.md").read_text().split("\n")
SETTLED = {"code", "user", "convention"}
STATUSES = {"supported", "partial", "falsified", "open", "withdrawn",
            "convention", "user"}


def rule_lines():
    """Non-blank rule lines of the skeleton (1-based numbers)."""
    out = []
    for i, line in enumerate(SKEL, 1):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("Status:"):
            continue
        if s.startswith("|---") or s.startswith("| Part |"):
            continue
        out.append(i)
    return out


def plan_text(ranges):
    parts = []
    for a, b in ranges:
        parts.extend(PLAN[a - 1:b])
    return "\n".join(parts)


def main():
    bad = []
    ids = [r["id"] for r in ROWS]
    if len(ids) != len(set(ids)):
        bad.append("duplicate ids")
    for r in ROWS:
        if r["status"] not in STATUSES:
            bad.append(f"{r['id']}: status {r['status']}")
        for d in r["dep"]:
            if d not in ids:
                bad.append(f"{r['id']}: unknown dependency {d}")

    # (1) coverage
    rl = rule_lines()
    cited = {n for r in ROWS for n in r["skel"]}
    missing = [n for n in rl if n not in cited]
    print(f"(1) coverage: {len(rl) - len(missing)} of {len(rl)} rule lines "
          f"cited; missing {missing}")

    # (2) number check
    nf, nt = [], 0
    for r in ROWS:
        txt = plan_text([tuple(x) for x in r["plan"]])
        for n in r["nums"]:
            nt += 1
            if n not in txt:
                nf.append((r["id"], n))
    print(f"(2) numbers: {nt - len(nf)} of {nt} found in the cited plan "
          f"lines; not found {nf}")

    # (3) supported rows need a settled basis
    weak = [r["id"] for r in ROWS
            if r["status"] == "supported" and not (set(r["basis"]) & SETTLED)]
    print(f"(3) supported rows without code, user or convention basis: {weak}")

    # status table
    from collections import Counter
    c = Counter(r["status"] for r in ROWS)
    print("status:", dict(c), "total", len(ROWS))
    print("basis only judge/precedent:",
          [r["id"] for r in ROWS if not (set(r["basis"]) & SETTLED)])

    # (4) contradictions: skeleton rules whose supporting row is not supported
    contra = []
    for r in ROWS:
        if r["skel"] and r["status"] in ("falsified", "withdrawn"):
            contra.append((r["id"], r["status"], r["skel"], r["claim"][:80]))
    print("(4) rules resting on falsified or withdrawn rows:")
    for x in contra:
        print("   ", x)

    print("    rule (b), a later entry changes the rule:")
    for ln, rid, why in CONTRA_B:
        assert rid in ids, rid
        assert ln in rl, ln
        print(f"    skeleton line {ln} against {rid}: {why[:90]}")
    print("    not in the skeleton at all (supported rows with empty skel):",
          [r["id"] for r in ROWS if not r["skel"] and r["status"] in
           ("supported", "partial", "user")])

    json.dump(ROWS, open(Path(__file__).with_name("ledger.json"), "w"),
              indent=1)
    if bad:
        print("STRUCTURE ERRORS:", bad)
        sys.exit(1)


if __name__ == "__main__":
    main()
