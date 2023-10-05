"""Mail module for SpeedDog"""
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from socket import gaierror
from config import AppConfig
from logs import log_error


SMTP_HOST = AppConfig.SMTP_HOST
SMTP_PORT = AppConfig.SMTP_PORT
SMTP_USER = AppConfig.SMTP_USER
SMTP_PASS = AppConfig.SMTP_PASS
RECEIVER = AppConfig.RECEIVER
CLIENT_HOSTNAME = AppConfig.CLIENT_HOSTNAME
SDOG_SRV = AppConfig.SDOG_SRV


def __send_mail(message: MIMEText):
    """Send mail StartTLS

    Args:
        message (str): message to send
    """

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, RECEIVER, message.as_string())
    except smtplib.SMTPHeloError as err:
        log_error('SMTP server refused connection.')
        log_error(str(err))
    except smtplib.SMTPAuthenticationError as err:
        log_error('SMTP Authentication error.')
        log_error(str(err))
    except gaierror as err:
        log_error('Can not connect to the SMTP server.')
        log_error(str(err))
    except smtplib.SMTPNotSupportedError as err:
        log_error('This auth method is not supported by the SMTP server.')
        log_error(str(err))
    except smtplib.SMTPRecipientsRefused as err:
        log_error('Recipient address are refused by the SMTP server.')
        log_error(str(err))
    except smtplib.SMTPSenderRefused as err:
        log_error('Sender address refused by the SMTP server.')
        log_error(str(err))
    except smtplib.SMTPException as err:
        log_error('SMTP server error.')
        log_error(str(err))


def send_limit_alert(speed_value: float, limit_value: float):
    """Send mail whel speed value is less than limit value.

    Args:
        speed_value (float): speed value
        limit_value (float): limit value
    """

    now = datetime.now()
    current_datatime = now.strftime('%Y-%m-%d %H:%M:%S')

    message = MIMEText(
        f"""Limit value: {str(limit_value)} Gbps
Current speed: {str(speed_value)} Gbps
Client: {CLIENT_HOSTNAME}
Server: {SDOG_SRV}
Time on client: {current_datatime}"""
    )
    message['Subject'] = f'SpeedDog | Speed alert [{CLIENT_HOSTNAME}]'
    message['From'] = SMTP_USER
    message['To'] = RECEIVER
    __send_mail(message=message)


def send_error_alert(error_message: str):
    """Send mail with error message

    Args:
        error_message (string): message with error
    """
    now = datetime.now()
    current_datatime = now.strftime('%Y-%m-%d %H:%M:%S')

    message = MIMEText(
        f"""{error_message}\nClient: {CLIENT_HOSTNAME}\nTime on client: {current_datatime}"""
    )

    message['Subject'] = f'SpeedDog | Error alert [{CLIENT_HOSTNAME}]'
    message['From'] = SMTP_USER
    message['To'] = RECEIVER
    __send_mail(message=message)
