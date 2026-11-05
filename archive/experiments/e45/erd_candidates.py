"""E45 (S) kind: per manifest page, the tables joined by foreign keys inside the
page, as connected components over the 4.1 DDL. Threshold registered in the plan:
an ERD candidate has a component of 4 to 12 tables. Output: erd_candidates.json"""
import json, os, re, collections
E = os.path.expanduser("~/git/misc/juju-reference/experiments")
man = json.load(open(f"{E}/e33/page-manifest.json"))["pages"]
home = {t: p for p, d in man.items() for t in d["tables"]}
lookups = {t for d in man.values() for t in d.get("lookups", [])}
# also lookups listed under the shared vocabulary
sv = json.load(open(f"{E}/e33/page-manifest.json"))["shared_vocabulary"]
shared = set(sv) if isinstance(sv, list) else set(sv.keys()) if isinstance(sv, dict) else set()
edges = collections.defaultdict(set)   # table -> referenced tables
for f in ("model.ddl", "controller.ddl"):
    ddl = open(f"{E}/e11/{f}").read()
    for m in re.finditer(r"CREATE TABLE\s+(?:IF NOT EXISTS\s+)?\"?([a-z_0-9]+)\"?\s*\((.*?)\n\);", ddl, re.S | re.I):
        t, body = m.group(1), m.group(2)
        for r in re.finditer(r"REFERENCES\s+\"?([a-z_0-9]+)\"?", body, re.I):
            if r.group(1) != t:
                edges[t].add(r.group(1))
out = {}
for p, d in man.items():
    tabs = set(d["tables"])
    adj = {t: set() for t in tabs}
    n_edges = 0
    for t in tabs:
        for r in edges.get(t, ()):
            if r in tabs:
                adj[t].add(r); adj[r].add(t); n_edges += 1
    seen, comps = set(), []
    for t in sorted(tabs):
        if t in seen: continue
        stack, c = [t], set()
        while stack:
            x = stack.pop()
            if x in c: continue
            c.add(x); stack.extend(adj[x] - c)
        seen |= c; comps.append(sorted(c))
    comps.sort(key=len, reverse=True)
    out[p] = {"kind": d["kind"], "tables": len(tabs), "fk_edges_inside": n_edges,
              "largest": len(comps[0]) if comps else 0, "largest_tables": comps[0] if comps else [],
              "components": [len(c) for c in comps], "points_to": d.get("points_to", [])}
json.dump(out, open("erd_candidates.json", "w"), indent=1)
print(f"{'page':22}{'kind':10}{'tables':>7}{'edges':>6}{'largest':>8}  verdict")
for p, v in sorted(out.items(), key=lambda kv: -kv[1]["largest"]):
    L = v["largest"]
    verdict = "ERD" if 4 <= L <= 12 else ("split (>12)" if L > 12 else "no diagram (<4)")
    print(f"{p:22}{v['kind']:10}{v['tables']:7}{v['fk_edges_inside']:6}{L:8}  {verdict}")
