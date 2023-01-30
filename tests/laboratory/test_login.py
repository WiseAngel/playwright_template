import pytest

import pytest_test.core.cheops_allure as cheops_report
import pytest_test.core.context as CTX
import pytest_test.utils.assert_utils as _assert
from pytest_test.pages.courses.login_page import LoginPage, LoginPageHelper
from pytest_test.pages.laboratory.lab_main_page import LabMainPage


@pytest.mark.xdist_group("lab")
@cheops_report.parent_suite("Лаборатория")
@cheops_report.suite("Логин пользователя")
@cheops_report.sub_suite("Логин пользователя")
@cheops_report.owner("Анна Буткевич")
@pytest.mark.extended_smoke
@pytest.mark.all_environments
class TestLogin:
    @pytest.mark.smoke
    @pytest.mark.monitoring
    @pytest.mark.sirius
    @pytest.mark.corp
    @pytest.mark.univ
    @cheops_report.title("Залогиниться пользователем с правами админа")
    def test_login_admin_user_sirius(self, browser, cluster):
        # Data
        user = CTX.USERS["admin"]

        # Arrange
        main_page = LabMainPage(browser, need_open=True, need_check=False, auto_authorize=False)
        login_page = LoginPage(browser, cluster)
        login_page_helper = LoginPageHelper()

        # Act

        login_page_helper.enter_credentials_sirius(login_page, user["email"], user["password"])
        main_page.wait_until_loader_disappeared()

        # Assert
        _assert.wait_true(main_page.is_sidebar_visible, "отображается сайдбар лаборатории",
                          "Должен отображаться сайдбар лаборатории")
        _assert.true(main_page.is_section_contest_present, "отображается раздел \"Олимпиады\"",
                     "Не отображается раздел \"Олимпиады\"")
        _assert.true(main_page.is_section_course_present, "отображается раздел \"Курсы\"",
                     "Не отображается раздел Курсы")
        _assert.true(main_page.is_section_environment_present, "отображается раздел \"Пространства\"",
                     "Не отображается раздел \"Пространства\"")
        _assert.true(main_page.is_section_users_present, "отображается раздел \"Пользователи\"",
                     "Не отображается раздел \"Пользователи\"")
        _assert.true(main_page.is_section_activity_present, "отображается раздел \"Мероприятия\"",
                     "Не отображается раздел \"Мероприятия\"")

    @pytest.mark.sirius
    @pytest.mark.corp
    @pytest.mark.univ
    @cheops_report.title("Залогиниться пользователем с правами только на курс")
    def test_login_user_with_course_rights_sirius(self, browser, cluster):
        # Data
        user = CTX.USERS["student"]

        # Arrange
        main_page = LabMainPage(browser, need_open=True, need_check=False, auto_authorize=False)
        login_page = LoginPage(browser, cluster)
        login_page_helper = LoginPageHelper()

        # Act
        login_page_helper.enter_credentials_sirius(login_page, user["email"], user["password"])
        main_page.wait_until_loader_disappeared()

        # Assert
        _assert.wait_true(main_page.is_sidebar_visible, "отображается сайдбар лаборатории",
                          "Должен отображаться сайдбар лаборатории")
        _assert.true(main_page.is_section_course_present, "отображается раздел \"Курсы\"",
                     "Не отображается раздел \"Курсы\"")
        _assert.false(main_page.is_additional_section_present, "не отображается ещё один раздел",
                      "Отображается еще один раздел")

    @pytest.mark.smoke
    @pytest.mark.monitoring
    @pytest.mark.cpm
    @cheops_report.title("Залогиниться пользователем с правами админа")
    def test_login_admin_user_cpm(self, browser, cluster):
        # Data
        user = CTX.USERS["admin"]
        email = user["email"]
        password = user["password"]

        # Arrange
        main_page = LabMainPage(browser, need_open=True, need_check=False, auto_authorize=False)
        login_page = LoginPage(browser, cluster, need_check=False)
        login_page_helper = LoginPageHelper()

        # Act
        login_page_helper.enter_credentials_cpm(login_page, email, password)
        main_page.wait_until_loader_disappeared()

        # Assert
        _assert.wait_true(main_page.is_sidebar_visible, "отображается сайдбар лаборатории",
                          "Должен отображаться сайдбар лаборатории")
        _assert.true(main_page.is_section_contest_present, "отображается раздел \"Олимпиады\"",
                     "Не отображается раздел \"Олимпиады\"")
        _assert.true(main_page.is_section_course_present, "отображается раздел \"Курсы\"",
                     "Не отображается раздел \"Курсы\"")
        _assert.true(main_page.is_section_environment_present, "отображается раздел \"Пространства\"",
                     "Не отображается раздел \"Пространства\"")
        _assert.true(main_page.is_section_users_present, "отображается раздел \"Пользователи\"",
                     "Не отображается раздел \"Пользователи\"")

    @pytest.mark.cpm
    @cheops_report.title("Залогиниться пользователем с правами только на курс")
    def test_login_user_with_course_rights_cpm(self, browser, cluster):
        # Data
        user = CTX.USERS["student"]
        email = user["email"]
        password = user["password"]

        # Arrange
        main_page = LabMainPage(browser, need_open=True, need_check=False, auto_authorize=False)
        login_page = LoginPage(browser, cluster, need_check=False)
        login_page_helper = LoginPageHelper()

        # Act
        login_page_helper.enter_credentials_cpm(login_page, email, password)
        main_page.wait_until_loader_disappeared()

        # Assert
        _assert.wait_true(main_page.is_sidebar_visible, "отображается сайдбар лаборатории",
                          "Должен отображаться сайдбар лаборатории")
        _assert.true(main_page.is_section_course_present, "отображается раздел \"Курсы\"",
                     "Не отображается раздел \"Курсы\"")
        _assert.false(main_page.is_additional_section_present, "не отображается ещё один раздел",
                      "Отображается еще один раздел")
