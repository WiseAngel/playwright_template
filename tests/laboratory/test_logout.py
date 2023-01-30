import pytest

import pytest_test.core.cheops_allure as cheops_report
import pytest_test.utils.assert_utils as _assert
from pytest_test.pages.courses.login_page import LoginPage
from pytest_test.pages.laboratory.lab_main_page import LabMainPage


@pytest.mark.xdist_group("lab")
@cheops_report.parent_suite("Лаборатория")
@cheops_report.suite("Выход из аккаунта пользователя")
@cheops_report.sub_suite("Выход из аккаунта пользователя")
@cheops_report.owner("Никита Свечкарёв")
@pytest.mark.logout
@pytest.mark.extended_smoke
@pytest.mark.all_environments
@pytest.mark.all_clusters
class TestLogout:
    @cheops_report.title("Выход из аккаунта пользователя")
    def test_logout_user(self, browser, cluster):
        # Arrange
        login_page = LoginPage(browser, cluster, need_check=False)
        lab_main_page = LabMainPage(browser, need_open=True, need_check=True)

        # Act
        lab_main_page.click_on_user_profile()
        lab_main_page.click_logout_button()

        # Assert
        _assert.wait_false(lab_main_page.is_sidebar_visible,
                           "не отображается сайдбар лаборатории, произошел выход из профиля",
                           "Не произошел выход из профиля, отображается сайдбар лаборатории")

        if cluster in ["sirius", "univ", "corp"]:
            _assert.wait_true(login_page.is_sirius_auth_form_title_visible,
                              "отображается форма авторизации",
                              "Не отображается форма авторизации")

            _assert.wait_true(login_page.is_login_input_displayed,
                              "поле ввода логина присутствует на странице",
                              "Поле ввода логина отсутствует на странице")

            _assert.wait_true(login_page.is_password_input_displayed,
                              "поле ввода пароля присутствует на странице",
                              "Поле ввода пароля отсутствует на странице")

            _assert.wait_true(login_page.is_submit_btn_displayed,
                              "кнопка отправки учётных данных присутствует на странице",
                              "Кнопка отправки учётных данных отсутствует на странице")

        if cluster == "cpm":
            _assert.wait_true(login_page.is_email_input_displayed,
                              "поле ввода логина присутствует на странице",
                              "Поле ввода логина отсутствует на странице")

            _assert.wait_true(login_page.is_get_login_code_inactive_btn_displayed,
                              "кнопка запроса кода авторизации присутсвует на странице",
                              "Кнопка запроса кода авторизации отсутствует на странице")
