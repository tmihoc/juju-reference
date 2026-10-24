"""E45 ranking: S candidates by exposure (facade kinds and facade count from
e11/artifacts.json for the page's domain) and reach (pages whose points_to name
the page), plus the L facts counted from the DDL. Output: rank_result.json"""
import json, os, re
E = os.path.expanduser("~/git/misc/juju-reference/experiments")
cand = json.load(open("erd_candidates.json"))
art = json.load(open(f"{E}/e11/artifacts.json"))
reach = {p: 0 for p in cand}
for p, v in cand.items():   # points_to entries end with "(<page>)"
    for t in v["points_to"]:
        m = re.search(r"\(([a-z-]+)\)\s*$", t)
        if m and m.group(1) in reach: reach[m.group(1)] += 1
DOMAIN = {"action": "operation", "model-migration": "modelmigration", "user": "access",
          "secret-backend": "secretbackend", "offer": "crossmodelrelation"}  # page to domain directory
rows = []
for p, v in cand.items():
    if not 4 <= v["largest"] <= 12: continue
    a = art.get(DOMAIN.get(p, p.replace("-", "")), {})
    rows.append(dict(page=p, tables=v["largest"], facade_kinds=len(a.get("facade_kinds", {})),
                     facades=a.get("facades", 0), reach=reach[p]))
rows.sort(key=lambda r: (-r["facade_kinds"], -r["reach"], -r["facades"]))
ddl = open(f"{E}/e11/model.ddl").read()
life = re.findall(r"CREATE TABLE (\w+) \([^;]*?life_id", ddl)
vals = re.findall(r"CREATE TABLE (\w+_status_value|\w+_status_type)\b", ddl)
out = dict(S=rows, life_tables=len(set(life)), status_lookups=sorted(set(vals)))
json.dump(out, open("rank_result.json", "w"), indent=1)
for r in rows: print(r)
print("life tables", len(set(life)), "status lookups", len(set(vals)), sorted(set(vals)))
