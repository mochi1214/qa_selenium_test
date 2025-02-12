from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_test import BaseTest
from credit_card_test import CreditCardTest

class MyClass:
    def __init__(self, url, test_type="credit_card"):
        self.base_test = BaseTest()
        self.url = url
        self.test = None

        if test_type == "credit_card":
            self.test = CreditCardTest(driver=self.base_test.driver)


    def run_test(self):
        """確保 BaseTest 完全執行完畢，再執行 CreditCardTest"""
        print("🚀 執行 BaseTest：開啟網站")
        self.base_test.open_website(self.url)

        # 確保頁面載入完畢
        print("⏳ 等待主要內容載入...")
        WebDriverWait(self.base_test.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("✅ BaseTest 執行完成，準備執行 CreditCardTest")

        if self.test:
            print("🚀 執行 CreditCardTest：點擊選單")
            self.test.credit_card_run_test()
        else:
            print("⚠️ 未指定測試類別，僅開啟網站但不執行 CreditCardTest")

        # 測試完成後關閉瀏覽器
        # self.base_test.driver.quit()
        # print("✅ 測試完成，瀏覽器已關閉")
