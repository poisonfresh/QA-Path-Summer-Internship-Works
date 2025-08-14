# pages/base_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 15

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str):
        print(f"URL açılıyor: {url}")
        self.driver.get(url)
        print("URL açıldı:", self.driver.current_url)

    def _by(self, locator):
        how, what = locator
        mapping = {
            "id": By.ID, "css": By.CSS_SELECTOR, "xpath": By.XPATH,
            "name": By.NAME, "class": By.CLASS_NAME, "tag": By.TAG_NAME
        }
        return (mapping.get(how, how), what)

    def find(self, locator, timeout=DEFAULT_TIMEOUT, visible=True):
        wait = WebDriverWait(self.driver, timeout)
        cond = EC.visibility_of_element_located if visible else EC.presence_of_element_located
        try:
            return wait.until(cond(self._by(locator)))
        except Exception:
            return None

    def click(self, locator, timeout=DEFAULT_TIMEOUT):
        el = self.find(locator, timeout=timeout)
        if not el:
            return False
        try:
            el.click()
            return True
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", el)
                return True
            except Exception:
                return False

    def type(self, locator, text, timeout=DEFAULT_TIMEOUT, clear=True):
        el = self.find(locator, timeout=timeout)
        if not el:
            return False
        try:
            if clear:
                el.clear()
        except Exception:
            pass
        try:
            el.send_keys(text)
            return True
        except Exception:
            try:
                self.driver.execute_script("arguments[0].value=arguments[1];", el, text)
                return True
            except Exception:
                return False

    def wait_url_contains(self, fragment, timeout=DEFAULT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))
            return True
        except Exception:
            return False

    def accept_cookies_if_present(self):
        candidates = [
            ("id", "sp-cc-accept"),
            ("css", "input#sp-cc-accept"),
            ("css", ".a-button-input[aria-labelledby*='sp-cc-accept']"),
            ("css", "input[name='accept']"),
            ("css", "input[name='sp-cc-accept']"),
        ]
        for c in candidates:
            btn = self.find(c, timeout=2)
            if btn:
                try:
                    btn.click()
                    print("Cookie banner kapattık.")
                    return True
                except Exception:
                    pass
        return False
    def switch_to_newest_tab(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def switch_to_first_tab(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[0])

