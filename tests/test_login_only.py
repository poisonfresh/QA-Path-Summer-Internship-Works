# tests/test_login_only.py
import os, pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.home_page import HomePage
from pages.login_page import LoginPage

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()

def test_login_manual(driver):
    home = HomePage(driver)
    home.open_home()

    login = LoginPage(driver)
    login.open_signin()
    login.dismiss_phone_prompt()
    assert home.wait_until_logged_in(timeout=90), "Elle giriş algılanamadı."



