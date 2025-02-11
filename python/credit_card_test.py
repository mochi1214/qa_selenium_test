from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class CreditCardTest:
    def __init__(self, driver):
        """使用 BaseTest 提供的 driver"""
        self.driver = driver

    def credit_card_run_test(self):
        self.click_menu()

    def click_menu(self):
        try:
            print("🔍 等待左上角選單按鈕...")

            # 使用 XPath 定位選單按鈕
            menu_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "cubre-a-burger")]'))
            )

            print("✅ 成功找到選單按鈕，準備點擊...")
            menu_button.click()
            print("✅ 選單按鈕點擊成功！")

            print("⏳ 等待選單展開...")
            menu_content = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "cubre-o-menu__content")]'))
            )
            print("✅ 選單成功展開！")

            # 確保選單內容載入
            print("⏳ 等待選單內容...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "cubre-o-menuLinkList")]'))
            )
            print("✅ 選單內容已載入！")

        except Exception as e:
            print(f"❌ 選單未展開，請確認 XPath 是否正確: {e}")
