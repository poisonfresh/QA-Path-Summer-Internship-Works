# pages/login_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    NOT_NOW = [
        (By.ID, "ap-account-fixup-phone-skip-link"),
        (By.XPATH, "//a[contains(.,'Not now') or contains(.,'Şimdilik değil') or contains(@id,'skip')]"),
    ]

    def open_signin(self):
        self.open("https://www.amazon.com/ap/signin?language=en_US")
        self.accept_cookies_if_present()

    def dismiss_phone_prompt(self):
        for by, sel in self.NOT_NOW:
            el = None
            try:
                el = self.driver.find_element(by, sel)
            except Exception:
                pass
            if el:
                try:
                    el.click()
                    print("Telefon doğrulama ekranı kapatıldı (Not now).")
                    return True
                except Exception:
                    pass
        return False

