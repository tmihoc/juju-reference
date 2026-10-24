#!/usr/bin/env python3
"""Mechanical checks of an entity reference page against page-recipe.md.
Reports; never edits. usage: check_page_rules.py <page.md> [...]"""
import re, sys

TITLES = ("database schema", "change streams", "calls", "and model migration", "workers", "credentials", "designations", "agent facades", "agent kinds")
GERUND = re.compile(r"^(Adding|Importing|Listing|Removing|Granting|Revoking|Creating|Updating|Deleting|Reading|Checking|Setting|Getting|Moving|Enabling|Disabling|Showing|Configuring|Migrating|Destroying|Upgrading|Connecting|Finding|Addressing|Reporting|Relaying|Bootstrapping|Making|Provisioning|Retrying|Reprovisioning|Reloading|Renaming|Requesting|Running|Canceling|Cancelling|Pruning|Consuming|Suspending|Entering|Writing|Changing|Registering|Logging|Rotating|Resuming|Claiming|Pinning|Unpinning|Uploading|Downloading|Resetting|Saving|Answering|Draining|Storing)\b")
BAD = [
    (r"\bis how\b", "opener 'is how': not a definition"),
    (r"\b(This|The) section (covers|describes|explains)\b", "metalanguage"),
    (r"\bauthoris|\bfavour|\bbehaviour|\bcolour\b|\bneighbour", "British spelling"),
    (r"\*Authority:\*", "label should be 'Caller'"),
    (r"\*Required access:\*", "label should be 'Caller'"),
    (r"\{ref\}`[^`]*command-juju-[^`]*`", "link to a CLI command page"),
    (r"\bthe (command-line client|CLI) offers\b", "CLI-led sentence"),
    (r"\*Rule:\* .{0,40}\bone (authority|access) requirement\b", "counting intro"),
    (r"\bhook tools?\b", "say 'hook command', not 'hook tool'"),
]
CLAUSE_AND = re.compile(r", and (the|a|an|each|every|it|its|they|their|no|there|that|this|these|those|[a-z-]+ (is|are|has|have|can|must|does|do|returns|gets|keeps|holds|names|stays|runs))\b")
OXFORD = re.compile(r"\b[A-Za-z-]+, [A-Za-z-]+ (and|or) [A-Za-z-]+")
VAGUE = re.compile(r"\b(batch|can carry)\b")
def sentence_rules(line):
    """Rules on prose with inline code removed (user, 2026-10-21 and 2026-10-20)."""
    prose = re.sub(r"`[^`]*`", "X", line)
    res = []
    for sent in re.split(r"(?<=[.:;])\s+", prose):
        m = CLAUSE_AND.search(sent)
        if m and ", " not in sent[:m.start()]:
            res.append("two clauses joined by ', and': split them or name the relation")
    if OXFORD.search(prose): res.append("list of three without the Oxford comma")
    if VAGUE.search(prose): res.append("vague word: batch or carry")
    return res

def main(path):
    lines = open(path).read().splitlines()
    out = []
    in_fence = False
    prev_text = ""      # last non-blank line outside a fence
    for n, line in enumerate(lines, 1):
        if line.startswith("```") or line.startswith("````"):
            in_fence = not in_fence if line.strip() not in ("```", "````") or in_fence else True
            if line.strip() in ("```", "````"): in_fence = False
            continue
        if in_fence: continue
        if line.startswith("## "):
            t = line[3:].lower()
            if not any(t.endswith(x) for x in TITLES):
                out.append((n, f"top-level title not in the map: {line}"))
        if line.startswith("### ") and any(w in " ".join(l for l in lines[:n] if l.startswith("## ")).lower() for w in ("operations", "calls")):
            if not GERUND.match(line[4:]):
                out.append((n, f"call subsection not a gerund nominal: {line}"))
        if not line.startswith("|"):
            for msg in sentence_rules(line): out.append((n, f"{msg}: {line.strip()[:90]}"))
        for pat, msg in BAD:
            if re.search(pat, line): out.append((n, f"{msg}: {line.strip()[:90]}"))
        if re.match(r"^- ", line) and not re.match(r"^- ", lines[n-2] if n >= 2 else ""):
            k = n - 2
            while k >= 0 and not lines[k].strip(): k -= 1
            if k >= 0 and not lines[k].startswith(("#", "(", ":", "|", "-", " ")) and not lines[k].rstrip().endswith(":"):
                out.append((n, "list not introduced by a colon at the end of the paragraph before it"))
        if re.match(r"^- ", line):
            p = prev_text
            if p.startswith("#") or p.startswith("(") or p == "" or p.startswith(":"):
                out.append((n, "bullet list with no intro sentence before it"))
        if line.strip():
            if not re.match(r"^\s*- ", line) or True:
                prev_text = line.strip() if not re.match(r"^\s*- ", line) else prev_text if prev_text and re.match(r"^\s*- ", prev_text) else prev_text
            if not re.match(r"^\s*- ", line): prev_text = line.strip()
    # first sentence after each ## heading must not start with a bullet
    return out
for p in sys.argv[1:]:
    res = main(p)
    print(f"{p}: {len(res)} finding(s)")
    for n, msg in res: print(f"  {n}: {msg}")
