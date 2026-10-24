---
name: tabs-alphabetical
description: "Order tabs alphabetically in the docs (Kubernetes before Machines), on every page"
metadata:
  type: feedback
---

Order tab sets alphabetically, on the architecture page and on every other docs page: Kubernetes comes before Machines.

**Why:** the user decided this on 2026-09-30 while adding the Kubernetes and Machines slideshow tabs to the architecture page (they also noted Kubernetes is the more current platform).

**How to apply:** when adding or touching a tab set, sort the tabs by label. Existing tab sets on other pages were not changed in PR 4; only fix them when a change already touches that page. Related: [[juju-pr-workflow]].
