#!/usr/bin/env python3
"""Count the documented client-visible error entries in the reference pages.

Method (reconstructed from session 89; reproduces its 950/670 at the
pre-ssh-server-fix tip e4eb027c82 exactly):

- An entry is every bold-backtick message (`**`...`**`) in an Errors list:
  from a `- *Errors:*` (or `- **Errors:**`) bullet up to the next heading.
- Error messages that appear on bullet lines OUTSIDE Errors lists count too
  (only the offer page has them: 7, quoted in Rules bullets).
- The six non-error resource-charm bullets (file, oci-image, store, upload,
  available, potential) are excluded.
- `--rows` additionally reports the per-page row number used in the PR text
  table (bold-backtick bullets that START the bullet; the table convention).
- Calls: `###` subsections under a `## ... calls` section only (scoped there
  on the user's call, 2026-10-21, session 95: schema subsections and list
  keys are not calls, and storage.md already carried five schema `###` inside
  the old all-`###` count); calls_with_errors counts the Errors bullets, one
  per call.

Usage: count_errors.py <worktree> [--rows]
Counted against the worktree HEAD. The count is anchored to the 4.1 tree
(/tmp/juju-41-tree); pass that path to count against the anchor tree.
"""
import re
import subprocess
import sys

# The preview links of pr-description.md (slug order as they appear).
TABLE = "/home/dora/git/misc/juju-reference/pr-description.md"
MSG = re.compile(r"\*\*`([^`]+)`\*\*")
NON_ERRORS = {"file", "oci-image", "store", "upload", "available", "potential"}


def slugs_from_table():
    seen, out = set(), []
    for line in open(TABLE):
        for m in re.finditer(r"\]\([^)]+/reference/([a-z0-9-]+)/\)", line):
            slug = m.group(1)
            if slug not in seen:
                seen.add(slug)
                out.append(slug)
    return out


def page(tree, slug):
    r = subprocess.run(
        ["git", "-C", tree, "show", f"HEAD:docs/reference/{slug}.md"],
        capture_output=True, text=True)
    return r.stdout


def counts(text):
    """Return (entries, row_number, operation-h3s, ops_with_errors)."""
    entries, row, ops, ops_err = [], 0, 0, 0
    in_errors, op = False, None
    parent = ""
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("- *Errors:*") or s.startswith("- **Errors:**"):
            in_errors = True
            ops_err += 1  # an Errors block is one per call
            continue
        if re.match(r"#{2,3} ", s):
            in_errors = False
            if s.startswith("## "):
                parent = s[3:].strip().lower()
            elif s.startswith("### ") and parent.endswith("calls"):
                op = s[4:].strip()
                ops += 1
            continue
        found = MSG.findall(ln)
        if in_errors and found:
            entries.extend(found)
        elif found and re.match(r"\s*[-*] ", ln):
            entries.extend(m for m in found if m not in NON_ERRORS)
        if re.match(r"\s*- \*\*`", ln):
            row += 1
    return entries, row, ops, ops_err


def main():
    tree = sys.argv[1]
    rows = "--rows" in sys.argv
    total, universe = 0, set()
    per_page = {}
    tot_ops = tot_ops_err = tot_rows = 0
    for s in slugs_from_table():
        e, row, ops, ops_err = counts(page(tree, s))
        per_page[s] = (len(e), row)
        total += len(e)
        universe.update(e)
        tot_ops += ops
        tot_ops_err += ops_err
        tot_rows += row
    print(f"entries={total} distinct={len(universe)} "
          f"calls={tot_ops} calls_with_errors={tot_ops_err}")
    if rows:
        for s, (e, r) in per_page.items():
            print(f"{s:24} entries={e:3} row={r:3}")


if __name__ == "__main__":
    main()
