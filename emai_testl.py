import smtplib
from email.mime.text import MIMEText
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
if __name__ == '__main__':
    text="Hello"
    remail="2609362670@qq.com"
    sendEmail(text,remail)