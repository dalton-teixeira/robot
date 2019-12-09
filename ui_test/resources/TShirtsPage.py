from PageObjectLibrary import PageObject


class TShirtsPage(PageObject):

    PAGE_TITLE = "T-shirts - My Store"
    PAGE_URL = "/index.php?id_category=5&controller=category"

    _locators = {
        "product": "css=.product_img_link img",
        "add_to_cart_button": "name=Submit",
        "added_to_cart_pop_up": "css=.layer_cart_product h2"
    }

    def click_on_product(self):
        with self._wait_for_page_refresh():
            self.selib.click_element(self.locator.product)

    def add_to_cart(self):
        self.click_on_product()
        self.selib.click_button(self.locator.add_to_cart_button)


