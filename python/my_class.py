from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_test import BaseTest
from credit_card_test import CreditCardTest
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MyClass:
    def __init__(self, url, test_type="credit_card", dev_mode=False):
        self.base_test = BaseTest(dev_mode)
        self.url = url
        self.test = None
        self.dev_mode = dev_mode

        if test_type == "credit_card":
            self.test = CreditCardTest(driver=self.base_test.driver, dev_mode=dev_mode)


    def run_test(self):
        self.base_test.open_website(self.url)

        # 確保頁面載入完畢
        logging.info("⏳ 等待主要內容載入...")
        WebDriverWait(self.base_test.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logging.info("✅ 執行完成，準備開始執行測試")

        if self.test:
            self.test.credit_card_run_test()
        else:
            logging.info("⚠️ 未指定測試類別，僅開啟網站")

        if not self.dev_mode:
            # 測試完成後關閉瀏覽器
            self.base_test.driver.quit()
            logging.info("✅ 測試完成，瀏覽器已關閉")
