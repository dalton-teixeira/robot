from PageObjectLibrary import PageObject


class MyAccountPage(PageObject):

    PAGE_TITLE = "My account - My Store"
    PAGE_URL = "/index.php?controller=my-account"

    _locators = {
    }
