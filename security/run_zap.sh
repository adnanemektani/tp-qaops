#!/usr/bin/env bash
# Scan baseline OWASP ZAP de Formy (nécessite Docker).
# Usage : ./run_zap.sh [url-cible]
set -uo pipefail
TARGET=${1:-https://formy-project.herokuapp.com}
OUT="$(cd "$(dirname "$0")/.." && pwd)/reports/security"
mkdir -p "$OUT" && chmod 777 "$OUT"
docker run --rm -v "$OUT":/zap/wrk:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t "$TARGET" -r zap_report.html -J zap_report.json -w zap_report.md -I
echo "Rapports : $OUT/zap_report.html | zap_report.json | zap_report.md"
