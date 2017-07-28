import smtplib
from email.mime.text import MIMEText
from email.header import Header

smtp_obj = smtplib.SMTP()


def connect_email(user_info):
    smtp_obj.connect(user_info['smtpSendServer'], user_info['smtpPort'])
    smtp_obj.login(user_info['username'], user_info['password'])


class Message(object):
    def __init__(self, originator, receiver, subject, content):
        self.msg = MIMEText(content, 'plain', 'utf-8')
        self.msg['From'] = Header(originator, 'utf-8')
        self.msg['To'] = Header(receiver, 'utf-8')
        self.msg['Subject'] = Header(subject, 'utf-8')

    def send_email(self, user_info):
        smtp_obj.sendmail(user_info['sendEmail'], user_info['receiveEmail'], self.msg.as_string())
