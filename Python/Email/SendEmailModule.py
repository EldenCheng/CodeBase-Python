import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os


def send_mail(smtp_info: dict, send_content: dict, send_to: list, attach_files=None):
    try:
        # 如果没有寄送地址的话,就把发送回自己的地址
        send_to = send_content['send_from'] if not send_to else send_to

        msg = MIMEMultipart()
        msg['From'] = send_content['send_from']
        msg['To'] = send_content['send_to']
        msg['Subject'] = send_content['subject']

        msg.attach(MIMEText(send_content['text']))

        for f in attach_files or []:
            with open(f, "rb") as fil:
                ext = f.split('.')[-1:]
                attachedfile = MIMEApplication(fil.read(), _subtype=ext)
                attachedfile.add_header('content-disposition', 'attachment', filename=os.path.basename(f))
            msg.attach(attachedfile)

        smtp = smtplib.SMTP(host=smtp_info['server'], port=25 if not smtp_info['port'] else smtp_info['port'])
        smtp.starttls()
        smtp.login(smtp_info['username'],smtp_info['password'])
        smtp.sendmail(send_content['send_from'], send_to, msg.as_string())
        smtp.close()
    except Exception as msg:
        print(msg)


if __name__ == "__main__":
    smtp_info = dict()
    send_content = dict()
    send_to = list()
    files = list()
    smtp_info['server'] = "smtp.mxhichina.com"
    smtp_info['port'] = 25
    smtp_info['username'] = "elden@mcgods.top"
    smtp_info['password'] = "Wesoft1234"
    send_to.append("elden.zheng@wesoft.com")
    send_to.append("leo.liu@wesoft.com")
    send_content["send_from"] = "elden@mcgods.top"
    send_content["send_to"] = "elden.zheng@wesoft.com;leo.liu@wesoft.com"
    send_content["subject"] = "The subject of Python Email Test"
    send_content["text"] = "<h1>The text of the Python Email Test<h1>"
    files.append("./Report.xlsx")

    send_mail(smtp_info, send_content, send_to, attach_files=files)





