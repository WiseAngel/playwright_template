import re

from playwright.sync_api import expect


class TestFoo:
    def test_foo(self, run):
        run.goto("https://playwright.dev/")

        # Expect a title "to contain" a substring.
        expect(run).to_have_title(re.compile("Playwright"))

        # create a locator
        get_started = run.get_by_role("link", name="Get started")

        # Expect an attribute "to be strictly equal" to the value.
        expect(get_started).to_have_attribute("href", "/docs/intro")

        # Click the get started link.
        get_started.click()

        # Expects the URL to contain intro.
        expect(run).to_have_url(re.compile(".*intro"))
