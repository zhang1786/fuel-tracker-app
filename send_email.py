import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_attachment(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain'))

    # 添加附件
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {os.path.basename(attachment_path)}'
    )
    msg.attach(part)

    # 连接到SMTP服务器并发送邮件
    try:
        # 使用QQ邮箱的SMTP服务器
        smtp_server = "smtp.qq.com"
        port = 587
        
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # 启用加密传输
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
        print(f"邮件已成功发送到 {receiver_email}")
        return True
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False

# 邮件配置
sender_email = "clawd_bot@foxmail.com"  # 发件人邮箱
sender_password = os.getenv("EMAIL_PASSWORD")  # 发件人邮箱密码或授权码
receiver_email = "172657125@qq.com"  # 收件人邮箱
subject = "谈心谈话记录表"
body = "您好，附件是谈心谈话记录表，包含6条谈话内容，请查收。"

# 发送邮件
send_email_with_attachment(sender_email, sender_password, receiver_email, subject, body, "谈心谈话记录.xlsx")