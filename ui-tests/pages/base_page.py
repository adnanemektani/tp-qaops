from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Page de base : attentes explicites + actions communes."""

    TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def open(self, url):
        self.driver.get(url)
        return self

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.clickable(locator).click()

    def type(self, locator, text):
        el = self.visible(locator)
        el.clear()
        el.send_keys(text)

    def text_of(self, locator):
        return self.visible(locator).text
