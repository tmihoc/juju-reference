"""E42 scoring (criteria pre-registered in structure-discovery-plan.md, E42).

A disagreement is class 'weak-rule' when the table is weak (a foreign key
column is part of its primary key) and the manifest homes it on the page of
the table that the key points to (the owner), i.e. E38c decides for the
manifest. Everything else is 'open' and is adjudicated by reading the code.
Run from experiments/e42: python3 score.py
"""
import collections
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["x"]
spec = importlib.util.spec_from_file_location("e41", os.path.join(HERE, "..", "e41", "e41.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
e15, chunk = m.e15, m.chunk
dbs = m.build(e15.NEW)
IO = os.path.join(HERE, "..", "judges", "io")

man = json.load(open(os.path.join(HERE, "..", "e33", "page-manifest.json")))
home = {t: p for p, d in man["pages"].items() for t in d["tables"]}


def key_parents(t):
    return {par for c, par, nn, k in m.fk_rows(dbs, t) if k}


def main(parts):
    J = []
    for n in parts:
        J += json.load(open(os.path.join(IO, f"m1deep_out_{n}.json")))
    names = set()
    for n in parts:
        names |= {t["table"] for t in json.load(open(os.path.join(IO, f"m1deep_input_{n}.json")))["tables"]}
    got = collections.Counter(r["table"] for r in J)
    print("input", len(names), "output", len(J), "missing", sorted(names - set(got)),
          "dups", [t for t, c in got.items() if c > 1])
    agree = [r for r in J if r["page"] == home.get(r["table"])]
    dis = [r for r in J if r["page"] != home.get(r["table"])]
    print("(1) agreement %d of %d = %.1f%%" % (len(agree), len(J), 100 * len(agree) / len(J)))
    ev = [r for r in J if r.get("evidence")]
    print("(3) cite file:line %d of %d = %.0f%%; 'name only' notes %d" % (
        len(ev), len(J), 100 * len(ev) / len(J),
        sum('name only' in (r.get('note') or '').lower() for r in J)))
    weak, opn = [], []
    for r in dis:
        t = r["table"]
        owners = {chunk.get(p) for p in key_parents(t)} - {None}
        (weak if home.get(t) in owners else opn).append(r)
    print("(4) disagreements %d: weak-rule decides for the manifest %d; open %d" % (
        len(dis), len(weak), len(opn)))
    print("    weak-rule, by judge page:", dict(collections.Counter(r['page'] for r in weak)))
    print("    open:")
    for r in opn:
        print("     %-40s manifest=%-16s judge=%-14s alt=%-14s %s" % (
            r["table"], home.get(r["table"]), r["page"], r.get("alt"), (r.get("evidence") or "")[:55]))
    json.dump(dict(agree=len(agree), total=len(J), weak=[r["table"] for r in weak],
                   open=[r["table"] for r in opn]),
              open(os.path.join(HERE, "e42_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:] or ["a"]) if False else main(["a"] + (["b"] if os.path.exists(os.path.join(IO, "m1deep_out_b.json")) else []))
