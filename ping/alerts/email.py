import smtplib
from email.mime.text import MIMEText
import logging

smtp_server = None


def init(host, port, username, password):
    global smtp_server

    smtp_server = smtplib.SMTP_SSL(host, port)
    smtp_server.login(username, password)


def send(sender, target, subject, text):
    if smtp_server is None:
        logging.error("Email server not initialized!")
        return

    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = target

    smtp_server.sendmail(sender, target, msg.as_string())


def close():
    if smtp_server is not None:
        smtp_server.quit()
