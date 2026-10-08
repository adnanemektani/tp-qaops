"""Test de sécurité simple : injection XSS dans le formulaire Formy.

Le formulaire Formy n'enregistre ni ne réaffiche les données saisies ; le test vérifie
qu'aucun script injecté ne s'exécute (pas d'alerte JS) après soumission.
"""
import allure
import pytest
from selenium.common.exceptions import NoAlertPresentException

from pages.formy_pages import FormyFormPage

PAYLOADS = [
    "<script>alert('xss1')</script>",
    "\"><img src=x onerror=alert('xss2')>",
    "'><svg/onload=alert('xss3')>",
]


@allure.epic("QAOps - Gestion d'étudiants")
@allure.feature("Sécurité - XSS")
@pytest.mark.parametrize("payload", PAYLOADS)
def test_sec01_xss_not_executed(driver, formy_url, payload):
    page = FormyFormPage(driver).load(formy_url)
    page.fill(payload, payload, payload)
    page.submit()
    try:
        alert = driver.switch_to.alert
        alert.dismiss()
        pytest.fail("Une alerte JS a été déclenchée : XSS exécuté")
    except NoAlertPresentException:
        pass
    # la charge utile ne doit pas être réinjectée telle quelle dans le HTML de la page
    assert payload not in driver.page_source
