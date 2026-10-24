"""Render claims-ledger.md from rows.py and apply the L4 selection rule."""
from pathlib import Path
from rows import ROWS, CONTRA_B

ROOT = Path(__file__).resolve().parents[2]
SETTLED = {"code", "user", "convention"}
LIVE = {"C45", "C47", "C52", "C53", "C54", "C58", "C23", "C24", "C09"}


def l4(r):
    """(a) a next-skeleton rule or live decision rests on it, and (b) its
    basis is a judge or precedent without a code check, or it passed at the
    limit."""
    a = r["id"] in LIVE or (r["skel"] and r["status"] != "falsified")
    judge_only = not (set(r["basis"]) & {"code", "user"}) or (
        "judge" in r["basis"] and "precedent" in r["basis"])
    limit = any(w in r["crit"] for w in ("narrowly", "at the limit"))
    return bool(a and (judge_only or limit))


def main():
    out = ["# Claims ledger (E40, session 80, 2026-10-20)", "",
           "Every row cites the lines of `skeleton-v5.md` that state it and "
           "the lines of `structure-discovery-plan.md` that carry the "
           "evidence. Numbers are checked by `experiments/e40/check.py` "
           "against those plan lines. Status is read from the plan entry: a "
           "registered criterion that was missed is never `supported`, and "
           "a post hoc rescue is labelled in the row. `basis` is what the "
           "claim stands on: code (derived from or checked against the 4.1 "
           "code), judge (an LLM reader), precedent (agreement with existing "
           "pages or how-tos, weak by the 2026-10-20 correction), user "
           "(decision), convention.", ""]
    from collections import Counter
    c = Counter(r["status"] for r in ROWS)
    out += ["Status counts: " + ", ".join(f"{k} {v}" for k, v in
                                          sorted(c.items())), "",
            "| id | status | basis | claim | evidence strength | registered "
            "criterion and readings | skeleton lines | re-test (L4) |",
            "|---|---|---|---|---|---|---|---|"]
    for r in ROWS:
        def e(s):
            return s.replace("|", "/").replace("\n", " ")
        cell_ver = (" **Verified here:** " + e(r["verified"])) if r["verified"] else ""
        cell_note = (" Note: " + e(r["note"])) if r["note"] else ""
        out.append(
            f"| {r['id']} | {r['status']} | {', '.join(r['basis'])} | "
            f"{e(r['claim'])}{cell_ver}{cell_note} | {e(r['strength'])} | "
            f"{e(r['crit'])} | {', '.join(map(str, r['skel'])) or '-'} | "
            f"{'yes' if l4(r) else ''} |")
    out += ["", "## Contradictions with skeleton-v5.md (rule b: a later entry "
            "changes the rule)", "",
            "| skeleton line | row | what is wrong |", "|---|---|---|"]
    for ln, rid, why in CONTRA_B:
        out.append(f"| {ln} | {rid} | {why} |")
    out += ["", "## Rows selected for re-test by the L4 rule", ""]
    for r in ROWS:
        if l4(r):
            out.append(f"- {r['id']} ({r['status']}; {', '.join(r['basis'])}): "
                       f"{r['claim'][:110]}")
    (ROOT / "claims-ledger.md").write_text("\n".join(out) + "\n")
    print("selected:", [r["id"] for r in ROWS if l4(r)])


main()
