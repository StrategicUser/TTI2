#!/usr/bin/env python
# Update Ansible Role Configuration File
# Strategic Service Solutions, Inc.
import sys
import os
import subprocess
import paramiko
import time
import base64
from getpass import getpass
from pprint import pprint
from sys import exit
from lxml import etree
import logging
#  ---------------------
#  Clear Buffer Function
#  ---------------------
def clear_buffer(ssh):
	if ssh.recv_ready():
		return ssh.recv(max_buffer)
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Network Device Password Function
#  --------------------------------
def setPass():
	passdict = []
	
	with open('files/ttipasscore.txt', 'r') as epass:
		for line3 in epass:
			line3 = line3.strip()
			passdict.append(line3)
	
	ttiuser = passdict[0]
	ttipass = passdict[1]
	return(ttiuser, ttipass)	
#  ------------
#  End Function
#  ------------
#	
#  --------------------------------
#  Network Add Trunk interface Configuration Function
#  --------------------------------
def setConfig(line):
	cdp_temp2 = os.system("cat /home/strategic/TTI/python/files/trunk_intf.txt >> /home/strategic/TTI/ansible/roles/" + line + "/files/" + line + "-config.cfg")
#
#
	return()
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Network Device Trunk Function
#  --------------------------------
def setTrunk(line, ttiuser, ttipass):
	commands = 'show interface trunk'																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																													
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
	stdin, stdout, stderr = ssh.exec_command(commands)
	trunk_out = stdout.read().decode()
	ssh.close()
	#trunk_out.strip('Port')
	return(trunk_out)
#  ------------
#  End Function
#  ------------
#
#
#  -----------------------------------
#  Main
#  -----------------------------------
logging.raiseExceptions=False		
max_buffer = 90000
trunk_list = []
#
# Call Password Function and retrieve Username and Password for file.
plist = setPass()
ttiuser = plist[0]
ttipass = plist[1]
#
# Open file that contains network devices config file that will be updated.
with open('files/ios-iplist.txt', 'r') as ccthost:
	for line in ccthost:																											
		line = line = line.strip().lower()
		#
		# Retrieve network device Trunk information. Then create a List that 
		# contains the Trunk Interfaces, and write to the proper file.
		with open('files/trunk_intf.txt', 'w') as f:
			trunk_out = setTrunk(line, ttiuser, ttipass)
			trunk_port = trunk_out.split()
			cnt = 0
			pos = '802.1q'
			while cnt <= (len(trunk_port) - 1):
				if pos == trunk_port[cnt]:
					acnt = cnt - 2
					f.write("\n")
					f.write("int " + trunk_port[acnt] + "\n")
					f.write("ip dhcp snooping trust \n")
					f.write("!\n")
				cnt = cnt + 1
		f.close()
		#
		#
		# Update the Ansible Role Config file
		setConfig(line)
		# 

		#
#  ------------
#  End Main
#  ------------
