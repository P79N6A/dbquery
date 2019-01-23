#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
from down_sql import *
username = "zhengdan10"
password = "!@#$820728devilnbZD"
driver = webdriver.Chrome('./chromedriver.exe')
driver.get("http://dbquery.jd.com")
driver.set_page_load_timeout(5)
print(driver)
time.sleep(5)
driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").send_keys(password)

driver.find_element_by_class_name("formsubmit_btn").click()
cookie_list = driver.get_cookies()
cookie = [item["name"] + "=" + item["value"] for item in cookie_list]  
  
cookiestr = ';'.join(item for item in cookie)
print('cookiestr =' + cookiestr)
sql = DownSql(cookiestr)
driver.quit()
