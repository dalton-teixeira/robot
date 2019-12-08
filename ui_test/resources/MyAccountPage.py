from PageObjectLibrary import PageObject
from robot.libraries.BuiltIn import BuiltIn

class MyAccountPage(PageObject):

    PAGE_TITLE = "My account - My Store"
    PAGE_URL = "/index.php?controller=my-account"

    _locators = {
    }
