#!/bin/bash
# usage: build.sh <worktree> <fmt> <log>
set -e
source ~/git/misc/docs-venv/bin/activate
cd "$1/docs"
rm -rf _build .sphinx/.doctrees
sphinx-build --keep-going -b "$2" . _build -w "$3" -c . -d .sphinx/.doctrees -j auto > "$3.out" 2>&1 || true
echo done $1 $2 >> "$3.out"
