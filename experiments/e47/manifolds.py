#!/usr/bin/env python3
"""E47: list the manifolds of each engine in the 4.1 tree, with the gating
wrapper (ifController, ifPrimaryController, ...) that decides where they run.
usage: manifolds.py TREE > manifolds.json
A manifold entry is a key of a dependency.Manifolds literal, at the first level of
the literal, followed by an optional chain of wrapper calls (if...(...))."""
import re, sys, json, os
T = sys.argv[1]
FILES = {
 "machine": "cmd/jujuagentd/agent/machine/manifolds.go",
 "model": "cmd/jujuagentd/agent/model/manifolds.go",
 "unit": "internal/worker/deployer/unit_manifolds.go",
 "modeloperator": "cmd/jujuagentd/agent/modeloperator/manifolds.go",
 "containeragent-unit": "cmd/containeragent/unit/manifolds.go",
 "safemode": "cmd/jujuagentd/agent/safemode/manifolds.go",
 "dbrepl": "cmd/jujuagentd/agent/dbrepl/manifolds.go",
}
out = {}
for eng, f in FILES.items():
    src = open(os.path.join(T, f)).read().split("\n")
    funcs = {}
    cur = None; inlit = False; depth = 0
    entries = []
    for i, line in enumerate(src):
        m = re.match(r'^func (\(.*?\) )?(\w+)\(', line)
        if m: cur = m.group(2)
        if re.search(r'dependency\.Manifolds\{\s*$', line) and not line.strip().startswith("//") and "func" not in line:
            inlit = True; depth = 0
            continue
        if inlit:
            if re.match(r'^\t\}', line):
                inlit = False; continue
            m = re.match(r'^\t\t(\w+(?:\.\w+)?):\s*(.*)$', line)
            if m:
                name, rest = m.groups()
                gates = []
                r = rest
                while True:
                    g = re.match(r'^(if\w+|\w+\.If\w+)\(', r)
                    if not g: break
                    gates.append(g.group(1)); r = r[g.end():]
                entries.append({"func": cur, "key": name, "gates": gates, "line": i + 1, "ctor": r[:60]})
    out[eng] = entries
json.dump(out, sys.stdout, indent=1)
