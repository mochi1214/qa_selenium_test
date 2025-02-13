from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from appium import webdriver as appium_webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BaseTest:
    def __init__(self, dev_mode=True, platform_name="Web", device_name=None):
        self.dev_mode = dev_mode
        self.platform_name = platform_name
        self.device_name = device_name
        self.driver = None

        if platform_name.lower() == "web":
            logging.info("🌍 使用 Selenium WebDriver 測試桌面瀏覽器...")
            self.setup_selenium()
        elif platform_name.lower() in ["ios", "android"]:
            logging.info(f"📱 使用 Appium WebDriver 測試手機 ({platform_name})...")
            self.setup_appium()
        else:
            raise ValueError(f"❌ 不支援的平台名稱: {platform_name}")


    def setup_selenium(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.set_window_size(800, 1000)


    def setup_appium(self):
        capabilities = AppiumOptions()
        capabilities.set_capability("platformName", self.platform_name)
        capabilities.set_capability("deviceName", self.device_name if self.device_name else "iPhone 14")
        capabilities.set_capability("browserName", "Safari")
        capabilities.set_capability("automationName", "XCUITest")
        capabilities.set_capability("platformVersion", "16.4")
        capabilities.set_capability("useNewWDA", True)

        logging.info(f"📱 使用 Appium 測試 {self.platform_name}，設備: {self.device_name}")
        self.driver = appium_webdriver.Remote("http://127.0.0.1:4723", options=capabilities)


    def open_website(self, url):
        try:
            self.driver.get(url)
            print("------------- 第一部分 -------------")
            logging.info(f"✅ 已開啟目標網頁： {url}")

            if self.is_captcha_present():
                input("⚠️ 請手動完成 CAPTCHA 驗證，完成後按 Enter 繼續...")

            logging.info("🔍 嘗試尋找搜尋框 `input#searchBox`...")
            search_input = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "searchBox"))
            )
            logging.info("✅ 搜尋框已找到且可見，準備輸入測試內容")

            if not self.is_element_in_viewport(search_input):
                logging.info("🔍 搜尋框不在視野內，準備滾動...")
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", search_input)
                time.sleep(0.5)

            self.random_delay()
            time.sleep(0.5)
            search_input.send_keys("測試內容")
            logging.info("✅ 已輸入搜尋內容")

            # 截圖
            self.take_screenshot("screenshot/homepage.png")

            time.sleep(0.5)

        except NoSuchElementException:
            logging.info("❌ 搜尋框 `input#searchBox` 找不到")
        except Exception as e:
            logging.info(f"❌ 測試執行時發生錯誤：{e}")

    # 檢查 CAPTCHA 是否存在
    def is_captcha_present(self):
        try:
            iframe = self.driver.find_element(By.TAG_NAME, "iframe")
            if "captcha" in iframe.get_attribute("src").lower():
                print("檢測到 CAPTCHA")
                return True
        except NoSuchElementException:
            pass

        if "robot" in self.driver.page_source.lower() or "captcha" in self.driver.page_source.lower():
            print("⚠️ 檢測到 CAPTCHA")
            return True

        print("✅ 未檢測到 CAPTCHA")
        return False


    def random_delay(self, min_time=2, max_time=5):
        time.sleep(random.uniform(min_time, max_time))


    def is_element_in_viewport(self, element):
        # 檢查元素是否在視野內
        return self.driver.execute_script(
            "var rect = arguments[0].getBoundingClientRect();"
            "return (rect.top >= 0 && rect.left >= 0 && rect.bottom <= window.innerHeight && rect.right <= window.innerWidth);",
            element
        )

    def take_screenshot(self, filename):
        # 根據模式決定是否執行截圖
        if not self.dev_mode:
            self.driver.get_screenshot_as_file(filename)
            logging.info(f"📸 已截圖: {filename}")
