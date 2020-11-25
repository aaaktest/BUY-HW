# coding = utf-8

from selenium import webdriver
import time
import os
from threading import Thread

current_url = 'https://www.vmall.com/?ANONYMITY_LOGIN_NAME=135****5770'
LOGIN_SUCCESS_CONFIRM = 'https://www.vmall.com/?ANONYMITY_LOGIN_NAME=135****5770'
print(current_url.find(LOGIN_SUCCESS_CONFIRM))
