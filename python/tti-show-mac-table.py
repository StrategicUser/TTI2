import sys
import os
import paramiko
import time
import base64
from getpass import getpass
from pprint import pprint
from sys import exit
from lxml import etree
import logging



ttiuser = 'admin'
ttipass = 'TTI.cisc0'
	

with open('files/ios-iplist.txt', 'r') as ccthost:
	for line in ccthost:																											
		line = line = line.strip().lower()
		with open('files/mac-table.txt', 'w') as config:
			commands = 'show mac address'																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																													
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
		 	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
			stdin, stdout, stderr = ssh.exec_command(commands)
		 	time.sleep(1)
			config_out = stdout.read().decode()
			ssh.close()
			#print config_out
			config.write(config_out)
		config.close()

		mac_final = os.system("cat files/mac_temp.txt \
		                                            | sed -n 's/dynamic/dynamic/gp'  \
		                                            | sed '/vPC/d' \
		                                            | sed '/Po/d'  \
		                                            | awk '{print $3, " " $7}' > files/tti-mac-table.txt")
ccthost.close()