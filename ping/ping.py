import os
import json
import logging

import coloredlogs

from .alerts import email as alert_email
from .alerts import slack as alert_slack
from .processors import ping_ipv4 as process_ping_ipv4
from .processors import ping_ipv6 as process_ping_ipv6
from .processors import https as process_https

settings = {}


def send_alert(site_name, check_type, message):
    for alert in settings["alerts"]:
        subject = "%s (%s)" % (site_name, check_type)
        body = "Failed check %s for %s:\n\n%s" % (check_type, site_name, message)

        if alert["type"] == "email":
            alert_email.send(alert["from"], alert["to"], subject, body)
        elif alert["type"] == "slack":
            alert_slack.send(alert["url"], subject, body)
        else:
            logging.error("Unknown alert type %s!" % alert["type"])


def check_site(site):
    logging.info("Processing " + site["name"] + "...")

    # Get the number of checks to perform
    checkCount = len(site["checks"])
    if checkCount == 0:
        logging.warning("No checks to perform!")
        return

    currentCheck = 0

    # Perform all checks for site
    for check in site["checks"]:
        currentCheck += 1
        logging.info("Performing check %s %d/%d..." % (check["type"], currentCheck, checkCount))

        # Skip check
        if not check["enabled"]:
            logging.info("Check is disabled.")

            continue

        # Default result value
        result = {
            "success": False,
            "message": None
        }

        # Perform check based on type
        if check["type"] == "ping_ipv4":
            result = process_ping_ipv4.process(check["options"])
        elif check["type"] == "ping_ipv6":
            result = process_ping_ipv6.process(check["options"])
        elif check["type"] == "https":
            result = process_https.process(check["options"])
        else:
            logging.error("Unknown check type %s!" % check["type"])

        # Send alert on error
        if not result["success"]:
            send_alert(site["name"], check["type"], result["message"])


if __name__ == "__main__":
    filename = os.path.dirname(os.path.realpath(__file__)) + "/../settings.json"

    try:
        with open(filename, mode="r") as f:
            settings = json.load(f)
    except json.JSONDecodeError as e:
        logging.critical("Invalid formatted settings file!")
        exit(1)

    coloredlogs.install(level=settings["logging"] if settings["logging"] else logging.WARNING)

    # Initialize alerts
    if settings["email"]:
        alert_email.init(settings["email"]["host"],
                         settings["email"]["port"],
                         settings["email"]["username"],
                         settings["email"]["password"])

    # Check sites
    for site in settings["sites"]:
        check_site(site)

    # Deinitialize alerts
    alert_email.close()

    logging.info("Done.")
    exit(0)
