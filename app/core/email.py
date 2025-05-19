import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(to: str, subject: str, body: str) -> None:
    """
    发送邮件
    :param to: 收件人邮箱
    :param subject: 邮件主题
    :param body: 邮件内容
    """
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = f"E-DBA <{settings.SMTP_USER}>"  # 添加发件人名称
    msg['To'] = to
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain', 'utf-8'))  # 指定编码为utf-8

    try:
        # 连接SMTP服务器
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()  # 启用TLS加密
        
        # 登录
        logger.info(f"正在连接SMTP服务器: {settings.SMTP_HOST}:{settings.SMTP_PORT}")
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        logger.info("SMTP登录成功")
        
        # 发送邮件
        server.send_message(msg)
        logger.info(f"邮件发送成功: {to}")
        server.quit()
    except Exception as e:
        logger.error(f"发送邮件失败: {str(e)}")
        raise Exception(f"Failed to send email: {str(e)}")

def test_email_config():
    """
    测试邮件配置是否正确
    """
    try:
        logger.info("开始测试邮件配置...")
        logger.info(f"SMTP服务器: {settings.SMTP_HOST}")
        logger.info(f"SMTP端口: {settings.SMTP_PORT}")
        logger.info(f"SMTP用户: {settings.SMTP_USER}")
        
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.quit()
        
        logger.info("邮件配置测试成功！")
        return True
    except Exception as e:
        logger.error(f"邮件配置测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_email_config() 