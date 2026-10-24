"""E43 scoring (criteria pre-registered in structure-discovery-plan.md, E43).

Mapping fixed in advance: own = character, of = leg, across = concept page
across entities, process = mechanism (E35 verdicts: character, leg, facet is
read as 'across' only for annotation, constraint, status as the E35 reading
named them concept pages; the E35 judge itself used character, leg, mechanism).
"""
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
IO = os.path.join(HERE, "..", "judges", "io")
new = {r["name"]: r for r in json.load(open(os.path.join(IO, "e43_out.json")))}
old = {r["name"]: r["verdict"] for r in json.load(open(os.path.join(IO, "e35_judge_out.json")))}
rule = json.load(open(os.path.join(HERE, "..", "e41", "e41_result.json")))
inp = [i["name"] for i in json.load(open(os.path.join(IO, "e43_input.json")))["items"]]
MAP = {"own": "character", "of": "leg", "process": "mechanism", "across": "facet"}
CONTROLS = ["cloud-instance", "unit-state", "relation-unit", "application-endpoint",
            "application-scale", "machine-placement"]

print("items", len(inp), "output", len(new), "missing", sorted(set(inp) - set(new)),
      "dups", len(inp) - len(set(inp)))
print("label counts:", dict(collections.Counter(r["label"] for r in new.values())))
print("name only notes:", sum("name only" in (r.get("note") or "").lower() for r in new.values()))
print("confidence:", dict(collections.Counter(r.get("confidence") for r in new.values())))

# E35 judge covered the 39 pages and the six controls
common = [n for n in inp if n in old]
print("\nitems with an E35 verdict:", len(common))
# facet/annotation/constraint/status were verdict 'leg' or 'character' in E35; compare
# on the three-way mapping, 'across' counted equal to E35 'leg' for annotation, constraint, status
CONCEPT = {"annotation", "constraint", "status"}


def same(n):
    """Registered mapping: own=character, of=leg, process=mechanism; across
    matches only the three concept pages named in E35 (annotation, constraint,
    status)."""
    a = new[n]["label"]
    if a == "across":
        return n in CONCEPT
    return MAP[a] == old[n]


agree = [n for n in common if same(n)]
print("(1) agreement with the E35 judge: %d of %d = %.1f%%" % (len(agree), len(common),
                                                                 100 * len(agree) / len(common)))
c = [n for n in CONTROLS if new[n]["label"] == "of"]
print("(2) negative controls labelled 'of': %d of 6 %s" % (len(c), [(n, new[n]["label"]) for n in CONTROLS]))

R = rule["rule"] if "rule" in rule else rule
sec = [g for g, r in R.items() if r["level"].startswith("section")]
pag = [g for g, r in R.items() if not r["level"].startswith("section")]
s_ag = [g for g in sec if g in new and new[g]["label"] == "of"]
p_ag = [g for g in pag if g in new and new[g]["label"] != "of"]
print("(3) E41 sections the judge calls 'of': %d of %d; E41 pages the judge does not call 'of': %d of %d" % (
    len(s_ag), len([g for g in sec if g in new]), len(p_ag), len([g for g in pag if g in new])))
print("    sections not 'of':", [(g, new[g]["label"]) for g in sec if g in new and new[g]["label"] != "of"])
print("    pages called 'of':", [(g, new[g]["label"], new[g].get("parent")) for g in pag if g in new and new[g]["label"] == "of"])

print("\n(4) items where this judge and the E35 judge differ:")
dif = [n for n in common if not same(n)]
for n in sorted(dif):
    r = new[n]
    print("  %-22s E35=%-10s new=%-8s parent=%-14s conf=%-6s rule=%s" % (
        n, old[n], r["label"], r.get("parent"), r.get("confidence"),
        R.get(n, {}).get("level", "-")))
json.dump(dict(agree=len(agree), n=len(common), controls=len(c), differ=sorted(dif)),
          open(os.path.join(HERE, "e43_result.json"), "w"), indent=1)
