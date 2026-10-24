#!/usr/bin/env python3
"""Scaffold the data model of one page into a ggarch model, ready to paste into
docs/juju.ggarch: records from the 4.1 DDL, plain labels, context records.

usage: build_page_schema.py MODELNAME DB tables.csv labels.json [context.csv] > model.ggarch
  DB          model | controller (which 4.1 DDL in experiments/e11)
  tables.csv  tables to scaffold (the page's own plus the context ones)
  labels.json {"table": "Plain\\nlabel"}  (every table that is drawn)
  context.csv tables drawn as context-record (other pages own them)
The scaffold drops quoted column names such as "key"; pass them in labels.json
under the key "__quoted__": {"table": ["key"]} and they are added as plain fields."""
import json, re, subprocess, sys, os
E = os.path.expanduser("~/git/misc/juju-reference/experiments/e11")
name, db, tables, labels = sys.argv[1:5]
context = set(sys.argv[5].split(",")) if len(sys.argv) > 5 else set()
lab = json.load(open(labels))
quoted = lab.pop("__quoted__", {})
sc = subprocess.run(["ggarch", "scaffold", f"{E}/{db}.ddl", "--db", db, "--tables", tables],
                    capture_output=True, text=True, check=True).stdout
for t, cols in quoted.items():
    for c in cols:
        pat = re.compile(r'(    %s \[type: record.*?fields \{\n)' % t, re.S)
        sc = pat.sub(lambda m: m.group(1) + f'        {c} [label: "{c}", type: "text", pk: true]\n', sc, 1)
for t, label in lab.items():
    sc, n = re.subn(r'(\n    %s \[type: )record(, label: )"[^"]*"' % t,
                    lambda m: m.group(1) + ("context-record" if t in context else "record") + m.group(2) + '"%s"' % label.replace("\n", "\\n"), sc, count=1)
    if n != 1: sys.exit(f"table {t} not found in the scaffold")
sc = sc.replace('model "Schema"', f'model "{name}"', 1)
print(sc.rstrip("\n"))
