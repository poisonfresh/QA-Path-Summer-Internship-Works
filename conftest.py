# conftest.py
import os, pathlib, pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def driver():
    opts = Options()
    # 1) Kalıcı kullanıcı profili (ilk sefer manual login yapacağız)
    profile_dir = pathlib.Path(r"C:\work\chrome-profile\amazon")
    profile_dir.mkdir(parents=True, exist_ok=True)
    opts.add_argument(f"--user-data-dir={profile_dir}")
    opts.add_argument("--profile-directory=Default")  # tek profil yeter

    # 2) Bot sinyallerini azalt
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    # 3) Stabil bir UA ve dil
    opts.add_argument("--lang=tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7")
    opts.add_argument("--window-size=1400,900")
    # Headless mod kullanma (Amazon daha agresif kontrol ediyor)

    drv = webdriver.Chrome(options=opts)

    # navigator.webdriver'ı gizle
    drv.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """
    })

    try:
        yield drv
    finally:
        drv.quit()
