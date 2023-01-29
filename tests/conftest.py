from datetime import datetime

import allure
import pytest
from playwright.sync_api import Page

import core.context as ctx
import utils.os_manipulation as om
import utils.resource_loader as rl
from pages.playwright_home_page import PlaywrightHomePage
from pages.playwright_languages_page import PlaywrightLanguagesPage
from utils.data_manipulation import get_random_string

ENVS = ['dev', 'test', 'prod']


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args, request):
    user_agent = request.config.getoption('user_agent')
    return {
        **browser_context_args,
        'viewport': {
            'width': 1200,
            'height': 600,
        },
        'device_scale_factor': 1,
        'user_agent': user_agent,
        'locale': 'ru-RU'
    }


@pytest.fixture(scope='session')
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        'downloads_path': om.add_new_directory(ctx.DOWNLOAD_FOLDER),
        'headless': False
    }


@pytest.fixture(scope='function')
def playwright_home_page(page: Page) -> PlaywrightHomePage:
    return PlaywrightHomePage(page)


@pytest.fixture(scope='function')
def playwright_languages_page(page: Page) -> PlaywrightLanguagesPage:
    return PlaywrightLanguagesPage(page)


@pytest.fixture(scope='function')
def delete_files():
    yield
    om.delete_files_of_directory()


@pytest.fixture(scope='class')
def get_test_data():
    def _get_test_data(resource_name):
        return rl.get_test_data(resource_name)

    yield _get_test_data


@pytest.fixture(scope='class')
def get_root_test_data():
    def _get_test_data(resource_name):
        return rl.get_test_data(resource_name)

    yield _get_test_data


@pytest.fixture(scope='session', autouse=True)
def init_context(env):
    ctx.DOWNLOAD_FOLDER = f'{rl.get_environment_resource("download_options.json")["download_folder"]}_{get_random_string()}'
    ctx.URLS = rl.get_environment_resource('urls.json')[env]
    ctx.USERS = rl.get_environment_resource('users.json')[env]


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='dev',
                     help='Choose environment')
    parser.addoption('--user_agent', action='store', default='autotests',
                     help='Choose user-agent')
    parser.addoption('--logging', action='store', default='off',
                     help='Choose logging method')


@pytest.fixture(scope='session')
def env(request):
    env = request.config.getoption('env').lower()
    if env not in ENVS:
        raise pytest.UsageError(f'--env should be one of: {", ".join(ENVS)}')
    return env


@pytest.fixture(scope='function')
def user_agent(request):
    return request.config.getoption('user_agent').lower()


# @pytest.mark.hookwrapper(scope='session', autouse=True)
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call) -> None:
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#     if call.when == 'call':
#         if call.excinfo is not None and 'page' in item.funcargs:
#             page = item.funcargs['page']
#             screenshot_dir = Path('playwright-screenshots')
#             screenshot_dir.mkdir(exist_ok=True)
#             filename = str(screenshot_dir / f'{slugify(item.nodeid)}.png')
#             print(screenshot_dir)
#             print(filename)
#             page.screenshot(path=filename, full_page=False)
#             if filename:
#                 html = '<div><img src="%s" style="width:600px;height:228px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % filename
#                 extra.append(pytest_html.extras.html(html))
#     report.extra = extra
# # --html = report.html


@pytest.fixture(scope='function', autouse=True)
def test_time():
    start = datetime.now()
    with allure.step(f'Test started: {start.strftime("%H:%M:%S")}'):
        pass
    yield
    end = datetime.now()
    with allure.step(f'Test finished: {end.strftime("%H:%M:%S")}'):
        pass
