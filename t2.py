from selenium import webdriver
import requests
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
broser=webdriver.Chrome();#实例化浏览器
broser.get("http://update.unifound.net/wxnotice/s.aspx?c=100601185_Seat_100601278_1FC");
time.sleep(2);#打开页面，休眠2s
broser.find_element_by_name("szLogonName").send_keys("222018603193001");
broser.find_element_by_name("szPassword").send_keys("Lianghao.215");
broser.find_element_by_class_name("btn").click();
#登录成功
time.sleep(2);
options=broser.find_elements_by_xpath("/html/body/div/form/div/p[3]/select/option");
#print(options[1].text)
options[0].click();
print(options[0].text);
time.sleep(2);#选中
broser.find_element_by_xpath("/html/body/div/form/div[2]/button").click();
result=broser.find_element_by_xpath("/html/body/div/div/p")
print(result.text)
