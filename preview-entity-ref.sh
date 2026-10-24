#!/bin/bash
# Live preview of the entity-reference branch on http://127.0.0.1:8001/
# Uses the venv of ../juju-pr4 (current sphinx, pinned ggarch).
cd /home/dora/git/misc/juju-entity-ref/docs || exit 1
rm -rf _build .sphinx/.doctrees
exec /home/dora/git/misc/docs-venv/bin/sphinx-autobuild -b dirhtml \
  --host 127.0.0.1 --port 8001 -j auto \
  . _build -c . -d .sphinx/.doctrees
