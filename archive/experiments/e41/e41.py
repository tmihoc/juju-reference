"""E41: page or section for a group with one owner and no dependents.

Rule (pre-registered in structure-discovery-plan.md, E41): G is a section of
P iff (a) the lead table of G has a NOT NULL foreign key (not a lookup, not a
self reference) into chunks of exactly one other page P and (b) no table of
any other page references a table of G. Otherwise G is a page.

Run from experiments/e41: python3 e41.py
"""
import collections
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, "..", "e37"))
sys.path.insert(0, "../e15")
import e15  # noqa: E402

exec(open("e38.py").read().split("fk,lookup=fkmap(e15.NEW)")[0])  # man, CARVE, chunk, chunks, fkmap


def build(ddl):
    dbs = {}
    for s in ("model", "controller"):
        db = sqlite3.connect(":memory:")
        for st in e15.split(open(ddl[s]).read()):
            db.executescript(st.rstrip().rstrip(";") + ";")
        dbs[s] = db
    return dbs


def fk_rows(dbs, t):
    """(column, parent, not_null, in_key) for table t, from SQLite."""
    for db in dbs.values():
        info = {r[1]: r for r in db.execute(f'PRAGMA table_info("{t}")')}
        if not info:
            continue
        pk = {c for c, r in info.items() if r[5] > 0}
        return [(r[3], r[2], bool(info[r[3]][3]) or r[3] in pk, r[3] in pk)
                for r in db.execute(f'PRAGMA foreign_key_list("{t}")')]
    return []


def classify(ddl, tabs=None):
    dbs = build(ddl)
    V = {s: e15.parse(ddl[s]) for s in ("model", "controller")}
    lookup = {t for s in V for t in V[s]["tables"]
              if e15.typing(V[s], t)["lookup"]} - {"space"}
    members = collections.defaultdict(list)
    for t, c in chunk.items():
        if (tabs is None or t in tabs) and t not in lookup:
            members[c].append(t)
    # dependents: other chunks that have a foreign key into a table of G
    deps = collections.defaultdict(set)
    for t, c in chunk.items():
        if t in lookup or (tabs is not None and t not in tabs):
            continue
        for col, par, nn, pk in fk_rows(dbs, t):
            pc = chunk.get(par)
            if pc and pc != c and par not in lookup:
                deps[pc].add(c)
    res = {}
    for g, G in members.items():
        indeg = collections.Counter()
        for t in G:
            for col, par, nn, pk in fk_rows(dbs, t):
                if par in G and par != t:
                    indeg[par] += 1
        L = e15.lead_table(g, G, indeg)
        owners, attr, ident = set(), set(), set()
        for col, par, nn, pk in fk_rows(dbs, L):
            pc = chunk.get(par)
            if par in lookup or not pc or pc == g or par == L:
                continue
            (owners if nn else attr).add(pc)
            if pk:
                ident.add(pc)
        a = len(owners) == 1
        b = not deps[g]
        res[g] = dict(lead=L, owners=sorted(owners), nullable=sorted(attr - owners),
                      identifying=sorted(ident), dependents=sorted(deps[g]),
                      a=a, b=b,
                      level=("section of " + sorted(owners)[0]) if a and b else "page")
    return res


if __name__ == "__main__":
    R1 = classify(e15.NEW)
    for g, r in sorted(R1.items(), key=lambda x: (x[1]["level"] == "page", x[0])):
        print("%-24s %-26s lead=%-28s owners=%-20s deps=%s" % (
            g, r["level"], r["lead"], r["owners"], r["dependents"][:5]))
    json.dump(R1, open(os.path.join(HERE, "e41_result.json"), "w"), indent=1)

    def sec(g):
        return R1[g]["level"].startswith("section")
    P1 = ["port", "unit-state", "application-scale", "machine-placement", "cloud-instance"]
    P2 = ["machine", "application", "unit", "model", "charm", "cloud", "user",
          "relation", "secret", "storage"]
    print("\n(1) sections", [(g, R1[g]["level"]) for g in P1 if g in R1],
          sum(sec(g) for g in P1 if g in R1), "of", len(P1))
    print("(2) pages", [(g, R1[g]["level"]) for g in P2 if g in R1],
          sum(not sec(g) for g in P2 if g in R1), "of", len(P2))
    P3 = ["telemetry", "agent-version", "model-defaults", "zone", "link-layer-device",
          "external-controller", "object-store"]
    print("(3) reported", [(g, R1[g]["level"], R1[g]["owners"], R1[g]["dependents"][:3])
                            for g in P3 if g in R1])
    P4 = ["permission", "relation-unit"]
    print("(4) reported", [(g, R1[g]["level"], R1[g]["owners"], R1[g]["dependents"][:3])
                            for g in P4 if g in R1])

    # (a) stability on 4.0.15 for chunks with no changed table
    ch = json.load(open("../e15/e15_result.json"))
    chg = set(ch["model"]["changed_C"]) | set(ch["controller"]["changed_C"])
    old_tabs = set()
    for s in ("model", "controller"):
        old_tabs |= set(e15.parse(e15.OLD[s])["tables"])
    common = {t for t in chunk if t in old_tabs}
    R0 = classify(e15.OLD, tabs=common)
    unchanged = [g for g in R1 if g in R0
                 and not any(t in chg for t, c in chunk.items() if c == g)]
    same = [g for g in unchanged if R0[g]["level"] == R1[g]["level"]]
    print("\n(a) chunks with no changed table: %d; same level in 4.0.15: %d = %.0f%%" % (
        len(unchanged), len(same), 100 * len(same) / max(1, len(unchanged))))
    print("   differing:", [(g, R0[g]["level"], R1[g]["level"])
                            for g in unchanged if g not in same])
