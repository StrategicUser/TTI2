import sys
import paramiko
import time
import base64
from getpass import getpass
from pprint import pprint
from sys import exit
from lxml import etree
import logging


ttiuser = 'cisco'
ttipass = 'cisco'
	

with open('files/lab-nexus-iplist.txt', 'r') as ccthost:
	for line in ccthost:																											
		line = line = line.strip().lower()
		print 'Username List for ' + line + '\n'
		commands = 'show run | include username'																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																													
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
		ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
		stdin, stdout, stderr = ssh.exec_command(commands)
		time.sleep(1)
		config_out = stdout.read().decode()
		ssh.close()
		print config_out
		print '\n\n'
		#config.write(config_out)


ttiuser = 'cisco'
ttipass = 'cisco'
	

with open('files/lab-ios-iplist.txt', 'r') as ccthost:
	for line in ccthost:																											
		line = line = line.strip().lower()
		print 'Username List for ' + line + '\n'
		commands = 'show run | include username'																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																													
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
		ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
		stdin, stdout, stderr = ssh.exec_command(commands)
		time.sleep(1)
		config_out = stdout.read().decode()
		ssh.close()
		print config_out
		print '\n\n'
		#config.write(config_out)