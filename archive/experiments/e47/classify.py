#!/usr/bin/env python3
"""E47 step 2: apply the criteria registered in structure-discovery-plan.md."""
import json, collections, re
d = json.load(open("manifolds.json"))
def name(k): return re.sub(r'(Name)?$', '', k.split(".")[-1])
CTRL = re.compile(r'^if(Primary)?Controller$|^ifController(?!ProxyReady|AgentConfig)|^ifNotController|^ifNotPrimaryController')
# (1) totality: every manifold has its engine; keys listed by two engines
owner = collections.defaultdict(set)
for eng, v in d.items():
    for x in v: owner[x["key"]].add(eng)
multi = {k: sorted(e) for k, e in owner.items() if len(e) > 1}
print("(1) manifolds:", sum(len(v) for v in d.values()), "in", len(d), "engines; keys listed by more than one engine:", len(multi))
for k, e in sorted(multi.items()): print("    ", k, e)
# (3) controller subset of the machine engine
m = d["machine"]
ctrl = [x for x in m if any(CTRL.match(g) for g in x["gates"])]
print("(3) machine engine manifolds:", len(m), "controller-gated by wrapper:", len(ctrl), "=%.0f%%" % (100*len(ctrl)/len(m)))
print("    gated others:", collections.Counter(g for x in m for g in x["gates"] if not CTRL.match(g)).most_common())
print("    controller-gated keys:", sorted(name(x["key"]) for x in ctrl))
# (2) the four C23 topics: where do their workers run?
topics = {"unit engine": ("unit", None), "application provisioner": None, "secrets": None, "storage": None}
def find(pat):
    r = []
    for eng, v in d.items():
        for x in v:
            if re.search(pat, x["key"], re.I): r.append((eng, x["func"], x["key"], x["gates"]))
    return r
for t, pat in (("application", r"application(provisioner)?|appprov|caasapplication"), ("secrets", r"secret"), ("storage", r"storage")):
    print("(2)", t)
    for r in find(pat): print("    ", r)
print("(2) unit engine:", len(d["unit"]), "manifolds:", sorted(name(x["key"]) for x in d["unit"]))
print("model engine:", sorted(name(x["key"]) for x in d["model"]))
