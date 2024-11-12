#!/usr/bin/env python3
# S-Cone-device-mgmt.py
# Strategic Service Solutions, Inc.

#####################################
#
#
#
# 1)Ping S-Cone WAN
# 2)Ping Devices on LAN
# 3)Connect to LAN services (SSH, FTP, Web Browser, etc) 
#
#
#
#
#
#
#
#
#
#
#

######################################
########### Modules ###########33
#####################################
import os
import subprocess
import paramiko

####################################
########## Variables ##############
####################################
sconeWanIp = ''


#####################################
######## Functions ###############
#######################################
def pingWan():
	command = subprocess.check_output(
	['ping', '-n', '2', '10.8.0.7'],
	stderr=subprocess.STDOUT, #get all output
	universal_newlines=True # return string not bytes
)

def pingLanDevice():
	command = subprocess.run(["ssh", "strategicuser@10.0.2.108"])
    



def sshDevice():
	command = subprocess.run(["ssh", "strategicuser@10.0.2.108"])


def winScp

def launchBrowser



================================

wanResponse = subprocess.check_output(
	['ping', '-n', '2', '10.8.0.7'],
	stderr=subprocess.STDOUT, #get all output
	universal_newlines=True # return string not bytes
)


completed = subprocess.run(['ls', '-1'])
print('returncode:', completed.returncode)


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ip, port=1337, username='root', password=pw)
print('[*] Connected successfully')

stdin, stdout, stderr = client.exec_command('ls -l')