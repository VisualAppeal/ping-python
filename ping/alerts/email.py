import smtplib
from email.mime.text import MIMEText
import logging

smtp_server = None


def init(host, port, username, password):
    global smtp_server

    try:
        smtp_server = smtplib.SMTP_SSL(host, port)
        smtp_server.login(username, password)
    except Exception as e:
        logging.error('Could not connect to email server!')
        raise e


def send(sender, target, subject, text):
    global smtp_server

    if smtp_server is None:
        logging.error("Email server not initialized!")
        return

    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = target

    smtp_server.sendmail(sender, target, msg.as_string())


def close():
    global smtp_server

    if smtp_server is None:
        logging.error("Email server not initialized!")
        return

    smtp_server.quit()
