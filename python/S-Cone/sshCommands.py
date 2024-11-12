#FOR TESTING - NOT NEEDED FOR BUILD

#!/usr/bin/env/ python

# Module to send ssh commands on S-Cone #

import subprocess
import paramiko
import settings


# Variables
#ssh = paramiko.SSHClient()

def pingNat(ip):

    settings.init()
    print(dir(settings.ssh.exec_command('ping -c 2 ' + ip)))
    stdin, stdout, stderr = settings.ssh.exec_command('ping -c 2 ' + ip)

def scrape(command):

    #'iw wlan0 link | grep signal && ifconfig eth0 | grep 192 && date'
    stdin, stdout, stderr = ssh.exec_command(command)

    return stdout 