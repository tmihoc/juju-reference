---
name: project-skeleton-research
description: Where the reference-page skeleton research stands (session 78) and where its summary lives
metadata:
  type: project
---

The reference-page skeleton is being treated as a scientific study of the Juju software (derive the parts from artifact classes in the code, compare with the docs), not from sentence classification. Read `~/git/misc/juju-reference/skeleton-research-summary.md` first in a new chat; it maps the experiments (E7 to E11), the evidence, open items and file locations.

**Why:** the user wants a skeleton that is both explanatory and predictive, grounded in the shape of the software; human raters are ruled out; only docs/ material counts (user-facing facts, or spanning facts a contributor needs), so artifacts are tiered by exposure (client-facing, cross-process, internal).

**How to apply:** do not freeze or roll out the skeleton yet; PR #23451 (layered form) will not land. Next tests are in the summary (out-of-sample recall against upstream human-written pages, version stability 4.0.15 against 4.1, a generator over held-out domains). See [[project-actor-part-template]], [[project-entity-reference-form]].

**Status at the end of session 78:** E12 to E14 done (controller storage as a topic; claim recall against old pages; close scrutiny: 29% of conceptual claims fail). Next: version stability (4.0.15 against 4.1 DDL), held-out generator, claim-gate prototype. Resume from `~/git/misc/juju-reference/RESUME.md`.
