from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_test import BaseTest
from credit_card_test import CreditCardTest
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MyClass:
    def __init__(self, url, test_type="credit_card", dev_mode=False, platform_name="Web", device_name=None):
        self.base_test = BaseTest(dev_mode, platform_name, device_name)
        self.url = url
        self.test = None
        self.dev_mode = dev_mode

        if test_type == "credit_card":
            self.test = CreditCardTest(driver=self.base_test.driver, dev_mode=dev_mode)


    def run_test(self):
        self.base_test.open_website(self.url)

        if self.test:
            self.test.credit_card_run_test()
        else:
            logging.info("⚠️ 未指定測試類別，僅開啟網站")

        if not self.dev_mode:
            # 測試完成後關閉瀏覽器
            self.base_test.driver.quit()
            logging.info("✅ 測試完成，瀏覽器已關閉")
