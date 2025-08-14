# pages/list_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class ListPage(BasePage):

    _ITEMS = (By.CSS_SELECTOR, "div#g-items li, div[data-itemid]") 
    _ITEM_TITLES_IN = " h3 a, span.a-list-item a, a[id^='itemName_']"
    _DELETE_BTNS_IN = " input[name='submit.deleteItem'], input[name='submit.deleteItem.x'], span.a-declarative input[value*='Delete']"

    def _all_items(self):
        try:
            return WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located(self._ITEMS)
            )
        except Exception:
            return []

    def contains_title(self, expected: str) -> bool:
        expected_low = expected.strip().lower()
        for li in self._all_items():
            try:
                t = li.find_element(By.CSS_SELECTOR, self._ITEM_TITLES_IN).text.strip().lower()
                if expected_low[:50] in t:  
                    return True
            except Exception:
                continue
        return False

    def delete_by_title(self, expected: str) -> bool:
        expected_low = expected.strip().lower()
        for li in self._all_items():
            title_txt = ""
            try:
                title_txt = li.find_element(By.CSS_SELECTOR, self._ITEM_TITLES_IN).text.strip().lower()
            except Exception:
                pass
            if expected_low[:50] in title_txt:
                try:
                    btn = li.find_element(By.CSS_SELECTOR, self._DELETE_BTNS_IN)
                    self.driver.execute_script("arguments[0].click();", btn)
                    return True
                except Exception:
                    pass
        return False
