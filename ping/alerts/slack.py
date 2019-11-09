from slack_webhook import Slack


def send(url, subject, body):
    slack = Slack(url=url)
    slack.post(text="*" + subject + "*\n\n" + body)
