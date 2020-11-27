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
# Mate 20 X(5G)
BUY_URL = 'https://www.vmall.com/product/10086375798519.html'
# 测试P30 Pro
# BUY_URL = 'https://www.vmall.com/product/10086951150635.html'
# 登录url
LOGIN_URL = 'https://id1.cloud.huawei.com/CAS/portal/loginAuth.html?validated=true&themeName=red&service=https%3A%2F%2Fwww.vmall.com%2Faccount%2Fcaslogin%3Furl%3Dhttps%253A%252F%252Fwww.vmall.com%252F&loginChannel=26000000&reqClientType=26&lang=zh-cn'
# 登录成功手动确认URL
LOGIN_SUCCESS_CONFIRM = 'https://www.vmall.com/'
# 开始自动刷新等待抢购按钮出现的时间点,提前3分钟
BEGIN_GO = '2020-11-25 10:15:00'

class OpenAccountLocators:
    # 这里有一层隐藏div 有点坑哈
    ACTIVE_BUTTON_JS = "document.getElementsByClassName('home-pop')[0].style.display='none'"

# 进到购买页面后提交订单
def submitOrder(driver, user):
    time.sleep(1)
    while BUY_URL == driver.current_url:
        print(user + ':当前页面还在商品详情！！！')
        time.sleep(3)

    while True:
        try:
            submitOrder = driver.find_element_by_link_text('提交订单')
            submitOrder.click()
            print(user + ':成功提交订单')
            break
        except:
            print(user + ':提交不了订单！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！')
            time.sleep(1)  # 到了订单提交页面提交不了订单一直等待
            pass
    while True:
        time.sleep(3000)
        print(user + ':进入睡眠3000s')
        pass


# 排队中
def onQueue(driver, user):
    time.sleep(1)
    nowUrl = driver.current_url
    while True:
        try:
            errorbutton = driver.find_element_by_link_text('返回活动页面')  # 出现这个一般是失败了。。
            if errorbutton.is_enabled():
                print(user + "：出现返回活动页面，可能抢购失败。。。")
                errorbutton.click()
            pass
        except:
            print(user + ':排队中')
            time.sleep(0.3)  # 排队中
            pass
        if nowUrl != driver.current_url and nowUrl != BUY_URL:
            print(user + ':排队页面跳转了!!!!!!!!!!!!!!')
            break
        else:
            goToBuy(driver, user)
    submitOrder(driver, user)


# 登录成功去到购买页面
def goToBuy(driver, user):
    driver.get(BUY_URL)
    print(user + '打开购买页面')
    # 转换成抢购时间戳
    timeArray = time.strptime(BEGIN_GO, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # 结束标志位
    over = False
    while True:
        if time.time() > timestamp:  # 到了抢购时间
            button = driver.find_elements_by_xpath('//*[@id="pro-operation"]/a')
            text = driver.find_elements_by_xpath('//*[@id="pro-operation"]/a/span')[0].text
            if text == '已售完':
                over = True
                break
            if text == '立即申购' and button.get_attribute('class') != 'product-button02 disabled':
            # buyButton = driver.find_element_by_link_text('立即申购')
                print(user + '立即申购按钮出现了！！！')
                button.click()
                print(user + '立即申购')
                break
            time.sleep(0.2)
        else:
            time.sleep(15)
            print(user + '睡眠15s，未到脚本开启时间：' + BEGIN_GO)
    if over:
        print("很遗憾，抢购结束。。。")
        exit(0)
    else:
        onQueue(driver, user)


# 登录商城,登陆成功后至商城首页然后跳转至抢购页面
def loginMall(user, pwd):
    # driver = webdriver.Chrome(executable_path=chrome_driver)
    driver = webdriver.Chrome(DRIVER_BIN)
    driver.get(LOGIN_URL)
    # 首先清除由于浏览器打开已有的cookies
    driver.delete_all_cookies()

    with open('cookies.txt', 'r') as cookief:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookieslist = json.load(cookief)

        # 方法1 将expiry类型变为int
        for cookie in cookieslist:
            # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)

    # 刷新页面
    driver.refresh()
    driver.implicitly_wait(5)
    goToBuy(driver, user)


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
