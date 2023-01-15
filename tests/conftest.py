import os
from datetime import datetime
from pathlib import Path

import allure
import pytest

from playwright.sync_api import sync_playwright

import core.context as ctx
import utils.os_manipulation as om
import utils.resource_loader as rl
from utils.data_manipulation import get_random_string
from utils.logging import Logs

ENVS = ["dev", "test", "prod"]
LOGGING_TYPE = ["off", "fail", "all"]


@pytest.fixture(scope="function")
def run(request, browser_name):
    user_agent = request.config.getoption("user_agent")
    logging = request.config.getoption("logging")
    folder_download = om.add_new_directory(ctx.DOWNLOAD_FOLDER)

    if logging not in LOGGING_TYPE:
        raise pytest.UsageError(
            f"--logging should be one of: {', '.join(LOGGING_TYPE)}")

    print(f"{browser_name =}")
    with sync_playwright() as pw:
        browsers = {
            "chromium": pw.chromium,
            "firefox": pw.firefox,
            "webkit": pw.webkit
        }
        browser = browsers[browser_name].launch(
            downloads_path=folder_download,
            headless=False
        )
        context = browser.new_context(
            viewport={"width": 1600, "height": 1024},
            device_scale_factor=1,
            user_agent=user_agent,
            locale="ru-RU",
            # record_video_dir="",

        )

    try:
        yield context.new_page()

        # root_path = os.path.dirname(os.path.dirname(__file__))
        # path_to_logs_dir = os.path.join(root_path, "logs")
        # Path(path_to_logs_dir).mkdir(parents=True, exist_ok=True)
        # now = datetime.now()
        # now_logs = now.strftime("%H%M%S")
        # now_screen = now.strftime("%Y-%m-%d_%H-%M-%S")
        # log_name = request.node.name.replace(
        #     " ", "").encode("utf-8").decode("unicode-escape")
        # failed = request.node.rep_setup.failed or request.node.rep_call.failed
        # store_logs = logging == "all" or (logging == "fail" and failed)
        #
        # if store_logs:
        #     result = "FAILED" if failed else "PASSED"
        #     file_name = f"{result}_{now_logs}_{log_name}.json"
        #     Logs.get_network_logs(browser, path_to_logs_dir, file_name)
        #     Logs.get_browser_logs(browser, path_to_logs_dir, file_name)
        #     Logs.get_performance_logs(browser, path_to_logs_dir, file_name)
        #
        # if request.node.rep_setup.passed or request.node.rep_call.failed or request.node.rep_call.skipped or request.node.rep_setup.failed:
        #     attach_name = request.function.__name__ + "_" + now_screen
        #     allure.attach(
        #         browser.get_screenshot_as_png(),
        #         name=attach_name,
        #         attachment_type=allure.attachment_type.PNG
        #     )
    finally:
        context.close()
        browser.close()
        om.delete_files_of_directory()
        om.delete_directory(folder_download)
        print("\nquit browser..")


@pytest.fixture(scope="function")
def delete_files():
    yield
    om.delete_files_of_directory()


@pytest.fixture(scope="class")
def get_test_data():
    def _get_test_data(resource_name):
        return rl.get_test_data(resource_name)

    yield _get_test_data


@pytest.fixture(scope="class")
def get_root_test_data():
    def _get_test_data(resource_name):
        return rl.get_test_data(resource_name)

    yield _get_test_data


@pytest.fixture(scope="session", autouse=True)
def init_context(env):
    # ctx.USERS = rl.get_environment_resource("users.json")[env]
    # ctx.URLS = rl.get_environment_resource("urls.json")[env]
    # ctx.DOWNLOAD_FOLDER = f"{rl.get_environment_resource('download_options.json')['download_folder']}_{get_random_string()}"
    ctx.USERS = "user"
    ctx.URLS = "url"
    ctx.DOWNLOAD_FOLDER = f"{get_random_string()}"


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev",
                     help="Choose environment")
    parser.addoption("--user_agent", action="store", default="autotests",
                     help="Choose user-agent")
    parser.addoption("--logging", action="store", default="off",
                     help="Choose logging method")


@pytest.fixture(scope="session")
def env(request):
    env = request.config.getoption("env").lower()
    if env not in ENVS:
        raise pytest.UsageError(f"--env should be one of: {', '.join(ENVS)}")
    return env


@pytest.fixture(scope="function")
def user_agent(request):
    return request.config.getoption("user_agent").lower()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # TODO: not used
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def test_time():
    start = datetime.now()
    with allure.step(f"Тест запущен в: {start.strftime('%H:%M:%S')}"):
        pass
    yield
    end = datetime.now()
    with allure.step(f"Тест завершен в: {end.strftime('%H:%M:%S')}"):
        pass
