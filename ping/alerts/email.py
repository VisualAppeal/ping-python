import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
import logging
import socket

smtp_server: SMTP_SSL


def init(host, port, username, password):
    global smtp_server

    socket.setdefaulttimeout(10)

    try:
        smtp_server = SMTP_SSL(host, port)
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

    try:
        smtp_server.quit()
    except smtplib.SMTPServerDisconnected:
        logging.warning("Could not close smtp connection.")
