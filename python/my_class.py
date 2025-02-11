from itertools import count
from re import search

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def random_delay(min_time=2, max_time=5):
    time.sleep(random.uniform(min_time, max_time))

# 設定 WebDriver 的選項
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

# 設定 WebDriver
driver = webdriver.Chrome()

class MyClass:
    def __init__(self):
        self.driver = driver

    def run_test(self):
        try:
            self.driver.get("https://www.cathaybk.com.tw/cathaybk/")
            print("已開啟目標網頁")

            if is_captcha_present(self.driver):
                input("請手動完成 CAPTCHA 驗證，完成後按下 Enter 繼續...")


            # 確保所有元素顯示
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            print("🔍 嘗試尋找搜尋框 `input#searchBox`...")

            try:
                search_input = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.ID, "searchBox"))
                )
                print("✅ 搜尋框已找到且可見，準備輸入測試內容")

                self.driver.execute_script("arguments[0].scrollIntoView();", search_input)

                random_delay()
                search_input.send_keys("測試內容")
                print("✅ 已輸入搜尋內容")

                # 截圖
                self.driver.get_screenshot_as_file("/Users/chiachenwu/Desktop/homepage.png")
                print("✅ 成功截圖完成")

            except NoSuchElementException:
                print("❌ 搜尋框 `input#searchBox` 找不到，請確認是否需要點擊按鈕才顯示。")

        except Exception as e:
            print(f"測試執行時發生錯誤：{e}")

        finally:
            # 關閉瀏覽器
            self.driver.quit()
            print("測試完成，瀏覽器已關閉")


# 檢查 CAPTCHA 是否存在
def is_captcha_present(driver):
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        if "captcha" in iframe.get_attribute("src").lower():
            print("檢測到 CAPTCHA")
            return True
    except NoSuchElementException:
        pass

    if "robot" in driver.page_source.lower() or "captcha" in driver.page_source.lower():
        print("檢測到 CAPTCHA")
        return True

    print("未檢測到 CAPTCHA")
    return False
