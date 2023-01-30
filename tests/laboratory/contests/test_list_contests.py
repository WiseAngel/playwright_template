import pytest

import core.cheops_allure as cheops_report
import utils.assert_utils as _assert
import utils.resource_loader as RL
from pages.laboratory.contests.lab_list_contests import LabListContestPage, LabListContestPageHelper
from pages.laboratory.lab_main_page import LabMainPage
from pages.virtual.menu_plus_page import MenuPlusPage, MenuPlusHelper
from pages.virtual.popup_warning_confirm import WarningPopupPage, WarningPopupHelper


@pytest.mark.xdist_group("lab")
@cheops_report.parent_suite("Лаборатория")
@cheops_report.suite("Олимпиады")
@cheops_report.sub_suite("Список олимпиад")
@cheops_report.owner("Анна Буткевич")
@pytest.mark.smoke
@pytest.mark.extended_smoke
@pytest.mark.all_environments
@pytest.mark.all_clusters
class TestLabListContestPage:
    @cheops_report.title("Добавление новой олимпиады")
    def test_addition_contest(self, browser, delete_contest_by_name):
        # Data
        name_contest = "Auto. Смоук тест"
        delete_contest_by_name(name_contest)

        # Arrange
        LabMainPage(browser)
        contest_list_page = LabListContestPage(browser)
        helper = LabListContestPageHelper()
        menu_plus = MenuPlusPage(browser)
        menu_helper = MenuPlusHelper()

        # Act
        id_first_contest = contest_list_page.get_text_id_contest(1)
        menu_helper.open_menu_plus(menu_plus)
        menu_helper.open_popup_for_add_element(menu_plus, "contests_list", "Олимпиаду")
        menu_helper.fill_input_field(menu_plus, name_contest)
        helper.confirm_add_contest(contest_list_page, id_first_contest, 1)

        # Assert
        _assert.equals(contest_list_page.get_text_name_contest(1), name_contest,
                       "добавилась олимпиада", "Не добавилась олимпиада")

    # @cheops_report.title("Импорт олимпиады")
    # def test_import_contest(self, browser, delete_contest_by_name):
    #     # Data
    #     file = RL.get_path_static_resource("contest_smoke.zip")
    #     name_contest = "Auto. Смоук тест"
    #     delete_contest_by_name(name_contest)
    #
    #     # Arrange
    #     LabMainPage(browser)
    #     contest_list_page = LabListContestPage(browser)
    #     helper = LabListContestPageHelper()
    #     menu_plus = MenuPlusPage(browser)
    #     menu_helper = MenuPlusHelper()
    #
    #     # Act
    #     id_first_contest = contest_list_page.get_text_id_contest(1)
    #     menu_helper.open_menu_plus(menu_plus)
    #     menu_helper.open_popup_for_add_element(menu_plus, "contests_list", "Загрузить олимпиаду из архива")
    #     menu_plus.wait_until_popup_present()
    #     helper.upload_archive_contest(contest_list_page, file, id_first_contest, 1)
    #
    #     # Assert
    #     _assert.equals(contest_list_page.get_text_name_contest(1), name_contest,
    #                    "добавилась олимпиада", "Не добавилась олимпиада")
    #
    # @cheops_report.title("Фильтрация олимпиад")
    # def test_filters_contests(self, browser):
    #     # Arrange
    #     LabMainPage(browser)
    #     contest_list_page = LabListContestPage(browser)
    #     helper = LabListContestPageHelper()
    #
    #     # Act
    #     is_selected_filter_all = contest_list_page.is_selected_filter_present("Все")
    #     helper.select_filter_contests(contest_list_page, "Сейчас")
    #     is_selected_filter_ongoing = contest_list_page.is_selected_filter_present("Сейчас")
    #     is_showed_ongoing_contests = contest_list_page.is_icon_contest_present("Сейчас")
    #     helper.select_filter_contests(contest_list_page, "В работе")
    #     is_selected_filter_actual = contest_list_page.is_selected_filter_present("В работе")
    #     helper.select_filter_contests(contest_list_page, "Завершённые")
    #     is_selected_filter_finish = contest_list_page.is_selected_filter_present("Завершённые")
    #     is_showed_finish_contests = contest_list_page.is_icon_contest_present("Завершённые")
    #     helper.select_filter_contests(contest_list_page, "Архив")
    #     is_selected_filter_archive = contest_list_page.is_selected_filter_present("Архив")
    #     is_showed_archive_contests = contest_list_page.is_icon_contest_present("Архив")
    #
    #     # Assert
    #     _assert.equals(is_selected_filter_all, True, "по умолчанию выбран фильтр \"Все\"",
    #                    "Не выбран фильтр \"Все\" по умолчанию")
    #     _assert.equals(is_selected_filter_ongoing, True, "выделен фильтр \"Сейчас\"", "Не выделен фильтр \"Сейчас\"")
    #     _assert.equals(is_showed_ongoing_contests, True, "в выборке отображаются только олимпиады в статусе \"Сейчас\"",
    #                    "В выборке отображаются не только олимпиады в статусе \"Сейчас\"")
    #     _assert.equals(is_selected_filter_actual, True, "выделен фильтр \"В работе\"", "Не выделен фильтр \"В работе\"")
    #     _assert.equals(is_selected_filter_finish, True, "выделен фильтр \"Завершённые\"",
    #                    "Не выделен фильтр \"Завершённые\"")
    #     _assert.equals(is_showed_finish_contests, True,
    #                    "в выборке отображаются только олимпиады в статусе \"Завершённые\"",
    #                    "В выборке отображаются не только олимпиады в статусе \"Завершённые\"")
    #     _assert.equals(is_selected_filter_archive, True, "выделен фильтр \"Архив\"", "Не выделен фильтр \"Архив\"")
    #     _assert.equals(is_showed_archive_contests, True, "в выборке отображаются только олимпиады в статусе \"Архив\"",
    #                    "В выборке отображаются не только олимпиады в статусе \"Архив\"")
    #
    # @cheops_report.title("Удаление олимпиады с помощью топ меню")
    # def test_delete_contest_by_top_menu(self, browser, lab_smt_api, delete_contest_by_name):
    #     # Data
    #     contest_file = RL.get_static_resource("contest_smoke.zip")
    #     name_contest = "Auto. Смоук тест"
    #     delete_contest_by_name(name_contest)
    #
    #     # Arrange
    #     contest_id = lab_smt_api.import_contest(contest_file).get("success")
    #     LabMainPage(browser)
    #     contest_list_page = LabListContestPage(browser)
    #     helper = LabListContestPageHelper()
    #     warning_popup = WarningPopupPage(browser)
    #     warning_helper = WarningPopupHelper()
    #
    #     # Act
    #     item_contest = contest_list_page.get_item_contest_by_id(contest_id)
    #     helper.open_top_menu_contest(contest_list_page, item_contest)
    #     contest_list_page.click_btn_delete_contest()
    #     warning_helper.set_checkboxes_and_continue_of_warning(warning_popup)
    #     helper.wait_until_content_present(contest_list_page)
    #
    #     # Assert
    #     _assert.not_contains(contest_id, contest_list_page.get_list_ids_contests(),
    #                          "удалилась олимпиада", "Не удалилась олимпиада")
    #
    # @pytest.mark.parametrize("search_type", ("name", "id"))
    # @cheops_report.title("Поиск олимпиады")
    # def test_search_contest_by_name(self, browser, search_type):
    #     # Data
    #     cheops_report.Dynamic.title(f"Поиск олимпиады по {search_type}")
    #
    #     # Arrange
    #     LabMainPage(browser)
    #     contest_list_page = LabListContestPage(browser)
    #     helper = LabListContestPageHelper()
    #
    #     # Act
    #     if search_type == "name":
    #         search_text = contest_list_page.get_text_name_contest(1)
    #     else:
    #         search_text = contest_list_page.get_text_id_contest(1)
    #     helper.search_contest(contest_list_page, search_type, search_text)
    #
    #     # Assert
    #     _assert.equals(contest_list_page.is_contest_searched(search_type, search_text), True,
    #                    "сработал поиск", "Не сработал поиск")
    #
    # @pytest.mark.parametrize("contest", (
    #         "contest_unchecked",
    #         "contest_published",
    #         "contest_checked",
    #         "contest_finished",
    #         "contest_archived"
    # ))
    # @cheops_report.title("Доступный функционал контекстного меню")
    # def test_context_menu_contest(self, browser, contest, get_test_data):
    #     # Data
    #     cheops_report.Dynamic.title(f"Доступный функционал контекстного меню - {contest}")
    #     contest_id = get_test_data(f"laboratory.contest_check_functionality.ids_{contest}")["contest_id"]
    #     points_context_menu = {
    #         "contest_published": ["Опубликовать результаты", "Опубликована", "Экспортировать", "Настройки",
    #                               "Удалить олимпиаду"],
    #         "contest_checked": ["Опубликовать", "Экспортировать", "Настройки", "Удалить олимпиаду"],
    #         "contest_finished": ["Опубликовать результаты", "Архивировать олимпиаду", "Экспортировать", "Настройки",
    #                              "Удалить олимпиаду"],
    #         "contest_archived": ["Извлечь из архива", "Экспортировать", "Настройки", "Удалить олимпиаду"],
    #         "contest_unchecked": ["Опубликовать", "Экспортировать", "Суперсессия", "Настройки", "Удалить олимпиаду"]
    #     }
    #     points_context_sub_menu = ["Список заданий", "Выгрузить задания", "Выгрузить всю олимпиаду"]
    #
    #     # Arrange
    #     LabMainPage(browser)
    #     contest_list_page = LabListContestPage(browser, tags="test", filter_contests=f"id_{str(contest_id)}")
    #     helper = LabListContestPageHelper()
    #
    #     # Act
    #     helper.open_context_menu_contest(contest_list_page, 1)
    #     context_menu = contest_list_page.get_names_item_context_menu()
    #     helper.open_submenu_export(contest_list_page)
    #     context_sub_menu = contest_list_page.get_names_item_context_submenu()
    #
    #     # Assert
    #     _assert.equals(context_menu, points_context_menu[contest], "отображаются доступные пункты контекстного меню",
    #                    "Не отображаются доступные пункты контекстного меню")
    #     _assert.equals(context_sub_menu, points_context_sub_menu, "отображаются доступные пункты меню экспорта",
    #                    "Не отображаются доступные пункты меню экспорта")
