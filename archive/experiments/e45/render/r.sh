#!/bin/bash
# usage: r.sh "View name" -> render light svg + png under render/
cd ~/git/misc/juju-diagrams/docs && source ~/git/misc/docs-venv/bin/activate
n=$(echo "$1" | tr ' ()' '_')
O=~/git/misc/juju-reference/experiments/e45/render
ggarch render juju.ggarch --view "$1" --light --out "$O/$n" >/dev/null 2>&1 || ggarch render-seq juju.ggarch --view "$1" --light --out "$O/$n" 2>&1 | tail -2
ls $O/$n*.svg | while read f; do $O/shot.sh $f; echo ${f%.svg}.png; done
