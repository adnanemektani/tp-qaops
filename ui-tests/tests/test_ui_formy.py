import allure
import pytest

from pages.formy_pages import (
    FormyDropdownPage,
    FormyFormPage,
    FormyPopupPage,
    FormyRadioPage,
    LoginPage,
    NestedFramesPage,
)

SUCCESS_MSG = "The form was successfully submitted!"


@allure.epic("QAOps - Gestion d'étudiants")
@allure.feature("UI - Formy / the-internet")
class TestUI:
    @allure.story("UI-01 Formulaire d'inscription complet")
    @pytest.mark.smoke
    def test_ui01_registration_form_success(self, driver, formy_url):
        page = FormyFormPage(driver).load(formy_url)
        page.fill("Sara", "Alaoui", "Etudiante QA")
        page.choose_education(2)       # College
        page.choose_sex(1)             # Male/Female selon la case
        page.select_experience(2)      # 2-4 ans
        page.submit()
        assert SUCCESS_MSG in page.success_message()
        assert driver.current_url.endswith("/thanks")

    @allure.story("UI-02 Formulaire - jeux de données multiples")
    @pytest.mark.parametrize(
        "first,last,job",
        [("Ahmed", "Benali", "Testeur"), ("Fatima", "El Idrissi", "Développeuse"), ("Yassine", "Tazi", "DevOps")],
    )
    def test_ui02_registration_form_datasets(self, driver, formy_url, first, last, job):
        page = FormyFormPage(driver).load(formy_url)
        page.fill(first, last, job)
        page.select_experience(3)
        page.submit()
        assert SUCCESS_MSG in page.success_message()

    @allure.story("UI-03 Boutons radio")
    def test_ui03_radio_buttons(self, driver, formy_url):
        page = FormyRadioPage(driver).load(formy_url)
        page.select(2)
        assert page.is_selected(2)
        assert not page.is_selected(1)
        page.select(3)
        assert page.is_selected(3)
        assert not page.is_selected(2)  # un seul bouton radio sélectionné à la fois

    @allure.story("UI-04 Liste déroulante")
    def test_ui04_dropdown_menu(self, driver, formy_url):
        page = FormyDropdownPage(driver).load(formy_url)
        page.choose("Autocomplete")
        assert driver.current_url.endswith("/autocomplete")

    @allure.story("UI-05 Alerte JavaScript")
    @pytest.mark.popup
    def test_ui05_js_alert(self, driver, formy_url):
        alert = FormyPopupPage(driver).trigger_alert(formy_url)
        assert alert.text.strip() != ""
        alert.accept()
        # après acceptation, plus d'alerte : la page reste utilisable
        assert driver.current_url.endswith("/switch-window")

    @allure.story("UI-06 Fenêtre modale")
    @pytest.mark.popup
    def test_ui06_modal(self, driver, formy_url):
        page = FormyPopupPage(driver)
        title = page.open_modal(formy_url)
        assert title.text == "Modal title"
        page.close_modal()

    @allure.story("UI-07 Login valide")
    @pytest.mark.smoke
    def test_ui07_login_success(self, driver, internet_url):
        page = LoginPage(driver).load(internet_url)
        page.login("tomsmith", "SuperSecretPassword!")
        assert "You logged into a secure area!" in page.flash()
        assert driver.current_url.endswith("/secure")

    @allure.story("UI-08 Login invalide")
    @pytest.mark.parametrize(
        "user,pwd,expected",
        [
            ("tomsmith", "mauvaispass", "Your password is invalid!"),
            ("inconnu", "SuperSecretPassword!", "Your username is invalid!"),
        ],
    )
    def test_ui08_login_failure(self, driver, internet_url, user, pwd, expected):
        page = LoginPage(driver).load(internet_url)
        page.login(user, pwd)
        assert expected in page.flash()
        assert driver.current_url.endswith("/login")

    @allure.story("UI-09 Frames imbriquées")
    @pytest.mark.frames
    def test_ui09_nested_frames(self, driver, internet_url):
        page = NestedFramesPage(driver).load(internet_url)
        assert page.read_frame("frame-top", "frame-left").strip() == "LEFT"
        assert page.read_frame("frame-top", "frame-middle").strip() == "MIDDLE"
        assert page.read_frame("frame-top", "frame-right").strip() == "RIGHT"
        assert page.read_frame("frame-bottom").strip() == "BOTTOM"
