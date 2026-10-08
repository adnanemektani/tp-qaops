#!/usr/bin/env bash
set -uo pipefail
: "${REQRES_API_KEY:?définir REQRES_API_KEY (clé gratuite sur app.reqres.in)}"
mkdir -p reports/api reports/ui
echo "== API (Newman) =="
newman run postman/Reqres_API.postman_collection.json -e postman/Reqres.postman_environment.json \
  --env-var apiKey="$REQRES_API_KEY" --reporters cli,json --reporter-json-export reports/api/newman.json
echo "== API (pytest) =="
(cd api-tests && pip install -q -r requirements.txt && pytest)
echo "== UI (Selenium) =="
(cd ui-tests && pip install -q -r requirements.txt && pytest)
