"""MODULE CONFIG"""
from configparser import ConfigParser
from ipaddress import ip_address
from socket import gethostname
from os import path
from utils import check_mail, stop_daemon
from logs import log_config_error, log_error

CONFIG_FILE_PATH = '/etc/SpeedDog/config/SpeedDog.conf'

if path.exists(CONFIG_FILE_PATH) is not True:
    log_error(
        'Config file not exist, reinstall program or create config file.'
    )
    stop_daemon()

config = ConfigParser()
config.read(CONFIG_FILE_PATH)


class AppConfig:
    """Config class"""

    # ===APP CONFIG===
    try:
        SDOG_SRV = ip_address(config.get('CLIENT_CONFIG', 'SDOG_SRV'))
    except ValueError as err:
        log_config_error('SDOG_SRV')
        stop_daemon()

    try:
        INTERVAL = config.getint('CLIENT_CONFIG', 'INTERVAL')
        if INTERVAL < 5:
            log_error("INTERVAL value is less than minimum time. (5 minute)")
    except ValueError as err:
        log_config_error('INTERVAL')
        stop_daemon()

    try:
        LIMIT = config.getfloat('CLIENT_CONFIG', 'LIMIT')
    except ValueError as err:
        log_config_error('LIMIT')
        stop_daemon()

    # ===REPORT CONFIG===
    try:
        RP_ERRORS = config.getboolean('REPORTS', 'RP_ERRORS')
    except ValueError as err:
        log_config_error('RP_ERRORS')
        stop_daemon()

    try:
        RP_SPEED = config.getboolean('REPORTS', 'RP_SPEED')
    except ValueError as err:
        log_config_error('RP_SPEED')
        stop_daemon()

    # ===MAIL CONFIG===
    RECEIVER = config.get('MAIL', 'RECEIVER')
    if RP_SPEED is True or RP_ERRORS is True:
        if check_mail(RECEIVER) is False:
            log_config_error('RECEIVER')
            stop_daemon()

    SMTP_HOST = config.get('MAIL', 'SMTP_HOST')
    if RP_SPEED is True or RP_ERRORS is True:
        if len(SMTP_HOST) == 0:
            log_config_error('SMTP_HOST')
            stop_daemon()

    try:
        if RP_SPEED is True or RP_ERRORS is True:
            SMTP_PORT = config.getint('MAIL', 'SMTP_PORT')
    except ValueError as err:
        log_config_error('SMTP_PORT')
        stop_daemon()

    SMTP_USER = config.get('MAIL', 'SMTP_USER')
    if RP_SPEED is True or RP_ERRORS is True:
        if len(SMTP_USER) == 0:
            log_config_error('SMTP_USER')
            stop_daemon()

    SMTP_PASS = config.get('MAIL', 'SMTP_PASS')
    if RP_SPEED is True or RP_ERRORS is True:
        if len(SMTP_PASS) == 0:
            log_config_error('SMTP_USER')
            stop_daemon()

    # ===HOSTNAME===
    try:
        CLIENT_HOSTNAME = gethostname()
    except Exception as err:
        log_config_error('CLIENT_HOSTNAME')
        stop_daemon()
