#!/bin/bash
# usage: shot.sh file.svg -> file.png (chromium snap reads only under $HOME)
f=$(readlink -f "$1"); w=$(grep -o 'viewBox="[^"]*"' "$f" | head -1 | tr -d '"' | awk '{print int($3)+20, int($4)+20}')
set -- $w
printf '<html><body style="margin:10px;background:white"><img src="file://%s"></body></html>' "$f" > "${f%.svg}.html"
chromium --headless --no-sandbox --disable-gpu --hide-scrollbars --screenshot="${f%.svg}.png" --window-size=$1,$2 "file://${f%.svg}.html" >/dev/null 2>&1
