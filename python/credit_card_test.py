from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class CreditCardTest:
    def __init__(self, driver):
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
            # 點擊「產品介紹」
            product_intro_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "cubre-a-menuSortBtn") and contains(text(), "產品介紹")]'))
            )

            # 將元素置頂到頂部，確保按鈕可見，避免無法點擊
            self.scroll_to_element(product_intro_button)

            print("✅ 找到『產品介紹』按鈕，準備點擊...")
            product_intro_button.click()
            print("✅ 成功點擊『產品介紹』！")

            time.sleep(0.5)

            # 點擊「產品介紹 > 信用卡」
            product_intro_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "cubre-a-menuSortBtn") and contains(text(), "信用卡")]'))
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", product_intro_button)
            time.sleep(0.5)

            print("✅ 找到『信用卡』按鈕，準備點擊...")
            product_intro_button.click()
            print("✅ 成功點擊『信用卡』！")

            self.count_credit_card_items()

            time.sleep(0.5)

            # 點擊「產品介紹 > 信用卡 > 信用卡介紹」
            product_intro_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "cubre-a-menuLink") and contains(text(), "卡片介紹")]'))
            )

            print("✅ 找到『信用卡介紹』按鈕，準備點擊...")
            product_intro_button.click()
            print("✅ 成功點擊『信用卡介紹』！")

            # 點擊「產品介紹 > 信用卡 > 信用卡介紹 > 停發卡」
            print("🔍 等待『停發卡』按鈕...")

            disabled_card_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "cubre-m-anchor__btn") and normalize-space()="停發卡"]'))
            )

            # 確保按鈕可見
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", disabled_card_button)
            time.sleep(1)

            print("✅ 找到『停發卡』按鈕，準備點擊...")
            disabled_card_button.click()
            print("✅ 成功點擊『停發卡』！")

            # 計算「停發卡」的數量
            time.sleep(0.5)
            self.count_disabled_credit_cards()

        except Exception as e:
            print(f"❌ 點擊『產品介紹』時發生錯誤: {e}")


    def count_disabled_credit_cards(self):
        try:
            print("🔍 測試 Swiper 切換卡片...")

            print("📜 滾動 100px 以顯示『停發卡』...")
            self.driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(1)

            # 等待『停發卡』區塊出現
            block_locator = (By.XPATH, '//section[@data-anchor-block="blockname06"]')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(block_locator))
            block_element = self.driver.find_element(*block_locator)

            print("✅ 停發卡區塊已顯示，準備開始測試切換...")

            pagination_bullets = block_element.find_elements(By.XPATH, './/div[contains(@class, "swiper-pagination")]//span[contains(@class, "swiper-pagination-bullet")]')

            print(f"🔍 發現 {len(pagination_bullets)} 個 pagination bullets，開始測試...")

            # 先對第一張卡片截圖
            first_screenshot_filename = "screenshot/screenshot_card_1.png"
            self.driver.save_screenshot(first_screenshot_filename)
            print(f"📸 已截圖: {first_screenshot_filename}")

            for index, bullet in enumerate(pagination_bullets, start=1):
                try:
                    # 記錄當前 active 卡片
                    old_active_card = block_element.find_element(By.XPATH, './/div[contains(@class, "swiper-slide-active")]')

                    print(f"🔄 點擊第 {index} 個 pagination bullet...")
                    self.driver.execute_script("arguments[0].click();", bullet)
                    time.sleep(2)

                    # 確認 active 卡片是否發生變化
                    new_active_card = block_element.find_element(By.XPATH, './/div[contains(@class, "swiper-slide-active")]')

                    if new_active_card != old_active_card:
                        print(f"✅ 成功切換到第 {index} 張卡片")

                        # 截圖
                        screenshot_filename = f"screenshot/screenshot_card_{index+1}.png"
                        self.driver.save_screenshot(screenshot_filename)
                        print(f"📸 已截圖: {screenshot_filename}")

                    else:
                        print(f"⚠️ 第 {index} 張卡片未發生變化，可能未成功點擊")

                except Exception as e:
                    print(f"⚠️ 第 {index} 個 pagination bullet 無法點擊: {e}")

            print("✅ Swiper 測試完成！")

        except Exception as e:
            print(f"❌ 測試 Swiper 切換時發生錯誤: {e}")


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
            # self.driver.get_screenshot_as_file("/Users/chiachenwu/Desktop/creditcard_item_count.png")

            # 列出信用卡項目的名稱
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






