from my_class import MyClass

if __name__ == "__main__":
    # 設定開發模式
    dev_mode = False

    if dev_mode:
        print("🛑 現在為開發模式，不會執行截圖功能")

    test_url = "https://www.cathaybk.com.tw/cathaybk/"
    my_instance = MyClass(url=test_url, test_type="credit_card", dev_mode=dev_mode)
    my_instance.run_test()

    if dev_mode:
        input("🔵 測試完成，請按 Enter 關閉程式...")