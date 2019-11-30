# Ping

Website, server, certificate uptime/validation monitor.

## Install

* `python3 -m venv venv`
* `source venv/bin/activate` 
* `pip install -r requirements.txt`
* `cp settings.example.json settings.json`

## Run

`python3 -m ping.ping ping/ping.py`

## Example cronjob

`0	*	*	*	*	cd /opt/ping-python/ && source venv/bin/activate && python3 -m ping.ping ping/ping.py &>> /var/log/ping-python.log`
