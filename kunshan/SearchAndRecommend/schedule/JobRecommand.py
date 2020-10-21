from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
from SearchAndRecommend.schedule.SchedulerConfig import mySchedule
from datetime import datetime

sender='csw92700@163.com'
password='OHAQPGXDIHYQVXAM'
receivers=["563796159@qq.com"]
smtpServer='smtp.163.com'


#邮件设置
# mail_msg = """
# <p>Python 邮件发送测试...</p>
# <p><a href="http://www.runoob.com">这是一个链接</a></p>
# """
# message = MIMEText(mail_msg, 'html', 'utf-8')
# message['From'] = Header("菜鸟教程", 'utf-8')
# message['to'] =  Header("测试", 'utf-8')
# subject = 'Python SMTP 邮件测试'
# message['Subject'] = Header(subject, 'utf-8')
msg=MIMEText('填写邮件内容','plain','utf-8')
msg['From']=formataddr(["FromRunoob",sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
msg['To']=formataddr(["FK",receivers[0]])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
msg['Subject']="菜鸟教程发送邮件测试"                # 邮件的主题，也可以说是标题


def login():
    server = smtplib.SMTP(smtpServer,25)
    server.set_debuglevel(1)
    server.login(sender,password)
    print("log success")
    return server

def sendEmail():
    try:
        for receiver in receivers:
            server = smtplib.SMTP(smtpServer, 25)
            server.set_debuglevel(1)
            server.login(sender, password)
            print("log success")
            server.sendmail(sender,receiver,msg.as_string())
            print("邮件发送成功")
            server.quit()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    return

def sendWeChat():
    pass

def loopSendEmail():
    nowTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(nowTime)
    scheduler = mySchedule()
    scheduler.add_job(sendEmail,"interval",seconds=10)
    scheduler.start()

if __name__=="__main__":
    loopSendEmail()