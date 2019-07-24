import io
import os
import sys
import time
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
def simulation_douban():

    PATH = sys.path[0]


    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # Change encoding into utf-8 for correctly printing

    url = 'https://www.douban.com'
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get(url)
    # print(browser.page_source)
    # browser.implicitly_wait(10)
    USERNAME = 'yourusername'
    PASSWORD = 'yourpassword'
    browser.switch_to.frame(browser.find_elements_by_tag_name('iframe')[0])

    bottom1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    bottom1.click()

    input1 = browser.find_element_by_id('username')
    input1.clear()
    input1.send_keys(USERNAME)
    time.sleep(0.1)
    input2 = browser.find_element_by_id('password')
    input2.clear()
    input2.send_keys(PASSWORD)
    time.sleep(0.1)
    bottom = browser.find_element_by_class_name('account-form-field-submit ')
    bottom.click()
    
    time.sleep(1)
    # print(bro/wser.page_source)
    return browser

