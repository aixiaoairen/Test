from selenium import webdriver
import win32gui
import win32con
import win32clipboard as w
import pandas as pd
import time;
import datetime
import os
import smtplib
from email.mime.text import MIMEText
'''
download("222018603193001","206416","晨")
'''
def download(username,pwd,task):
    option = webdriver.ChromeOptions()
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = webdriver.Chrome(options=option);  # 实例化浏览器
    # 打开网页
    driver.get("http://authserverxg.swu.edu.cn/authserver/login?service=https%3A%2F%2Fswu.campusphere.net%2Fportal%2Flogin");
    # 打开成功
    time.sleep(2);  # 休眠2s
    '''
    开始登录“金智教育平台”
    '''
    driver.find_element_by_id("username").send_keys(username);
    driver.find_element_by_id("password").send_keys(pwd);
    # 通过class_name寻找元素可以只写部分class_name，如果包含空格的话，最好只写空格之前的
    driver.find_element_by_class_name("auth_login_btn").click();#登录按钮
    time.sleep(4);
    driver.find_element_by_xpath("/html/body/div/article[4]/aside/div/div/div[3]/div").click();
    time.sleep(1);
    coachCat = driver.find_element_by_xpath(
        "/html/body/div/article[4]/aside/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/h5")
    coachCat.click();  # 点击进入辅导猫
    time.sleep(1);  # 进入成功，休眠1s
    search_window = driver.window_handles;  # 返回当前的多个句柄，list类型
    driver.switch_to.window(search_window[len(search_window) - 1]);  # 根据句柄来定位网页,默认选择最新的窗口
    # 点击我关注的任务
    time.sleep(4);  # 新打开页面后，有可能html资源没有加载完全，因此无法找到
    driver.find_element_by_xpath("//span[text()=\"我关注的任务\"]").click();
    time.sleep(1);
    '''
    根据实际需求：
    查寝和签到
    '''
    driver.find_element_by_xpath("/html/body/div[5]/div[3]/div/div[2]/"
                                 "div[2]/div/div[2]/div/div[2]/div[3]/"
                                 "div/div[1]/div[1]/div[3]/div[6]").click();  # 签到
    # 一般只有晨间打卡和晚间打卡
    time.sleep(2);
    task_morning = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]"
                                                "/div/div[2]/div[3]/div/div[3]/div/div/div/div[2]/"
                                                "table/tbody/tr[2]/td[2]/div/span");
    task_night=driver.find_element_by_xpath("/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/"
                                            "div[2]/div[3]/div/div[3]/div/div/div/div[2]/table/tbody/tr[1]/"
                                            "td[2]/div/span");
    if task in task_morning.text:
        task_morning.click();
    elif task in task_night.text:
        task_night.click();
    else:
        print("任务无法分辨，task="+task);
        return 0;
    search_window = driver.window_handles;  # 返回当前的多个句柄，list类型
    driver.switch_to.window(search_window[len(search_window) - 1]);  # 根据句柄来定位网页,默认选择最新的窗口
    time.sleep(10);
    # 打开每日数据界面，总是看第一行数据的详情
    # 因为每日详情在table里面，而table在frame中，因此，我们需要先选择frame
    iframe = driver.find_element_by_class_name("sub-module-frame");  # 找到iframe
    driver.switch_to.frame(iframe);  # 进入iframe
    # 查看未签到的人数
    # data=driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[3]/div/div[2]/"
    #                                   "div[1]/div/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[7]/div/span");
    # 进入的每日详情
    driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[3]/div/div[2]/div[1]/div/"
                                 "div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[9]/div/a").click();
    time.sleep(3);
    # 导出所有未签到的学生的数据
    ##先查看未签到的所有同学
    driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[3]/div/div[2]/div[2]/div").click();
    ##选择导出
    driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[3]/div/div[2]/div[1]/div/"
                                 "div[4]/div/div[2]/div/div[1]/button/span/span").click();
    ###导出数据
    driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[3]/div/div[2]/div[1]/"
                                 "div/div[4]/div/div[2]/div/div[2]/ul[1]/li/span").click();
    time.sleep(4);
    print("下载成功")
    return 1;

#制造消息
def  makeMsg(filepath):
    df=pd.read_excel(filepath)
    x,y=df.shape;#现在一共有x人未打开
    msg = ""
    if x==0:
        return msg;
    for i in range(0, x):
        msg += df['班级'][i] + "  " + df['姓名'][i] + '\n'
    os.remove(filepath);#用完后删除
    return msg
'''  
 发送者的窗口，要发送的消息
send("明月清风","这是测试代码")
'''
def sendMsg(name,msg):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, msg)
    w.CloseClipboard()
    # 获取窗口句柄
    handle = win32gui.FindWindow(None, name)
    while True:
        # 填充消息
        win32gui.SendMessage(handle, 770, 0, 0)
        # 回车发送消息
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        time.sleep(30)
'''
供调用的函数
'''
#计算时间的函数
def nowTime():
    dt = datetime.datetime.now();
    hours=dt.hour;#小时[0,24]
    mins=dt.minute;#分钟[0,60]
    return hours*60+mins;
def final():
    #计算当前时间
    if(nowTime()>=420 and nowTime()<=750):
        task="晨";#晨间打卡
        filepath = "C:\\Users\\LiangHao\\Downloads\\学生健康晨间打卡.xlsx"
    elif nowTime()>=1140 and nowTime()<=1350:
        task="晚"
        filepath = "C:\\Users\\LiangHao\\Downloads\\学生健康晚间打卡.xlsx"
    else:
        sendEmail("任务分配失败","2609362670@qq.com");
        return;
    #配置文件
    user = "222018603193001"
    pwd = "206416";

    #下载未打卡名单
    if download(user,pwd,task)==0:
        sendEmail("下载名单失败", "2609362670@qq.com");
        return;
    #制作消息
    message=makeMsg(filepath);
    sendMsg("明月清风",message);#发送到哪个窗口
    time.sleep(4);
    return;
#发送通知邮件
def sendEmail(text,remail):
    smtp = "smtp.163.com";
    subject = "打卡"
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

if __name__ == '__main__':
    while True:
        if nowTime()>=480 and nowTime()<=780:
            final();#执行一次
            print("晨间打卡")
            time.sleep(1800);#1个小时后再次执行
        elif nowTime()>=1600 and nowTime()<=1350:
            final();
            print("晚间打卡")
            time.sleep(1800);  # 1个小时后再次执行
        else:
            print("不在打卡时间",datetime.datetime.now())
            time.sleep(7200);