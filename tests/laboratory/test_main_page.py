import pytest

import pytest_test.core.cheops_allure as cheops_report
import pytest_test.core.context as CTX
import pytest_test.utils.assert_utils as _assert
from pytest_test.pages.laboratory.courses.lab_course_page import LabCoursePage
from pytest_test.pages.laboratory.courses.lab_course_qa_page import LabCourseQAPage
from pytest_test.pages.laboratory.lab_main_page import LabMainPage


@pytest.mark.xdist_group("lab")
@cheops_report.parent_suite("Лаборатория")
@cheops_report.suite("Главная страница")
@cheops_report.sub_suite("Проверка элементов главной страницы")
@cheops_report.owner("Анна Буткевич")
@pytest.mark.extended_smoke
@pytest.mark.all_environments
@pytest.mark.sirius
class TestLabMainPage:
    @cheops_report.title("Админ. Проверка наличия основных элементов")
    def test_availability_of_elements_main_page(self, browser, cluster, env):
        # Arrange
        main_page = LabMainPage(browser)

        # Assert
        _assert.wait_true(main_page.is_block_statistic_present, "отображается статистика на главной",
                          "Не отображается статистика на главной")
        _assert.true(main_page.is_block_graph_present, "отображается график на главной",
                     "Не отображается график на главной")
        _assert.true(main_page.is_block_questions_present, "отображается блок с вопросами на главной",
                     "Не отображается блок с вопросами на главной")

    @cheops_report.title("Админ. Проверка перехода в вопросы курса")
    def test_user_with_full_rights_can_go_to_question_from_main_page(self, browser, cluster, env):
        # Arrange
        main_page = LabMainPage(browser)

        # Act
        main_page.wait_until_questions_present()
        main_page.click_first_question()
        course_qa_page = LabCourseQAPage(browser, "", need_open=False, need_check=False)
        name_section = course_qa_page.get_text_active_section()

        # Assert
        _assert.equals(name_section, "Вопросы", "открылась страница \"Лаб.Курсы.Вопросы\"",
                       "Не открылась страница \"Лаб.Курсы.Вопросы\"")

    @cheops_report.title("Админ. Проверка перехода в курс с блока вопросов")
    def test_user_with_full_rights_can_go_to_course_from_question_main_page(self, browser, cluster, env):
        # Arrange
        main_page = LabMainPage(browser)

        # Act
        main_page.wait_until_questions_present()
        main_page.click_first_course()
        course_page = LabCoursePage(browser, "", need_open=False, need_check=False)

        # Assert
        _assert.wait_true(course_page.is_checked_page, "открылась страница \"Лаб.Курсы\"",
                          "Не открылась страница Лаб.Курсы")

    @cheops_report.title("Админ с правами на вопросы курса. Проверка перехода в вопросы курса")
    def test_user_with_part_rights_can_go_to_question(self, browser):
        # Data
        user_token = CTX.USERS["student"]["token"]

        # Arrange
        main_page = LabMainPage(browser, token=user_token)

        # Act
        main_page.wait_until_questions_present()
        main_page.click_first_question()
        course_qa_page = LabCourseQAPage(browser, "", need_open=False, need_check=False)
        name_section = course_qa_page.get_text_active_section()

        # Assert
        _assert.equals(name_section, "Вопросы", "открылась страница \"Лаб.Курсы.Вопросы\"",
                       "Не открылась страница \"Лаб.Курсы.Вопросы\"")
