
# SpeedDog

Systemd daemon for checking the speed between two hosts and reporting (by email) when the speed is below the required limit.

## Table of contents
* [Introduction](#Introduction)
* [Installation](#Installation)
* [Configuration](#Configuration)
* [Usage/Examples](#Usage/Examples)
* [Technologies](#Technologies)

## Introduction
For SpeedDog to work properly, you need to run two instances of SpeedDog, a server and a client. Install SpeedDog in server mode on one host and in client mode on the other. Both hosts must be on the same network or routable between them. Iperf is used to measure the speed.


## Installation
### Install from source
SpeedDog operates in one of two modes, server or client. To install in which mode, use the `-m` parameter `[server or client]`.

+ Download repo
```
git clone https://github.com/CY57h3By8FpFj/SpeedDog
```
+ Go to the cloned folder
```
cd SpeedDog
```
+ Run the installation (as root)
```
python3 install.py -m [mode] 
```
+ DONE

### Install the deb package
+ Download deb package from [releases](https://github.com/CY57h3By8FpFj/SpeedDog/releases) (use wget or similar)
+ Install with apt

## Configuration
Configuration is only necessary for client mode. All configuration parameters are stored in the `SpeedDog.conf` file in the `/etc/SpeedDog` folder. 

### List of config parameters

#### Base config
`SRV_DOG` - IP address of SpeedDog server\
`INTERVAL` - time in minutes between speed tests\
`LIMIT` - minimum speed for connection between client and server

#### Reports config
`RP_ERRORS` - send mail on error\
`RP_LIMIT` - send mail when speed is below limit

#### Mail config
`RECEIVER` - email address to send messages\
`SMTP_HOST` - host address for SMTP server\
`SMTO_PORT` - port for SMTP server\
`SMTP_USER` - username for SMTP server\
`SMTP_PASS` - password for SMTP server

## Usage/Examples
SpeedDog is a systemd daemon, run it like any other daemon.\
\
For the client (as root):
```
systemctl start speeddog-client
```
For the server (as root):
```
systemctl start speeddog-server
```

## Technologies
SpeedDog - `python`  
Unit file - `bash`

Binaries:\
`iperf` - [https://iperf.fr/](https://iperf.fr/)

