"""Regenerate the Schema model of docs/juju.ggarch from the 4.1 model DDL:
scaffold the listed tables, re-add the quoted "key" columns the scaffold drops,
and replace the model "Schema" block in the docs file."""
import json, re, subprocess, os
E = os.path.expanduser("~/git/misc/juju-reference/experiments")
G = os.path.expanduser("~/git/misc/juju-diagrams/docs/juju.ggarch")
c = json.load(open("erd_candidates.json"))
tables = c["relation"]["largest_tables"] + c["action"]["largest_tables"] + \
    ["model", "model_agent", "model_constraint", "model_life"]
sc = subprocess.run(["ggarch", "scaffold", f"{E}/e11/model.ddl", "--db", "model", "--tables", ",".join(tables)],
                    capture_output=True, text=True, check=True).stdout
for t in ("relation_unit_setting", "relation_unit_setting_archive", "relation_application_setting", "operation_parameter"):
    pat = re.compile(r'(    %s \[type: record.*?fields \{\n)' % t, re.S)
    assert pat.search(sc), t
    sc = pat.sub(lambda m: m.group(1) + '        key [label: "key", type: "text", pk: true]\n', sc, 1)
head = '''// The data model: the tables behind the reference pages, scaffolded from the
// 4.1 DDL by experiments/e45/build_schema.py (`ggarch scaffold model.ddl --db
// model --tables ...`). The scaffold drops quoted column names, so each "key"
// column is added by hand.
'''
s = open(G).read()
i = s.index("// The data model:"); j = s.index('model "Schema"')
k = s.index("\n}\n", j) + 3
s = s[:i] + head + sc[sc.index('model "Schema"'):].rstrip("\n") + "\n" + s[k:]
open(G, "w").write(s)
