#!/usr/bin/env python3
"""For each prep page, list the error strings in its rules-and-errors
sections and resolve them to Go constants and non-test raise sites."""
import os, re, shlex, subprocess, sys

REPO = "/home/dora/git/misc/juju-entity-ref"
PREP = os.environ["TMPDIR"] + "/prep"

def sh(cmd):
    return subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True,
                          text=True).stdout

cache = {}
def grep(pattern, flags="-rInF"):
    key = (pattern, flags)
    if key not in cache:
        cache[key] = sh(
            f"git grep {flags} --no-color -e {shlex.quote(pattern)} -- '*.go' "
            f"':!*_test.go' ':!*/mocks/*' | head -40").splitlines()
    return cache[key]

def errors_in(page):
    text = open(f"{PREP}/{page}.md").read().splitlines()
    out, sect = [], None
    for i, line in enumerate(text, 1):
        if re.match(r"#{2,3} .*rules and errors", line, re.I):
            sect = line.strip("# ")
        elif re.match(r"#{2,3} ", line):
            sect = None
        if sect:
            m = re.match(r"\s*[-*] \*\*`([^`]+)`\*?\*?", line)
            if m:
                out.append((i, sect, m.group(1)))
    return out

def layer(path):
    if "/state/" in path or "schema" in path:
        return "state"
    if "/service/" in path:
        return "service"
    if "apiserver" in path:
        return "apiserver"
    if "worker" in path:
        return "worker"
    return path.split("/")[0]

for page in sys.argv[1:]:
    print(f"\n=== {page}")
    for line, sect, err in errors_in(page):
        defs = [g for g in grep(f'"{err}"') if "errors" in g.split(":")[0]
                or "ConstError" in g]
        if not defs:
            # message may be formatted or lower-cased: loose search
            defs = grep(err)[:2]
            tag = "LOOSE" if defs else "NOT FOUND"
        else:
            tag = "defined"
        names = []
        for d in defs:
            m = re.search(r"(\w+)\s*=\s*(?:errors\.)?ConstError", d)
            if m:
                names.append(m.group(1))
        sites = []
        for n in names[:1]:
            for g in grep(rf"\b{n}\b", "-rInw"):
                p = g.split(":")
                if "errors.go" in p[0] or p[2].strip().startswith("//"):
                    continue
                sites.append(f"{p[0]}:{p[1]}")
        layers = sorted({layer(s) for s in sites})
        print(f"L{line:<4} [{sect[:28]}] {err!r}: {tag} "
              f"{names[:1]} sites={len(sites)} {layers}")
        for s in sites[:4]:
            print(f"        {s}")
        if tag != "defined":
            for d in defs[:2]:
                print(f"        ~ {d[:150]}")
