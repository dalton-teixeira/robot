from PageObjectLibrary import PageObject
from robot.libraries.BuiltIn import BuiltIn


class HomePage(PageObject):

    PAGE_TITLE = "My Store"
    PAGE_URL = "/"

    _locators = {
        "login_link": "class=login",
    }

    def click_on_login(self):
        """Click the sign in link"""
        config = BuiltIn().get_variable_value("${CONFIG}")
        with self._wait_for_page_refresh():
            self.selib.click_link(self.locator.login_link)
