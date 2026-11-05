# Audit pilot: the deleted `reference/metadata.md` (2026-11-05)

First use of the refactor mode (`method/docs-decision-procedure.md`, section "Auditing an existing change") on the largest single removal in PR #23661. Base `e5db99d585`, PR head `48ef1fca17`. Source reads only; no live run.

## What the PR did

`reference/metadata.md` ("Simplestreams metadata", 200 lines) was deleted. `reference/image-metadata.md` was added and `redirects.txt` maps `reference/metadata` to it; the label `(metadata)` moved to the new page, so existing links resolve (address preserved).

The old page had six parts: why Juju needs metadata at bootstrap (an image ID and an agent binary URL), the simplestreams format, the basic workflow, image metadata contents, agent binary metadata contents, configuration, and deploying private clouds. The new page is a different subject: the image metadata **records and their three calls** (list, save, delete) and the effect of model migration.

## Statement classification

| Old content | Where it is now | Class |
|---|---|---|
| Why bootstrap needs an image and an agent binary location; what simplestreams is | Not on the new page; partly in `howto/manage-metadata.md` and `howto/.../set-up-your-juju-deployment-offline.md` | Moved in part |
| Image product ID format (`com.ubuntu.cloud:server:<version>:<arch>`) and daily variant | Nowhere in the PR's docs | Dropped |
| Agent binary product ID format (`com.ubuntu.juju:<os>:<arch>`), content type | Nowhere | Dropped |
| Index and product file directory layout (`streams/v1/index.(s)json`, `product-*.(s)json`, `<stream>/tools-*.tar.gz`) | Nowhere | Dropped |
| `agent-metadata-url` and `image-metadata-url` configuration | The generated model configuration keys; one fewer page mentions the agent key | Moved in part |
| Private-cloud deployment steps | `howto/manage-metadata.md`, offline set-up how-to | Task, kept as how-to |

## Source check of the dropped facts (4.1)

- Image product IDs of the form `com.ubuntu.cloud:server:<version>:<arch>` are still in use (`environs/imagedownloads/testdata`).
- The default index path in 4.1 is `streams/<version>/index2`, with `index` as the legacy path (`environs/simplestreams/simplestreams.go:332-333`). The old text says `index.(s)json`, so the old statement is **partly out of date**, not simply right.
- Whether the agent-binary product ID form is still `com.ubuntu.juju:<os>:<arch>` was not confirmed in this pass.

## Verdict (procedure output)

| Item | Action | Basis | Confidence |
|---|---|---|---|
| Deleting the page and redirecting | Keep the redirect and the label | R15 satisfied for the URL; the label resolves | Determined |
| The simplestreams data layout and product ID formats | **Restore, corrected**, at an owner for "the metadata Juju reads at bootstrap" (not on `image-metadata.md`, whose subject is the records and calls) | Quantity regression: a unique reference fact for operators setting up private clouds and offline deployments, absent from the whole set; the old text needs the index-path correction before it goes back | Open(Q1): confirm the audience question and the 4.1 layout against the source |
| The page that now holds the label `(metadata)` | Check that its lede does not claim to be the simplestreams reference | The old label was about the simplestreams system, and a link to it now lands on records and calls | Determined (check) |

## What this shows about the audit

A statement-level before and after comparison finds regressions that a review of the new pages alone cannot: nothing on `image-metadata.md` is wrong, and the loss is in what is absent. The procedure needs its refactor mode for this, which it now has.
