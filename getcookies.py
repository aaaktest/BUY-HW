# coding = utf-8

from selenium import webdriver
import time
import os
from threading import Thread
import json

ACCOUNTS = {
    "username": "password"
}
# chrome_driver = "D:\chromedriver.exe"   # Win32_76.0.3809.126
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver")

LOGIN_URL = 'https://id1.cloud.huawei.com/CAS/portal/loginAuth.html?validated=true&themeName=red&service=https%3A%2F%2Fwww.vmall.com%2Faccount%2Fcaslogin%3Furl%3Dhttps%253A%252F%252Fwww.vmall.com%252F&loginChannel=26000000&reqClientType=26&lang=zh-cn'
# 登录成功手动确认URL
LOGIN_SUCCESS_CONFIRM = 'https://www.vmall.com/'



# 登录商城,登陆成功后至商城首页保存cookies
def loginMall(user, pwd):
    # driver = webdriver.Chrome(executable_path=chrome_driver)
    driver = webdriver.Chrome(DRIVER_BIN)
    driver.get(LOGIN_URL)
    try:
        driver.implicitly_wait(5)
        # time.sleep(5)  # 等待页面加载完成
        coveraccount1 = driver.find_element_by_class_name('hwid-cover-input')
        coveraccount1.click()
        time.sleep(1)
        account1 = driver.find_elements_by_xpath('//input[@type="text"]')[0]
        password1 = driver.find_element_by_class_name('hwid-input-pwd')
        account1.send_keys(user)
        time.sleep(1)
        password1.send_keys(pwd)
        print(user + '输入了账号密码，等待手动登录')
    except:
        print(user + '账号密码不能输入')
    while True:
        time.sleep(1)
        print(driver.current_url)
        print(driver.current_url.find(LOGIN_SUCCESS_CONFIRM))
        if driver.current_url.find(LOGIN_SUCCESS_CONFIRM) >= 0:
            print(user + '登录成功！')
            with open('cookies.txt', 'w') as cookief:
                # 将cookies保存为json格式
                cookief.write(json.dumps(driver.get_cookies()))
                print(user + 'cookies写入成功！')
    driver.close()

if __name__ == "__main__":
    # 账号密码
    data = ACCOUNTS
    # 构建线程
    threads = []
    for account, pwd in data.items():
        t = Thread(target=loginMall, args=(account, pwd,))
        threads.append(t)
        # 启动所有线程
    for thr in threads:
        time.sleep(2)
        thr.start()
