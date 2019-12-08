from PageObjectLibrary import PageObject
from selenium.webdriver.support.ui import Select
from robot.libraries.BuiltIn import BuiltIn


class RegisterPage(PageObject):
    PAGE_TITLE = "Login - My Store"
    PAGE_URL = "/index.php?controller=authentication&back=my-account#account-creation"

    _locators = {
        "gender_mr": "id=id_gender1",
        "firstname": "id=customer_firstname",
        "lastname": "id=customer_lastname",
        "password": "id=passwd",
        "days": "id=days",
        "months": "id=months",
        "years": "id=years",
        "address1": "id=address1",
        "city": "id=city",
        "state": "id=id_state",
        "zipcode": "id=postcode",
        "mobile": "id=phone_mobile",
        "submitAccount": "id=submitAccount"
    }

    def fill_out_customer_form(self):
        config = BuiltIn().get_variable_value("${CONFIG}")

        self.select_gender_mr()
        self.enter_first_name(config.new_customer_firstname)
        self.enter_last_name(config.new_customer_lastname)
        self.enter_password(config.new_customer_password)
        self.enter_day_of_birth(config.new_customer_day_of_birth)
        self.enter_month_of_birth(config.new_customer_month_of_birth)
        self.enter_year_of_birth(config.new_customer_year_of_birth)
        self.enter_address(config.new_customer_address)
        self.enter_city(config.new_customer_city)
        self.enter_state(config.new_customer_state)
        self.enter_zipcode(config.new_customer_zipcode)
        self.enter_mobile(config.new_customer_mobile)

    def enter_first_name(self, name):
        self.selib.input_text(self.locator.firstname, name)

    def select_gender_mr(self):
        self.selib.click_element(self.locator.gender_mr)

    def enter_last_name(self, name):
        self.selib.input_text(self.locator.lastname, name)

    def enter_password(self, password):
        self.selib.input_text(self.locator.password, password)

    def enter_day_of_birth(self, day):
        Select(self.selib.find_element(self.locator.days.split("=")[1])).select_by_value(day)

    def enter_month_of_birth(self, month):
        Select(self.selib.find_element(self.locator.months.split("=")[1])).select_by_value(month)

    def enter_year_of_birth(self, year):
        Select(self.selib.find_element(self.locator.years.split("=")[1])).select_by_value(year)

    def enter_date_of_birth(self, date):
        self.enter_day_of_birth(date.split("/")[2])
        self.enter_month_of_birth(date.split("/")[1])
        self.enter_year_of_birth(date.split("/")[0])

    def enter_address(self, address):
        self.selib.input_text(self.locator.address1, address)

    def enter_city(self, city):
        self.selib.input_text(self.locator.city, city)

    def enter_zipcode(self, zipcode):
        self.selib.input_text(self.locator.zipcode, zipcode)

    def enter_mobile(self, mobile):
        self.selib.input_text(self.locator.mobile, mobile)

    def enter_state(self, state):
        Select(self.selib.find_element(self.locator.state.split("=")[1])).select_by_value(state)

    def click_on_submit_account(self):
        with self._wait_for_page_refresh():
            self.selib.click_button(self.locator.submitAccount)
