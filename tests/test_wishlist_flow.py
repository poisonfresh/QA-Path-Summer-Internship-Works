# tests/test_wishlist_flow.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.list_page import ListPage

EMAIL = os.getenv("AMAZON_EMAIL", "")
PWD   = os.getenv("AMAZON_PASSWORD", "")

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # istersen: options.add_argument("--disable-blink-features=AutomationControlled")
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()

def test_wishlist_end_to_end(driver):
    # 1) Ana sayfa
    home = HomePage(driver)
    home.open_home()

    # 2) Login ekranı (manuel giriş)
    login = LoginPage(driver)
    login.open_signin()
    login.dismiss_phone_prompt()   # varsa “Not now”
    assert home.wait_until_logged_in(timeout=90), "Elle giriş tamamlanmadı (Hello, <name> görünmedi)."

    # 3) Arama
    search = SearchResultsPage(driver)
    search.search("samsung")

    # 4) “samsung” sonuç sayfasındayız varsayıyoruz; 5) sayfa 2
    search.go_to_page_2()
    search.assert_on_page_2()

    # 6) 3. ürünü aç
    title_from_results = search.open_nth_result(3)

    # 7) Ürün sayfası: listeye ekle
    product = ProductPage(driver)
    product.add_to_list()
    product.go_to_list_via_confirmation()

    # 8) Liste sayfasında ürün var mı?
    wishlist = ListPage(driver)
    assert wishlist.contains_title(title_from_results), "Ürün Wish List'te bulunamadı."

    # 9) Sil
    assert wishlist.delete_by_title(title_from_results), "Silme butonu bulunamadı."
    # 10) Artık yok
    assert not wishlist.contains_title(title_from_results), "Ürün hâlâ listede görünüyor."


