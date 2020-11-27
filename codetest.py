# coding = utf-8

from selenium import webdriver
import time
import os
import json
from threading import Thread

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver")

current_url = 'https://www.vmall.com/?ANONYMITY_LOGIN_NAME=135****5770'
LOGIN_SUCCESS_CONFIRM = 'https://www.vmall.com/?ANONYMITY_LOGIN_NAME=135****5770'
print(current_url.find(LOGIN_SUCCESS_CONFIRM))
LOGIN_URL = 'https://id1.cloud.huawei.com/CAS/portal/loginAuth.html?validated=true&themeName=red&service=https%3A%2F%2Fwww.vmall.com%2Faccount%2Fcaslogin%3Furl%3Dhttps%253A%252F%252Fwww.vmall.com%252F&loginChannel=26000000&reqClientType=26&lang=zh-cn'



driver = webdriver.Chrome(DRIVER_BIN)
driver.get(LOGIN_URL)

with open('cookies.txt', 'w') as cookief:
    # 将cookies保存为json格式
    cookief.write(json.dumps(driver.get_cookies()))

driver.close()