#!/usr/bin/env bash
# Usage : REQRES_API_KEY=xxx ./run_jmeter.sh [users] [ramp] [loops]
set -euo pipefail
USERS=${1:-50}; RAMP=${2:-10}; LOOPS=${3:-10}
OUT=../reports/performance
rm -rf "$OUT" && mkdir -p "$OUT"
jmeter -n -t reqres_load_test.jmx \
  -Jusers="$USERS" -Jramp="$RAMP" -Jloops="$LOOPS" -Japikey="${REQRES_API_KEY:?définir REQRES_API_KEY}" \
  -l "$OUT/results.jtl" -e -o "$OUT/html-report"
echo "Rapport HTML : $OUT/html-report/index.html"
