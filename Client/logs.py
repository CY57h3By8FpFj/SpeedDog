"""Logs module for SpeedDog"""
import syslog

APP_NAME = "SpeedDog"


def log_error(err_msg: str):
    """Write ERROR to syslog

    Args:
        err_msg (str): error message
    """
    syslog.openlog(ident=APP_NAME)
    syslog.syslog(syslog.LOG_ERR, str(err_msg))
    syslog.closelog()


def log_info(inf_msg: str):
    """Write INFO to syslog

    Args:
        inf_msg (str): info message
    """
    syslog.openlog(ident=APP_NAME)
    syslog.syslog(syslog.LOG_INFO, str(inf_msg))
    syslog.closelog()


def log_warn(warn_msg: str):
    """Write WARN to syslog

    Args:
        warn_msg (str): info message
    """
    syslog.openlog(ident=APP_NAME)
    syslog.syslog(syslog.LOG_WARNING, str(warn_msg))
    syslog.closelog()


def log_config_error(parameter: str):
    """Write config file ERROR to syslog

    Args:
        parameter (str): parameter who has raise error
    """
    syslog.openlog(ident=APP_NAME)
    syslog.syslog(
        syslog.LOG_ERR,
        f'Error - {parameter} parameter in config file is not valid.',
    )
    syslog.closelog()
