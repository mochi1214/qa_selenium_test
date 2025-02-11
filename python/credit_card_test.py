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
        self.click_product_intro()

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


            # 確保選單內容載入
            print("⏳ 等待選單內容...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "cubre-o-menuLinkList")]'))
            )
            print("✅ 選單內容已載入！")

        except Exception as e:
                print(f"❌ 選單未展開，請確認 XPath 是否正確: {e}")

    def click_product_intro(self):
        try:

            product_intro_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "cubre-a-menuSortBtn") and contains(text(), "產品介紹")]'))
            )

            # 將元素置頂到頂部，確保按鈕可見，避免無法點擊
            self.scroll_to_element(product_intro_button)
            # self.driver.execute_script("arguments[0].scrollIntoView(true);", product_intro_button)
            # time.sleep(1)

            print("✅ 找到『產品介紹』按鈕，準備點擊...")
            product_intro_button.click()
            print("✅ 成功點擊『產品介紹』！")

            time.sleep(1)

            product_intro_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "cubre-a-menuSortBtn") and contains(text(), "信用卡")]'))
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", product_intro_button)
            time.sleep(1)

            print("✅ 找到『信用卡』按鈕，準備點擊...")
            product_intro_button.click()
            print("✅ 成功點擊『信用卡』！")


        except Exception as e:
            print(f"❌ 點擊『產品介紹』時發生錯誤: {e}")


    # 將元素置頂到頂部，確保按鈕可見，避免無法點擊
    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)


