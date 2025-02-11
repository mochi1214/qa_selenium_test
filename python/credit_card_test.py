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

            time.sleep(0.5)

            product_intro_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "cubre-a-menuSortBtn") and contains(text(), "信用卡")]'))
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", product_intro_button)
            time.sleep(0.5)

            print("✅ 找到『信用卡』按鈕，準備點擊...")
            product_intro_button.click()
            print("✅ 成功點擊『信用卡』！")

            # time.sleep(5)

            self.count_credit_card_items()

        except Exception as e:
            print(f"❌ 點擊『產品介紹』時發生錯誤: {e}")


    # 將元素置頂到頂部，確保按鈕可見，避免無法點擊
    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)


    # 計算信用卡列表的項目數量
    def count_credit_card_items(self):
        try:
            print("🔍 等待『信用卡』列表展開...")

            # 等待信用卡子選單的父級元素變成 is-L2open，確保真的展開
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "cubre-o-menuLinkList__item") and contains(@class, "is-L2open")]'))
            )

            print("✅ 信用卡列表展開成功，開始計算項目數量...")

            # 等待所有子項目可見
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "cubre-o-menuLinkList__content")]//a[contains(@class, "cubre-a-menuLink")]'))
            )

            # 計算信用卡的子項目
            card_items = self.driver.find_elements(By.XPATH, '//div[contains(@class, "cubre-o-menuLinkList__item") and contains(@class, "is-L2open")]//div[contains(@class, "cubre-o-menuLinkList__content")]//a[contains(@class, "cubre-a-menuLink")]')

            # 截圖
            time.sleep(1)
            self.driver.get_screenshot_as_file("/Users/chiachenwu/Desktop/creditcard_item_count.png")

            # **列出 9 個項目的名稱**
            item_names = [item.text.strip() for item in card_items if item.text.strip()]
            item_count = len(item_names)

            print(f"✅ 信用卡列表共有 {item_count} 項")
            print("📋 信用卡選單項目:")
            for index, name in enumerate(item_names, start=1):
                print(f"{index}. {name}")

            return item_count, item_names


        except Exception as e:
            print(f"❌ 計算信用卡項目數量時發生錯誤: {e}")
            return 0






