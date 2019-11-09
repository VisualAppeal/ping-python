import platform
import subprocess
import logging


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', '-4', '-i', '3', host]

    return subprocess.run(command, capture_output=True)


def process(site):
    result = ping(site["ip"])
    if result.returncode != 0:
        logging.warning("Could not ping %s" % site["ip"])

    return {
        "success": result.returncode == 0,
        "message": (result.stdout + result.stderr).decode('UTF-8')
    }
