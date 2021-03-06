from selenium import webdriver
import time
import datetime
import smtplib
from email.mime.text import MIMEText
#供调用,返回结果(提示，所选分钟)
def login(url,username,password):
    re = [];
    option = webdriver.ChromeOptions()
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    broser = webdriver.Chrome(options=option);  # 实例化浏览器
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
        temp_msg_1=broser.find_element_by_xpath("/html/body/div/div[2]/p");#查看失败原因
        #sendEmail(temp_msg_1.text,"2609362670@qq.com");
        re.append(temp_msg_1.text);
        re.append(-1)
        return re;
    options = broser.find_elements_by_xpath("/html/body/div/form/div/p[3]/select/option");
    length=len(options);#查看当前有多少可选项
    #优先选择最长的
    strs=options[length-1].text;
    ti = ""
    for i in range(0, len(strs)):
        if strs[i] != '分':
            ti += strs[i];
        else:
            break;
    options[length-1].click();
    time.sleep(2);
    broser.find_element_by_xpath("/html/body/div/form/div[2]/button").click();
    result = broser.find_element_by_xpath("/html/body/div/div/p");#操作后的结果
    print(result.text)
    re.append(result.text);
    re.append(int(ti))
    return re;
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
    if text_0[1] <=0:
        sendEmail("占座失败"+text_0[0],remail);
        return -1;
    text_1="2F-001 "+text_0[0];
    sendEmail(text_1,remail);
    time.sleep(10);
    url_2="http://update.unifound.net/wxnotice/s.aspx?c=100601185_Seat_100601457_1FC";
    user_2 = "222018603193015";
    pwd_2 = "222018603193015";
    text_2 = login(url_2, user_2, pwd_2)
    print(text_2[0])
    #if text_2[1] == "不在开放时间" or text_2[0] =="设备已分配给他人使用,未暂离":
    if text_2[1]<=0:
        sendEmail("占座失败:" + text_2[0], remail);
        return -1;
    text_3 = "2F-002 " + text_2[0];
    sendEmail(text_3, remail);
    return text_2[1];
#通用的选择函数，暂不使用
def selectSeat_(url,user,pwd,seat):
    remail = "2609362670@qq.com";
    text_0=login(url,user,pwd)
    if text_0[1] <=0:
        sendEmail("占座失败"+text_0[0],remail);
        return -1;
    text_1=seat+" "+text_0[0];
    sendEmail(text_1,remail);
    time.sleep(10);
    return text_1[1];
#计算时间的函数
def nowTime():
    dt = datetime.datetime.now();
    hours=dt.hour;#小时[0,24]
    mins=dt.minute;#分钟[0,60]
    return hours*60+mins;
if __name__ == '__main__':
    i=1;
    s=0;
    f=0;
    fs=0;
    while True:
        print("{0}:第{1}次运行，成功占座:{2}次，失败{3}次，无效时间内运行{4}次".format(datetime.datetime.now(),i,s,f,fs))
        if(nowTime()>=480 and nowTime()<=1260):
            times=selectSeat();#返回所选时间
            if(times>=0):
                print(datetime.datetime.now(),"-----","已经选择:",times,"分钟");
                print("当前时间为:",int(nowTime()/60),":",nowTime()%60)
                s=s+1
                time.sleep(times+10);
            else:
                print("------作为已经被占用，下一次尝试占座时间为:", int(nowTime() / 60) + 1, ":", nowTime() % 60)
                time.sleep(3600);#休眠1个小时
                f = f + 1;
        elif nowTime()<400 or nowTime()>1300:
            print("------不在开放时间，即将休眠，下一次尝试占座时间为:",int(nowTime()/60)+1,":",nowTime()%60)
            fs=fs+1
            time.sleep(3600);
        i=1+1;