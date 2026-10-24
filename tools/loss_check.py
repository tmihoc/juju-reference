#!/usr/bin/env python3
"""loss_check.py page: list prep sentences that are missing from the new
worktree page (whitespace and markdown-marker insensitive)."""
import os, re, sys

PREP = "/tmp/claude-1000/prep"
NEW = "/home/dora/git/misc/juju-entity-ref/docs/reference"

def norm(s):
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[*`_]", "", s)
    return s.strip().lower()

def shingles(n, k=4):
    w = re.findall(r"[a-z0-9<>/-]+", n)
    return [" ".join(w[i:i+k]) for i in range(max(0, len(w) - k + 1))]

def strip_fences(text):
    return re.sub(r"```\{ggarch\}.*?```", "", text, flags=re.S)

def units(text):
    text = strip_fences(text)
    out = []
    for para in re.split(r"\n\s*\n", text):
        para = re.sub(r"^\s*([-*]|\d+\.)\s+", "", para, flags=re.M)
        for s in re.split(r"(?<=[.!?:;])\s+", para.replace("\n", " ")):
            n = norm(s)
            if len(n) >= 25 and not n.startswith(("(", ":", "---")):
                out.append((s.strip(), n))
    return out

for page in sys.argv[1:]:
    prep = open(f"{PREP}/{page}.md").read()
    new = norm(strip_fences(open(f"{NEW}/{page}.md").read()))
    newset = set(shingles(new))
    missing = []
    for s, n in units(prep):
        sh = shingles(n)
        if not sh:
            continue
        hit = sum(1 for x in sh if x in newset) / len(sh)
        if hit < 0.6:
            missing.append(f"[{hit:.0%}] {s}")
    print(f"\n=== {page}: {len(missing)} prep sentences not found verbatim")
    for s in missing:
        print("  -", s[:230])
