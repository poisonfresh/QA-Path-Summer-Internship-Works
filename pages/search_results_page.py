# pages/search_results_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class SearchResultsPage(BasePage):
    SEARCH_BOX = [
        (By.ID, "twotabsearchtextbox"),
        (By.NAME, "field-keywords"),
        (By.CSS_SELECTOR, "input[type='text'][aria-label][name='field-keywords']"),
        (By.CSS_SELECTOR, "input[type='text'][aria-label*='Search']"),
    ]
    SEARCH_SUBMIT = [
        (By.ID, "nav-search-submit-button"),
        (By.CSS_SELECTOR, "input[type='submit'][value][aria-label]"),
        (By.CSS_SELECTOR, "span[id='nav-search-submit-text'] input[type='submit']"),
    ]
    _RESULTS_SLOT = (By.CSS_SELECTOR, "div.s-main-slot")
    _PAGE_2_LINKS = [
        (By.CSS_SELECTOR, "a[aria-label='Go to page 2']"),
        (By.CSS_SELECTOR, "a.s-pagination-item[href*='page=2']"),
        (By.XPATH, "//a[contains(@class,'s-pagination-item') and normalize-space()='2' and not(contains(@class,'s-pagination-selected'))]"),
    ]
    _PAGE_2_CURRENT = (
        By.XPATH,
        "//span[contains(@class,'s-pagination-item') and contains(@class,'s-pagination-selected') and normalize-space()='2']"
    )
    _CARD_SELECTOR = "div.s-main-slot div[data-component-type='s-search-result']"
    _TITLE_ANCHORS_SELECTOR = "div.s-main-slot div[data-component-type='s-search-result'] h2 a"

    def _find_first(self, locators, each=6, visible=True):
        cond = EC.visibility_of_element_located if visible else EC.presence_of_element_located
        for by, sel in locators:
            try:
                el = WebDriverWait(self.driver, each).until(cond((by, sel)))
                return el, (by, sel)
            except Exception:
                continue
        return None, None

    def click_any(self, locators, each=5):
        for by, sel in locators:
            try:
                el = WebDriverWait(self.driver, each).until(EC.element_to_be_clickable((by, sel)))
                try:
                    el.click()
                    return True
                except Exception:
                    self.driver.execute_script("arguments[0].click();", el)
                    return True
            except Exception:
                continue
        return False

    def _wait_results_loaded(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self._RESULTS_SLOT)
        )

    def search(self, query: str):
        self.accept_cookies_if_present()
        box, _ = self._find_first(self.SEARCH_BOX, each=8)
        if not box:
            raise AssertionError("Arama kutusu bulunamadı.")
        try:
            box.clear()
        except Exception:
            pass
        box.send_keys(query)
        if not self.click_any(self.SEARCH_SUBMIT, each=6):
            raise AssertionError("Arama butonu tıklanamadı.")
        self._wait_results_loaded()

    def go_to_page_2(self):
        link = None
        for by, sel in self._PAGE_2_LINKS:
            link = self.find((by, sel), timeout=4)
            if link:
                break
        if not link:
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except Exception:
                pass
            for by, sel in self._PAGE_2_LINKS:
                link = self.find((by, sel), timeout=4)
                if link:
                    break
        if not link:
            raise AssertionError("Sayfa 2 linki bulunamadı.")
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
        except Exception:
            pass
        try:
            link.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", link)
        self._wait_results_loaded(timeout=20)

    def assert_on_page_2(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self._PAGE_2_CURRENT)
            )
        except Exception:
            raise AssertionError("Sayfa 2 görüntülenmiyor.")

    def open_nth_result(self, n: int):
        self._wait_results_loaded()
        anchors = self.driver.find_elements(By.CSS_SELECTOR, self._TITLE_ANCHORS_SELECTOR)
        anchors = [a for a in anchors if a.is_displayed()]
        if not anchors:
            raise AssertionError("Ürün başlık linkleri bulunamadı.")
        if n < 1 or n > len(anchors):
            raise AssertionError(f"{n}. ürün yok. Toplam başlık linki: {len(anchors)}")
        target = anchors[n - 1]
        title_text = (target.text or target.get_attribute("innerText") or "").strip()
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target)
        except Exception:
            pass
        try:
            target.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", target)
        return title_text
