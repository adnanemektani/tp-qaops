from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from .base_page import BasePage


class FormyFormPage(BasePage):
    """Formulaire d'inscription Formy : /form"""

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    JOB_TITLE = (By.ID, "job-title")
    SELECT_EXPERIENCE = (By.ID, "select-menu")
    DATE = (By.ID, "datepicker")
    SUBMIT = (By.CSS_SELECTOR, "a.btn.btn-lg.btn-primary")
    ALERT_SUCCESS = (By.CSS_SELECTOR, "div.alert-success")

    def load(self, base_url):
        return self.open(f"{base_url}/form")

    def choose_education(self, n):
        self.click((By.ID, f"radio-button-{n}"))

    def choose_sex(self, n):
        self.click((By.ID, f"checkbox-{n}"))

    def select_experience(self, value):
        Select(self.visible(self.SELECT_EXPERIENCE)).select_by_value(str(value))

    def fill(self, first, last, job, date="01/01/2025"):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.JOB_TITLE, job)
        self.type(self.DATE, date)

    def submit(self):
        self.click(self.SUBMIT)

    def success_message(self):
        return self.text_of(self.ALERT_SUCCESS)


class FormyPopupPage(BasePage):
    """Alertes JS (/switch-window) et modale (/modal)."""

    ALERT_BTN = (By.ID, "alert-button")
    MODAL_BTN = (By.ID, "modal-button")
    CLOSE_BTN = (By.ID, "close-button")
    MODAL_TITLE = (By.ID, "exampleModalLabel")

    def trigger_alert(self, base_url):
        self.open(f"{base_url}/switch-window")
        self.click(self.ALERT_BTN)
        return self.wait.until(EC.alert_is_present())

    def open_modal(self, base_url):
        self.open(f"{base_url}/modal")
        self.click(self.MODAL_BTN)
        return self.visible(self.MODAL_TITLE)

    def close_modal(self):
        self.click(self.CLOSE_BTN)
        self.wait.until(EC.invisibility_of_element_located(self.MODAL_TITLE))


class FormyRadioPage(BasePage):
    """Boutons radio : /radiobutton"""

    def load(self, base_url):
        return self.open(f"{base_url}/radiobutton")

    def select(self, n):
        self.click((By.ID, f"radio-button-{n}"))

    def is_selected(self, n):
        return self.visible((By.ID, f"radio-button-{n}")).is_selected()


class FormyDropdownPage(BasePage):
    """Menu déroulant bootstrap : /dropdown"""

    BUTTON = (By.ID, "dropdownMenuButton")

    def load(self, base_url):
        return self.open(f"{base_url}/dropdown")

    def choose(self, link_text):
        self.click(self.BUTTON)
        self.click((By.LINK_TEXT, link_text))


class LoginPage(BasePage):
    """Login (the-internet.herokuapp.com/login) — Formy n'a pas de page login."""

    USER = (By.ID, "username")
    PWD = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH = (By.ID, "flash")

    def load(self, base_url):
        return self.open(f"{base_url}/login")

    def login(self, user, pwd):
        self.type(self.USER, user)
        self.type(self.PWD, pwd)
        self.click(self.SUBMIT)

    def flash(self):
        return self.text_of(self.FLASH)


class NestedFramesPage(BasePage):
    """Frames imbriquées (the-internet.herokuapp.com/nested_frames)."""

    def load(self, base_url):
        return self.open(f"{base_url}/nested_frames")

    def read_frame(self, *names):
        """Descend dans les frames (ex: 'frame-top','frame-middle') et lit le body."""
        self.driver.switch_to.default_content()
        for name in names:
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, name)))
        text = self.visible((By.TAG_NAME, "body")).text
        self.driver.switch_to.default_content()
        return text
