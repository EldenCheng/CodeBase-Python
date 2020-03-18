import logging
import re
import poplib
import time
from email.header import decode_header
from email.utils import parseaddr
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from email.utils import parseaddr

config_alias = dict()

config_alias['POP3 Server'] = 'pop3.mxhichina.com'

def decode_str(s):
    """
        解码邮件的subject或recipients
        :param s: 邮件中待解码的subject或recipients
        :return: 解码后的subject或recipients
        """
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    logging.debug(charset)
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        m = re.search(r'(?<=charset=)(?=").*?(?=")', content_type)
        if m is not None:
            charset = m.group(0)
        else:
            charset = re.search(r'(?<=charset=)\S+', content_type).group(0)
    return charset


def _parse_email(msg, is_get_content=True, init=True, email_message=None):
    """
       :param msg:
       :param is_get_content: 是否获取邮件正文内容
       :param init: 是否为初次调用该方法，递归时赋值为False
       :param email_message: 返回的邮件内容，包含From/ To/ Subject,当get_content为True时，则也会返回邮件的正文内容
       :return:
       """
    if init:
        email_message = dict()  # 返回的邮件内容，默认是返回
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    # 需要解码Subject字符串:
                    value = decode_str(value)
                    email_message[header] = value
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
                    email_message[header] = value

    if is_get_content:
        # 如果邮件对象是一个MIMEMultipart,
        if msg.is_multipart():
            # get_payload()返回list，包含所有的子对象:
            parts = msg.get_payload()
            for part in parts:
                # 递归每一个子对象:
                _parse_email(part, init=False, email_message=email_message)
        else:
            # 邮件对象不是一个MIMEMultipart, 根据content_type判断:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                # 纯文本或HTML内容:
                content = msg.get_payload(decode=True)
                # 要检测文本编码:
                charset = guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                if email_message.get('content'):
                    email_message['content'].append(content)
                else:
                    email_message['content'] = [content]
            else:
                # 不是文本,作为附件处理:
                # email_message['attachment'] = content_type
                logging.debug('Attachment')

    return email_message


def get_specific_email_content(user_account: str, password: str, recipients: str, subject: str = None,
                               more_flag: bool = False, limit_number: int=5):
    """
           :param user_account: 查看邮件的邮箱地址
           :param password: 该邮箱密码
           :param recipients: 收件人的email地址 格式' <xxx@xxx.com>' 注意有空格
           :param subject: 标题
           :param more_flag: 是否寻找多封一样标题的邮件
           :param limit_number: 寻找邮件数量的上限
           :return: content_list 返回包含邮件内容的列表e.g[{from:xxx,to:xxx,subject:xxx, content:xxxx}]     server：POP3服务器
           """

    content_list = list()
    pop3_server = config_alias['POP3 Server']

    # 开始连接到服务器
    try:
        # 连接到POP3服务器,有些邮箱服务器需要ssl加密，可以使用poplib.POP3_SSL
        # telnetlib.Telnet('pop.163.com', 995)
        server = poplib.POP3_SSL(pop3_server, 995, timeout=10)
    except Exception:
        time.sleep(5)
        server = poplib.POP3(pop3_server, 110, timeout=10)

    # 打开或者关闭调试信息，为打开，会在控制台打印客户端与服务器的交互信息
    server.set_debuglevel(0)

    # 打印POP3服务器的欢迎文字，验证是否正确连接到了邮件服务器
    logging.debug(server.getwelcome().decode('utf8'))

    # 开始进行身份验证
    server.user(user_account)
    server.pass_(password)

    logging.debug('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似['1 82923', '2 2184', ...]
    logging.debug(mails)
    # 获取所有邮件的收件人和subject:

    '''
    @Elden on 11/5/2019
    limit_number参数原来的作用是在more flag为Turn的情况下限制返回的email content的数量
    但在我们的script里基本没有用到这个功能, 鉴于有时候邮箱有太多邮件, 但我们实际上是不需要检查所有的邮件的,
    因此借用limit_number来限制要检查邮件的数量
    '''
    index = len(mails) + 1
    if limit_number == 0:
        end = 1
    else:
        end = index - limit_number
        if end < 1:
            end = 1

    for i in reversed(range(end, index)):
        resp, lines, octets = server.retr(i)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('gb18030', errors='ignore')
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        content = _parse_email(msg)
        '''
        @Elden on 11/5/2019
        下面的对比条件中有些小问题, 所以在原代码基础上加上去空格功能
        以免解释出来的收件人与主题的前后包含的空格令到对比失败
        '''
        logging.info("第{0}封邮件: TO: {1} Subject: {2}".format(i, content['To'], content['Subject']))
        if more_flag:
            if content['To'].strip() == '<' + recipients.strip() + '>':
                if subject:
                    if content['Subject'].strip() == subject.strip():
                        content_list.append(content)
                else:
                    content_list.append(content)
                if len(content_list) >= limit_number:
                    break
        else:
            if content['To'].strip() == '<' + recipients.strip() + '>':
                if subject:
                    if content['Subject'].strip() == subject.strip():
                        content['index'] = i
                        content_list.append(content)
                        break
                else:
                    content['index'] = i
                    content_list.append(content)
                    break
    return content_list, server