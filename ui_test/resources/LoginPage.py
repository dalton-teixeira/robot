from PageObjectLibrary import PageObject
from robot.libraries.BuiltIn import BuiltIn
from datetime import datetime
import time


class LoginPage(PageObject):

    PAGE_TITLE = "Login - My Store"
    PAGE_URL = "/index.php?controller=authentication&back=my-account"

    _locators = {
        "email_create": "id=email_create",
        "create_account": "id=SubmitCreate",
    }

    def create_new_account(self):
        config = BuiltIn().get_variable_value("${CONFIG}")
        now = datetime.now()
        email_create = "{}@test.com".format(now.strftime("%Y%d%m%H%M%S"))
        config.new_customer_email = email_create
        self.enter_email_create(email_create)
        self.click_the_create_account_button()

    def enter_email_create(self, email):
        self.selib.input_text(self.locator.email_create, email)

    def click_the_create_account_button(self):
        self.selib.click_button(self.locator.create_account)
