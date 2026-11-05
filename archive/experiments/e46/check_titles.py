"""E46 (read-only): which of the proposed section titles appear on the six
pilot pages, and which headings the pilots use that the map lacks.
Usage: python check_titles.py  (reads ~/git/misc/juju-v2-preview/docs/reference)"""
import os, re
D = os.path.expanduser("~/git/misc/juju-v2-preview/docs/reference")
MAP = ["data model", "change streams", "operations", "and model migration"]
for f in ("machine", "controller", "model", "access", "ssh-key", "agent"):
    heads = [(len(m.group(1)), m.group(2)) for m in re.finditer(r"^(#+) (.*)$", open(f"{D}/{f}.md").read(), re.M)]
    h2 = [t for n, t in heads if n == 2]
    ent = heads[0][1]
    suffix = [t[len(ent):].strip().lower() if t.lower().startswith(ent.lower()) else t.lower() for t in h2]
    hit = [m for m in MAP if any(x == m or x.endswith(m) for x in suffix)]
    extra = [x for x in suffix if not any(x == m or x.endswith(m) for m in MAP)]
    print(f"{f:11} mapped {hit}  not in map {extra}")
