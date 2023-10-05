"""Speed module"""
import subprocess
from mail import send_error_alert
from config import AppConfig
from logs import log_error


def __run_speed_test(server_ip: str) -> str:
    """Run Iperf as subprocess for speed test

    Args:
        server_ip (str): Server host address as IP

    Returns:
        str: Return stdout from Iperf or NONE if any errors
    """
    command = f'iperf -c {server_ip} -y C'

    with subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as client:
        stdout, stderr = client.communicate()
        errcode = client.returncode
        stdout = stdout.decode('UTF-8').strip()
        stderr = stderr.decode('UTF-8').strip()

        if errcode != 0:
            serror = f'Error - {stderr}'
            if AppConfig.RP_ERRORS:
                send_error_alert(error_message=serror)
            log_error('Failed to run IPERF')
            log_error(serror)
            return None

        if len(stderr) != 0:
            serror = f'Error - {stderr}'
            if AppConfig.RP_ERRORS:
                send_error_alert(error_message=serror)
            log_error(f'Failed connect to {server_ip}')
            log_error(serror)
            return None

        return stdout


def __read_speed(stdout_data: str) -> int:
    """Extract speed value from output data from Iperf

    Args:
        stdout_data (str): Output data from Iperf

    Returns:
        str: Speed value or None if error.
    """
    speed = stdout_data[stdout_data.rfind(',') + 1 :]
    try:
        speed = int(speed)
    except ValueError as err:
        serror = f'Error read speed value - {err}'
        if AppConfig.RP_ERRORS:
            send_error_alert(error_message=serror)
        log_error(serror)
        return None
    return speed


def __convert_speed_to_human_redable_in_Gbps(speed: int) -> float:
    """Convert speed value to Gbps for human redable value.

    Args:
        speed (int): Speed value

    Returns:
        float: Speed value as Gbps
    """
    human_speed = speed / 1000000000
    human_speed = round(human_speed, 2)
    return human_speed


def get_speed(server_ip: str) -> float:
    """Get speed value from Iperf output data.

    Args:
        server_ip (str): IP address for SpeedDog server

    Returns:
        float: Speed value as float round to 2 places after comma in Gbps or NONE if any errors
    """
    stdout_data = __run_speed_test(server_ip=server_ip)
    if stdout_data is None:
        return None
    speed = __read_speed(stdout_data=stdout_data)
    if speed is None:
        return None
    human_speed = __convert_speed_to_human_redable_in_Gbps(speed=speed)
    return human_speed
