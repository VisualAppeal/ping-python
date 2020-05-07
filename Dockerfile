FROM python:3.8

MAINTAINER VisualAppeal <tim@visualappeal.de>

COPY ping /ping/ping
COPY requirements.txt /ping/requirements.txt
COPY settings.json /ping/settings.json

WORKDIR /ping

RUN pip3 install -r requirements.txt

CMD python3 -m ping.ping ping/ping.py
