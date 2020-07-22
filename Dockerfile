FROM python:3.8

MAINTAINER VisualAppeal <tim@visualappeal.de>

RUN pip install poetry

COPY ping /ping/ping
COPY requirements.txt /ping/requirements.txt
COPY settings.json /ping/settings.json

WORKDIR /ping

RUN poetry install

CMD python3 -m ping.ping ping/ping.py
