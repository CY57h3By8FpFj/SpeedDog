"""SpeedDog client"""
from time import sleep
from config import AppConfig
from speed import get_speed
from mail import send_limit_alert
from logs import log_info, log_warn
from utils import check_internet, is_to_slow


SDOG_SRV = AppConfig.SDOG_SRV
LIMIT = AppConfig.LIMIT
RP_SPEED = AppConfig.RP_SPEED
INTERVAL = AppConfig.INTERVAL

while True:
    check_internet()
    speed_value = get_speed(SDOG_SRV)
    if speed_value is not None:
        log_info(f'Link speed to {SDOG_SRV} - {speed_value} Gbps')
        if is_to_slow(speed=speed_value, limit=LIMIT):
            log_warn(f'Speed is below the LIMIT: {LIMIT} Gbps, current speed {speed_value} Gbps')
            if RP_SPEED:
                send_limit_alert(speed_value=speed_value, limit_value=LIMIT)
    log_info(f'Wait {INTERVAL} min.')
    sleep(INTERVAL * 60)
