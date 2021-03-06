from selenium import webdriver
import time
import smtplib
from email.mime.text import MIMEText
#供调用,返回结果
def login(url,username,password):
    broser = webdriver.Chrome();  # 实例化浏览器
    broser.get(url);#模拟登录
    time.sleep(2);#睡眠2s
    broser.find_element_by_name("szLogonName").send_keys(username);
    broser.find_element_by_name("szPassword").send_keys(password);
    broser.find_element_by_class_name("btn").click();
    # 登录成功
    time.sleep(2);
    #在这里要检验一下：
    temp_msg=broser.find_element_by_xpath("/html/body/div/div/p");
    if temp_msg.text == "操作失败":
        temp_msg_1=broser.find_element_by_xpath("/html/body/div/div[2]/p");
        #sendEmail(temp_msg_1.text,"2609362670@qq.com");
        return temp_msg_1.text;
    options = broser.find_elements_by_xpath("/html/body/div/form/div/p[3]/select/option");
    length=len(options);#查看当前有多少可选项
    #优先选择最长的
    options[length-1].click();
    time.sleep(2);
    broser.find_element_by_xpath("/html/body/div/form/div[2]/button").click();
    result = broser.find_element_by_xpath("/html/body/div/div/p");#操作后的结果
    return result.text;
#发送通知邮件
def sendEmail(text,remail):
    smtp = "smtp.163.com";
    subject = "图书馆占座"
    #邮件的大致设置
    sender = "lianghaoswu@163.com";#发送者
    pwds = "TLNOFJSYQPYWISOA";#邮箱第三方登录授权码
    content = text;#内容
    recver =remail;#接收方
    #设置发送邮件明文
    message = MIMEText(content, "plain", "utf-8");
    message['Subject'] = subject;
    message['To'] = recver;
    message['Form'] = sender;
    #登录并发送邮件
    smtp = smtplib.SMTP_SSL("smtp.163.com", 994);#实例化邮箱
    smtp.login(sender, pwds);#登录
    smtp.sendmail(sender, [recver], message.as_string())
    smtp.close();
    return 1;
#整合：
#我已经内置了座位的URL和个人信息
def selectSeat():
    remail = "2609362670@qq.com";
    url_1="http://update.unifound.net/wxnotice/s.aspx?c=100601185_Seat_100601278_1FC";
    user_1="222018603193001";
    pwd_1="Lianghao.215";
    text_0=login(url_1,user_1,pwd_1)
    if text_0 == "不在开放时间":
        sendEmail("占座失败"+text_0,remail);
        return -1;
    text_1="2F-001 "+text_0;
    sendEmail(text_1,remail);
    time.sleep(10);
    url_2="http://update.unifound.net/wxnotice/s.aspx?c=100601185_Seat_100601457_1FC";
    user_2 = "222018603193015";
    pwd_2 = "222018603193015";
    text_2 = "2F-002 "+login(url_2,user_2,pwd_2);
    sendEmail(text_2,remail);
    return 1;
if __name__ == '__main__':
    selectSeat()