"""Utils module for SpeedDog"""
import subprocess
from urllib.request import urlopen
from urllib.error import URLError
from re import match, IGNORECASE
from logs import log_warn

TEST_PAGE = 'https://google.com'


def check_internet():
    """Check if host has internet connection."""
    try:
        urlopen(TEST_PAGE, timeout=5)
    except URLError:
        log_warn(
            'No internet connection detected, emails with reports can not be sended.'
        )


def check_mail(mail: str) -> bool:
    """Check if mail address is valid

    Args:
        mail (str): mail address

    Returns:
        bool: True if valid, False if not
    """
    if match(
        '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[a-zA-Z]$)',
        mail,
        IGNORECASE,
    ):
        return True
    return False


def is_to_slow(speed: float, limit: float) -> bool:
    """Check if speed value is less than limit value.

    Args:
        speed (float): speed value
        limit (float): limit value

    Returns:
        bool: True if less than limit, False if more than limit.
    """
    return speed < limit


def stop_daemon():
    """Stop daemon"""
    with subprocess.Popen(
        ['systemctl', 'stop', 'speeddog-client'], stdout=subprocess.PIPE
    ) as stop_it:
        stop_it.wait()
    raise SystemExit()
