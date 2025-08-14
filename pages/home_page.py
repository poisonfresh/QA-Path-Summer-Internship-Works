# pages/home_page.py
from .base_page import BasePage, DEFAULT_TIMEOUT
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage(BasePage):
    URL = "https://www.amazon.com/"


    _LOGO = ("id", "nav-logo-sprites")
    _ACCOUNT_LINE1 = (By.ID, "nav-link-accountList-nav-line-1") 

    def open_home(self):
        self.open(self.URL)
        self.accept_cookies_if_present()
        ok = self.find(self._LOGO, timeout=10) or self.find(("tag", "body"), timeout=8, visible=False)
        if not ok:
            raise AssertionError("Ana sayfa yüklenemedi.")
        print("Ana sayfa yüklendi (amazon.com).")

    def open_sign_in(self):
        self.open("https://www.amazon.com/ap/signin?language=en_US")
        self.accept_cookies_if_present()

    def wait_until_logged_in(self, timeout=120):
        """
        Sen elle giriş yaptıktan sonra, üstteki yazının
        'Hello, sign in' dışındaki bir değere dönmesini bekler.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: (t := d.find_element(*self._ACCOUNT_LINE1)).is_displayed()
                and ("sign in" not in t.text.lower())
            )
            print("Giriş algılandı.")
            return True
        except Exception:
            return False

