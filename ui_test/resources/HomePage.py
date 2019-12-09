from PageObjectLibrary import PageObject


class HomePage(PageObject):

    PAGE_TITLE = "My Store"
    PAGE_URL = "/"

    _locators = {
            "tshirt": "xpath=//*[@id='block_top_menu']/ul/li/a[text() = 'T-shirts'][1]",
            "login": "class=login"
    }

    def click_on_tshirt(self):
        self.selib.click_link(self.locator.tshirt)

    def click_on_login(self):
        self.selib.click_link(self.locator.login)
