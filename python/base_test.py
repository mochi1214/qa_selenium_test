from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import random

class BaseTest:
    def __init__(self):
        """初始化 WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        # 使用手機模式
        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},  # iPhone X 模擬
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36"
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

        self.driver = webdriver.Chrome(options=options)


    def open_website(self, url):
        try:
            self.driver.get(url)
            print(f"✅ 已開啟目標網頁： {url}")

            if self.is_captcha_present():
                input("⚠️ 請手動完成 CAPTCHA 驗證，完成後按 Enter 繼續...")

            print("🔍 嘗試尋找搜尋框 `input#searchBox`...")
            search_input = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "searchBox"))
            )
            print("✅ 搜尋框已找到且可見，準備輸入測試內容")

            # 避免不必要的滾動
            if not self.is_element_in_viewport(search_input):
                print("🔍 搜尋框不在視野內，準備滾動...")
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", search_input)
                time.sleep(0.5)

            self.random_delay()
            time.sleep(0.5)
            search_input.send_keys("測試內容")
            print("✅ 已輸入搜尋內容")

            # 截圖
            # self.driver.get_screenshot_as_file("/Users/chiachenwu/Desktop/homepage.png")

            time.sleep(0.5)

        except NoSuchElementException:
            print("❌ 搜尋框 `input#searchBox` 找不到")
        except Exception as e:
            print(f"❌ 測試執行時發生錯誤：{e}")


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
            print("檢測到 CAPTCHA")
            return True

        print("未檢測到 CAPTCHA")
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
