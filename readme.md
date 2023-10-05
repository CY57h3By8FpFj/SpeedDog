
# SpeedDog

Systemd daemon to check speed between two host and report (email) if speed value is less than required limit.

## Table of contents
* [Introduction](#Introduction)
* [Installation](#Installation)
* [Configuration](#Configuration)
* [Usage/Examples](#Usage/Examples)
* [Technologies](#Technologies)

## Introduction
For correct work, you must run two instances of SpeedDog, server and client. On the one host install SpeedDog in server mode on the second host install SpeedDog in client mode. Both host must be in the same network or routable between it. For speed  measure used is Iperf.

## Installation
SpeddDog works in two modes server or client. 
To install mode what you want use:
-m parameter `[server or client]`

+ Download repo
```
git clone https://github.com/CY57h3By8FpFj/SpeedDog
```
+ Enter to cloned folder
```
cd SpeddDog
```
+ Run installation (as root)
```
python3 install.py -m [mode] 
```
+ DONE

## Configuration
Configuration is needed only for client mode. All config parameters are stored in `.env` file in `/opt/SpeedDog` folder. 

### List of config parameters

#### Base Config
`SRV_DOG` - IP address for SpeedDog server\
`INTERVAL` - time in minutes between speed tests\
`LIMIT` - minimal speed for link between client and server

#### Reports config
`RP_ERRORS` - send mail if errors\
`RP_LIMIT` - send mail if speed has less than limit

#### Mail config
`RECEIVER` - Email address to send messages\
`SMTP_HOST` - Host address for SMTP server\
`SMTO_PORT` - Port for SMTP server\
`SMTP_USER` - Username for SMTP server\
`SMTP_PASS` - Password for SMTP server\

## Usage/Examples
SpeedDog works as systemd daemon, run it like others daemons.\
\
For client (as root):
```
systemctl start speeddog-client
```
For server (as root):
```
systemctl start speeddog-server
```

## Technologies
SpeedDog - `python`  
Unit file - `bash`

Binaries:\
`iperf` - [https://iperf.fr/](https://iperf.fr/)

