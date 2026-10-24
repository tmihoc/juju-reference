---
name: check-every-docs-builder
description: "Docs changes that add or change a custom Sphinx node/directive (ggarch) must be verified with the latex builder too, because RTD builds a PDF and a failed PDF step fails the whole build"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 11bbabe8-762f-40b8-8557-35a16d46409d
  modified: 2026-09-30T15:38:56.454Z
---

Before pushing docs changes that touch a custom Sphinx extension, directive or node type (the ggarch `{ggarch}` figures), build with every builder Read the Docs runs: `dirhtml` AND `latex` (`python -m sphinx -T -b latex -D language=en . <out>`), plus text/markdown when the extension has visitors for them. A missing visitor in any builder fails the whole RTD build, and the published docs stop updating.

**Why:** on 2026-09-30 the RTD build of juju 4.1 (build 4504812) failed after PR 4 merged: HTML was fine, but `formats: - pdf` runs the latex builder, which raised `NotImplementedError: ... unknown node type: ggarch` because the extension had no latex visitor. My PR 4 verification had only run `dirhtml`. Fixed in ggarch 85546a9 and juju PR #23449.

**How to apply:** add `-b latex` to the pre-push docs checks. Baseline LaTeX errors (missing dashboard PNGs, one invalid character, `latexmk` exit 12 with `-f`) are tolerated by RTD; a Python exception is not. Fix renderer problems in ggarch (scratch clone when another session uses the shared checkout), push ggarch first, then bump the pin in `docs/requirements.txt`. Related: [[pr4-architecture-rewrite-state]], [[ggarch-session-notes]].
