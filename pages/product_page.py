# pages/product_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class ProductPage(BasePage):
    TITLE = (By.ID, "productTitle")
    ADD_TO_LIST = [
        (By.ID, "add-to-wishlist-button-submit"),
        (By.CSS_SELECTOR, "input#add-to-wishlist-button-submit"),
        (By.CSS_SELECTOR, "input[aria-labelledby*='add-to-wishlist-button-submit']"),
    ]
    VIEW_LIST_IN_CONFIRM = [
        (By.ID, "huc-view-your-list"),
        (By.ID, "WLHUC_viewlist"),
        (By.XPATH, "//a[contains(.,'View Your List') or contains(.,'List')]"),
    ]

    def get_title(self) -> str:
        el = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(self.TITLE))
        return el.text.strip()

    def add_to_list(self):
     
        for loc in self.ADD_TO_LIST:
            try:
                WebDriverWait(self.driver, 12).until(EC.element_to_be_clickable(loc)).click()
                return
            except Exception:
                continue
        raise AssertionError("Add to List butonu bulunamadı/tıklanamadı.")

    def go_to_list_via_confirmation(self):
        for loc in self.VIEW_LIST_IN_CONFIRM:
            try:
                WebDriverWait(self.driver, 12).until(EC.element_to_be_clickable(loc)).click()
                return
            except Exception:
                continue
        raise AssertionError("Liste görüntüleme bağlantısı bulunamadı.")



