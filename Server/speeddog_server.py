"""SpeedDog Server"""
import subprocess

with subprocess.Popen(['iperf', '-s'], stdout=subprocess.PIPE) as server:

    EXIT_CODE = server.wait()

if EXIT_CODE is not None:
    raise SystemExit('Daemon failed')
