import configparser
import os
import mail
from wxpy import *

# 切换当前工作路径
os.chdir('/data/wx_bot')

cf = configparser.ConfigParser()
cf.read('config.int')
user_info = {
    'sendEmail': cf.get('e-mail', 'sendEmail'),
    'receiveEmail': cf.get('e-mail', 'receiveEmail'),
    'username': cf.get('e-mail', 'username'),
    'password': cf.get('e-mail', 'password'),
    'smtpPort': cf.getint('e-mail', 'smtpPort'),
    'smtpSendServer': cf.get('e-mail', 'smtpSendServer')
}
mail.connect_email(user_info)

# mail用法
# msg = mail.Message('发件人', 'receiver', '1/21313', '!~sad123')
# msg.send_email(user_info)

bot = Bot(cache_path=True)
myself = bot.self

bot.enable_puid('wxpy_puid.pkl')
bot.registered.disable()
need_received_message = bot.groups().search('4班通知公告群（禁水）')


@bot.register([Friend, Group])
def auto_reply(msg):
    # 如果是群聊，但没有被 @，则不回复
    if isinstance(msg.chat, Group) and not msg.is_at and not (msg.sender in need_received_message):
        return
    else:
        if msg.type is 'Recording' or msg.type is 'Attachment' or msg.type is 'Video':
            return '请发送文字消息，方便消息转发至邮箱，如遇急事请电联'
        else:
            type(msg)
            try:
                email = mail.Message(msg.member.name, msg.receiver.name, msg.sender.name, msg.text)
                email.send_email(user_info)
            except:
                email = mail.Message(msg.sender.name, msg.receiver.name, msg.sender.name, msg.text)
                email.send_email(user_info)
            return


embed()
