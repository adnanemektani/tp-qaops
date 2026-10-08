"""Configuration pytest : création du driver Chrome + capture d'écran sur échec."""
import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

FORMY_URL = os.getenv("FORMY_URL", "https://formy-project.herokuapp.com")
INTERNET_URL = os.getenv("INTERNET_URL", "https://the-internet.herokuapp.com")


@pytest.fixture(scope="session")
def formy_url():
    return FORMY_URL


@pytest.fixture(scope="session")
def internet_url():
    return INTERNET_URL


@pytest.fixture
def driver(request):
    options = Options()
    # HEADLESS=0 pour voir le navigateur en local ; par défaut headless (CI)
    if os.getenv("HEADLESS", "1") == "1":
        options.add_argument("--headless=new")
    if os.getenv("CHROME_BIN"):  # utilisé dans le pipeline GitLab (chromium apt)
        options.binary_location = os.environ["CHROME_BIN"]
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1366,900")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)  # on n'utilise que des attentes explicites
    request.node.driver = drv
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = getattr(item, "driver", None)
        if drv is not None:
            allure.attach(
                drv.get_screenshot_as_png(),
                name="capture_echec",
                attachment_type=allure.attachment_type.PNG,
            )
