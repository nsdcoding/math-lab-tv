#!/bin/bash
# Quick low-quality render for QA iteration: ./ql.sh s01_hook [s02_welcome ...]  (prints each scene's QA json)
cd "$(dirname "$0")"; mkdir -p build
for f in "$@"; do
  c=$(grep -oP 'class \K\w+(?=\(PBase\)|\(Base\))' scenes/$f.py | head -1)
  echo "$f:$c"
done | xargs -P 4 -I{} bash -c 'f=${1%%:*}; c=${1##*:}; manim -ql --disable_caching --media_dir build/media scenes/$f.py $c > build/lq_$f.log 2>&1 && echo "$c ok $(python3 -c "import json;d=json.load(open(\"build/qa/$c.json\"));print(len(d));[print(\"   \",x[\"kind\"],x[\"a\"],\"|\",x.get(\"b\"),x[\"times\"][:3]) for x in d[:12]]")" || { echo "$c FAILED"; tail -5 build/lq_$f.log; }' _ {}
