#!/usr/bin/env python3
"""Per API method of a client facade: the access it requires, the block checks it
makes and the client-visible errors it returns (code and message), read from the
Go source. Not a parser: regular expressions over brace-matched function bodies,
good enough to give a writer the facts and a place to look, never the page text.

usage: extract_facade.py <facade dir relative to the 4.1 tree> [--tree PATH]
e.g.   extract_facade.py apiserver/facades/client/keymanager
Output: markdown. Every row cites file:line so a writer can check it."""
import os, re, sys, glob

TREE = os.path.expanduser("~/git/misc/juju-v2-preview")

def body_end(src, start):
    depth, i = 0, src.index("{", start)
    while i < len(src):
        c = src[i]
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: return i + 1
        i += 1
    return len(src)

def line_of(src, pos): return src.count("\n", 0, pos) + 1

def functions(path):
    src = open(path).read()
    out = []
    for m in re.finditer(r"^func \((\w+) \*?(\w+)\) (\w+)\(", src, re.M):
        end = body_end(src, m.start())
        out.append(dict(recv=m.group(2), name=m.group(3), file=os.path.relpath(path, TREE),
                        line=line_of(src, m.start()), body=src[m.start():end], src=src, off=m.start()))
    return out

ACCESS = [
    (r"HasPermission\(\s*ctx,\s*permission\.(\w+)", lambda m: f"permission {m.group(1)}"),
    (r"HasModelAdmin\(", lambda m: "model admin (or controller superuser)"),
    (r"HasPermission\(\s*ctx,\s*permission\.(\w+),\s*names\.New(\w+)Tag", lambda m: f"{m.group(1)} on {m.group(2)}"),
    (r"AuthClient\(\)", lambda m: "any authenticated client"),
]
BLOCKS = re.compile(r"\.(ChangeAllowed|RemoveAllowed|DestroyAllowed)\(")
ERR = re.compile(r"ParamsErrorf\(\s*(params\.\w+),\s*\"((?:[^\"\\]|\\.)*)\"", re.S)
HELPER = re.compile(r"\bapi\.(check\w+)\(|\b(\w+)\.(check\w+)\(")

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    d = args[0]
    files = [f for f in glob.glob(f"{TREE}/{d}/*.go") if not f.endswith("_test.go") and "mock" not in f]
    fns = [fn for f in files for fn in functions(f)]
    helpers = {fn["name"]: fn for fn in fns}
    print(f"# Facade `{d}`\n")
    for fn in fns:
        if not fn["name"][0].isupper(): continue
        body = fn["body"]
        errs = [(m.group(1), m.group(2).replace("\n", " "), fn["line"] + body[:m.start()].count("\n"))
                for m in ERR.finditer(body)]
        blocks = [(m.group(1), fn["line"] + body[:m.start()].count("\n")) for m in BLOCKS.finditer(body)]
        checks = []
        for m in re.finditer(r"\bapi\.(check\w+)\(", body):
            h = helpers.get(m.group(1))
            if h:
                acc = [lab(mm) for pat, lab in ACCESS for mm in re.finditer(pat, h["body"])]
                checks.append((m.group(1), fn["line"] + body[:m.start()].count("\n"), sorted(set(acc)), h["file"], h["line"]))
        direct = [lab(mm) for pat, lab in ACCESS for mm in re.finditer(pat, body)]
        if not (errs or blocks or checks or direct): continue
        print(f"## {fn['name']}  (`{fn['file']}:{fn['line']}`)\n")
        for name, ln, acc, hf, hl in checks:
            print(f"- access: `{name}` at line {ln} -> {', '.join(acc) or 'see helper'} (`{hf}:{hl}`)")
        for a in sorted(set(direct)): print(f"- access (inline): {a}")
        for b, ln in blocks: print(f"- block: `{b}` at line {ln}")
        for code, msg, ln in errs: print(f"- error: `{code}` \"{msg}\" (line {ln})")
        print()

main()
