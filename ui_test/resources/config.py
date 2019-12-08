import os
import sys


class Config(object):

    def __init__(self):
        _here = os.path.dirname(__file__)

        sys.path.insert(0, os.path.abspath(os.path.join(_here, "..", "..")))
        sys.path.insert(0, os.path.abspath(os.path.join(_here)))

        self.root = os.path.abspath(os.path.join(_here, ".."))
        self.server = "http://automationpractice.com"
        self.browser = "Firefox"
        self.delay = 1

        self.new_customer_firstname = "customer"
        self.new_customer_lastname= "test"
        self.new_customer_password = "Pass1234!"
        self.new_customer_email = ""
        self.new_customer_day_of_birth = "1"
        self.new_customer_month_of_birth = "12"
        self.new_customer_year_of_birth = "1990"
        self.new_customer_address = "1234 street"
        self.new_customer_city = "DC"
        self.new_customer_state = "53"
        self.new_customer_zipcode = "20002"
        self.new_customer_mobile = "994163559"


    def __str__(self):
        return "<Config: %s>" % str(self.__dict__)


# This creates a variable that robot can see
CONFIG = Config()
