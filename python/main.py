from my_class import MyClass

if __name__ == "__main__":
    test_url = "https://www.cathaybk.com.tw/cathaybk/"
    my_instance = MyClass(url=test_url, test_type="credit_card")
    my_instance.run_test()

    # input("🔵 測試完成，請按 Enter 關閉程式...")