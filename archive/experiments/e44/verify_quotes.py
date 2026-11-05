"""E44: mechanical check that each evidence quote occurs within 3 lines of the
cited line in the 4.1 code copy. Reports failures; the truth of each answer is
checked by hand (see plan, E44 results)."""
import glob, json, os, sys
ROOT = "/tmp/juju-code-e44"
bad = 0; tot = 0
for f in sorted(glob.glob(os.path.expanduser("~/git/misc/juju-reference/experiments/judges/io/e44_q[12]_*.json"))):
    for q in json.load(open(f)):
        for e in q.get("evidence", []):
            tot += 1
            p = os.path.join(ROOT, e["file"])
            if not os.path.exists(p):
                print("MISSING FILE", os.path.basename(f), q["id"], e["file"]); bad += 1; continue
            lines = open(p, errors="replace").read().split("\n")
            ln = int(e["line"])
            win = "\n".join(lines[max(0, ln - 4): ln + 3])
            quote = e["quote"].strip()
            norm = lambda s: " ".join(s.split())
            if norm(quote) not in norm(win):
                print("QUOTE NOT FOUND", os.path.basename(f), q["id"], e["file"], ln, repr(quote[:80])); bad += 1
print("evidence items", tot, "failing", bad)
