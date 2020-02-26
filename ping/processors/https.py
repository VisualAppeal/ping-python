import logging
from urllib.request import ssl, socket
from urllib.parse import urlparse
from datetime import datetime, timezone
from dateutil import parser

import requests


def check_http(url, timeout=3, validate_ssl=True):
    logging.debug("Validating url %s for SSL errors" % url)

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.SSLError as e:
        if not validate_ssl:
            logging.info("Ignoring ssl error: %s" % e)

            return {
                "success": True,
                "message": str(e)
            }

        logging.warning(e)

        return {
            "success": False,
            "message": str(e)
        }
    except requests.exceptions.HTTPError as e:
        logging.warning(e)

        return {
            "success": False,
            "message": str(e)
        }

    logging.debug("No HTTP error.")

    return {
        "success": True,
        "message": None
    }


def check_ssl_expiration(url, days):
    logging.debug("Check certificate expiration for %s" % url)

    parsed_uri = urlparse(url)
    hostname = '{uri.netloc}'.format(uri=parsed_uri)
    PORT = 443
    context = ssl.create_default_context()

    with socket.create_connection((hostname, PORT), timeout=3) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert_details = ssock.getpeercert()

            if not "notAfter" in cert_details:
                return {
                    "success": False,
                    "message": "No 'notAfter' field in certificate!"
                }

            not_after = parser.parse(cert_details["notAfter"])
            diff_days = (not_after - datetime.now(timezone.utc)).days

            logging.debug("Certificate valid for %d days." % diff_days)

            if diff_days < days:
                return {
                    "success": False,
                    "message": "Certificate for %s only valid for %d days!" % (url, diff_days)
                }

            return {
                "success": True,
                "message": None
            }


def process(site):
    success = True
    message = []

    for url in site["urls"]:
        result = check_http(
            url,
            site["timeout"] if "timeout" in site else 3,
            site["validate_ssl"] if "validate_ssl" in site else False
        )

        if not result["success"]:
            success = False
            message.append(result["message"])

        if "validate_ssl_expiration_days" in site:
            result = check_ssl_expiration(url, site["validate_ssl_expiration_days"])
            if not result["success"]:
                success = False
                message.append(result["message"])

    return {
        "success": success,
        "message": "\n\n".join(message)
    }
