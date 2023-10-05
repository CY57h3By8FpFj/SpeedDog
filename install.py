"""SpeedDog installer"""
import argparse
from os import geteuid, getcwd, path
from shutil import which, copy, copytree, ignore_patterns

# CONFIG
MODE_SERVER = 'SERVER'
MODE_CLIENT = 'CLIENT'
APP_NAME = 'SpeedDog'
CURRENT_PATH = getcwd()
SRV_DIR = '/Server/'
CLI_DIR = '/Client/'
CONF_DIR = 'config'
UNIT_DIR = 'unit'
SRV_UNIT_FILE = 'speeddog-server.service'
CLI_UNIT_FILE = 'speeddog-client.service'
SRV_UNIT_PATH = SRV_DIR + UNIT_DIR + '//' + SRV_UNIT_FILE
CLI_UNIT_PATH = CLI_DIR + UNIT_DIR + '//' + CLI_UNIT_FILE
INSTALL_PATH = '/opt/SpeedDog/'
SYSTEMD_UNIT_PATH = '/etc/systemd/system/'
CONFIG_PATH_DST = '/etc/SpeedDog/'
CONFIG_PATH_SRC = '/config/'


# COLORS
class Colors:
    """Color define"""

    BLUE = '\033[34m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    PURPLE = '\033[35m'
    ENDC = '\033[m'


def print_line():
    """Print line with colors"""
    print(
        Colors.YELLOW
        + '-' * 5
        + Colors.ENDC
        + Colors.CYAN
        + '-' * 50
        + Colors.ENDC
        + Colors.YELLOW
        + '-' * 5
        + Colors.ENDC
    )


def print_app_title(install_mode: str):
    """Print title line"""
    print_line()
    print(
        'Install '
        + Colors.PURPLE
        + APP_NAME
        + Colors.ENDC
        + ' as '
        + install_mode
    )
    print_line()


def print_config_info():
    """Print info about complete config"""
    print_line()
    print('Before run SpeedDog please complete config file:')
    print(Colors.CYAN + 'nano /etc/SpeedDog/SpeedDog.conf' + Colors.ENDC)


def print_all_ok():
    """Print all ok line"""
    print_line()
    print(Colors.GREEN + 'ALL OK' + Colors.ENDC)


def print_footer(install_mode: str):
    """Print footer line"""
    print_line()
    print('Type: ')
    print(
        Colors.CYAN
        + 'systemctl enable speeddog-'
        + install_mode.lower()
        + '.service'
        + Colors.ENDC
        + ' - to enable service.'
    )
    print(
        Colors.CYAN
        + 'systemctl start speeddog-'
        + install_mode.lower()
        + '.service'
        + Colors.ENDC
        + ' - to start service.'
    )
    print_line()


def print_ok():
    """Print OK"""
    print(Colors.GREEN + 'OK' + Colors.ENDC)


def print_fail():
    """Print FAIL"""
    print(Colors.RED + 'FAIL' + Colors.ENDC)


def print_phrase(phrase: str):
    """Print phrase"""
    print(Colors.YELLOW + phrase + ' ... ' + Colors.ENDC, end='')


def check_root_permission():
    """Check if script is running with root permission"""
    print_phrase('Check root')
    uid = geteuid()
    if uid != 0:
        print_fail()
        raise (
            SystemExit(
                'Run this script as root: '
                + Colors.CYAN
                + 'sudo python3 install.py -m [mode]'
                + Colors.ENDC
            )
        )
    print_ok()


def check_iperf():
    """Check if Iperf is installed"""
    print_phrase('Check Iperf')
    iperf_path = which('iperf')
    if iperf_path is None:
        print_fail()
        raise (
            SystemExit(
                'Please install iperf: '
                + Colors.CYAN
                + 'apt install iperf '
                + Colors.ENDC
            )
        )
    print_ok()


def check_for_previously_installation():
    """Check if exist old installation"""
    # === check folder in /opt
    print_phrase('Check previously installation')
    if path.exists(INSTALL_PATH):
        print_fail()
        raise (
            SystemExit(
                'Directory exist. Check '
                + Colors.CYAN
                + INSTALL_PATH
                + Colors.ENDC
            )
        )
    # ===  SRV unit file in systemd path
    if path.exists(SYSTEMD_UNIT_PATH + SRV_UNIT_FILE):
        print_fail()
        raise (
            SystemExit(
                'File exist. Check '
                + Colors.CYAN
                + SYSTEMD_UNIT_PATH
                + SRV_UNIT_FILE
                + Colors.ENDC
            )
        )

    # === CLI unit file in systemd path
    if path.exists(SYSTEMD_UNIT_PATH + CLI_UNIT_FILE):
        print_fail()
        raise (
            SystemExit(
                'File exist. Check '
                + Colors.CYAN
                + SYSTEMD_UNIT_PATH
                + CLI_UNIT_FILE
                + Colors.ENDC
            )
        )

    # === Config path
    if path.exists(CONFIG_PATH_DST):
        print_fail()
        raise (
            SystemExit(
                'Directory exist. Check '
                + Colors.CYAN
                + CONFIG_PATH_DST
                + Colors.ENDC
            )
        )

    print_ok()


def innstall_app(install_mode: str):
    """Copy all files to install path

    Args:
        install_mode (str): installation mode
    """
    print_phrase('Install app')
    try:
        if install_mode == MODE_CLIENT:
            copytree(
                CURRENT_PATH + CLI_DIR,
                INSTALL_PATH,
                ignore=ignore_patterns(CONF_DIR, UNIT_DIR),
            )
            copytree(CURRENT_PATH + CLI_DIR + CONFIG_PATH_SRC, CONFIG_PATH_DST)
        if install_mode == MODE_SERVER:
            copytree(
                CURRENT_PATH + SRV_DIR,
                INSTALL_PATH,
                ignore=ignore_patterns(UNIT_DIR),
            )
    except Exception as err:
        print_fail()
        raise (SystemExit(err)) from err
    print_ok()


def install_daemon(install_mode: str):
    """Copy unit file to systemd path

    Args:
        install_mode (str): installation mode
    """
    print_phrase('Install daemon file')
    try:
        if install_mode == MODE_CLIENT:
            copy(CURRENT_PATH + CLI_UNIT_PATH, SYSTEMD_UNIT_PATH)
        if install_mode == MODE_SERVER:
            copy(CURRENT_PATH + SRV_UNIT_PATH, SYSTEMD_UNIT_PATH)
    except Exception as err:
        print_fail()
        raise (SystemExit(err)) from err
    print_ok()


# PARSE ARGS
parser = argparse.ArgumentParser(description='SpeedDog installer.')
parser.add_argument(
    '-m',
    '--mode',
    required=True,
    help='Select mode of installation [client or server]',
)
args = vars(parser.parse_args())
mode = args['mode'].upper()

# INSTALL APP
if mode in ('SERVER', 'CLIENT'):
    print_app_title(install_mode=mode)
    check_root_permission()
    check_iperf()
    check_for_previously_installation()
    innstall_app(install_mode=mode)
    install_daemon(install_mode=mode)
    print_all_ok()
    if mode == MODE_CLIENT:
        print_config_info()
    print_footer(install_mode=mode)
else:
    raise SystemExit(
        'Use correct options for parameter -m --mode '
        + Colors.CYAN
        + 'server or client'
        + Colors.ENDC
    )
