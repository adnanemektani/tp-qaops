# TP QAOps – Automatisation des tests et qualité logicielle

Projet de fin de module (Université Hassan II – FSAC) : tests UI, API, performance, sécurité et pipeline CI/CD.

## Structure
| Dossier | Contenu |
|---|---|
| `ui-tests/` | Selenium + pytest + Allure (Page Object) – 9 scénarios UI + test XSS |
| `api-tests/` | Tests API pytest/requests (Reqres) |
| `postman/` | Collection Postman + environnement (exécution Newman) |
| `performance/` | Plan JMeter (50 utilisateurs GET/POST) + script |
| `security/` | Script OWASP ZAP + charges utiles XSS |
| `docs/` | Plan de tests (Word) et rapport final (Word) |
| `reports/` | Rapports générés à l'exécution |
| `.gitlab-ci.yml` | Pipeline API → UI → Performance → Sécurité → Notification |

## Prérequis
Python 3.12, Chrome, Node 20 (Newman), JMeter 5.x, Docker (ZAP).
**Reqres exige une clé API gratuite** : https://app.reqres.in puis `export REQRES_API_KEY=...`

## Exécution rapide
```bash
./run_all.sh          # API + UI (local)
cd performance && REQRES_API_KEY=xxx ./run_jmeter.sh 50 10 10
cd security && ./run_zap.sh
```
Rapport Allure : `allure serve reports/ui/allure-results`

## Remarques
- Formy n'a ni login ni iframe : ces scénarios utilisent https://the-internet.herokuapp.com.
