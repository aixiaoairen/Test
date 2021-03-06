'''
实现了登录西南大学教务系统
'''
from selenium import webdriver
import requests
import time
from selenium.webdriver.common.keys import Keys
broser=webdriver.Chrome();#实例化浏览器
#broser.get("https://uaaap.swu.edu.cn/cas/login");
broser.get("https://uaaap.swu.edu.cn/cas/login?service="
           "http://i.swu.edu.cn/PersonalApplications/viewPageV3");
time.sleep(2);
cookie_bro=broser.get_cookies();
cookie1=cookie_bro[0]['value'];
print("当前cookie:"+cookie1)
broser.find_element_by_id("username").send_keys("liangshuai")
broser.find_element_by_id("password").send_keys("Lianghao.215")
broser.find_element_by_class_name("blue").click()
###登录成功
time.sleep(2);
time.sleep(1)
#search_window = broser.current_window_handle  # 当登陆后有新增一个网页，用此代码来定位

#根据a标签的全部文本
##一定要注意以下两个语句的区别，被注释的语句是错误的
#即用xpath寻找元素是：driver.find_element。只能寻找一个
#broser.find_elements_by_xpath("/html/body/div[2]/div/div/div/div/div[2]/div/a[3]");
#登录教务系统
broser.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[2]/div/a[3]").click();
time.sleep(2);#登录成功
