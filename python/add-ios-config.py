#!/usr/bin/env python
# Update Cisco IOS Device Configuration 
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
	
	with open('files/passcore.txt', 'r') as epass:
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
	temp1 = os.system("cat /home/strategic/TTI/python/files/config.txt > /home/strategic/TTI/python/files/final_config.txt")
	temp2 = os.system("cat /home/strategic/TTI/python/files/trunk_intf.txt >> /home/strategic/TTI/python/files/final_config.txt")
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
def setConfigSSH(line, ttiuser, ttipass):
	"""use paramiko to ssh into the switch"""
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
	ssh = ssh.invoke_shell()
	command = "config t\n"
	ssh.send(command)
	time.sleep(1)
	ssh.send(command)
	with open('/home/strategic/TTI/python/files/final_config.txt', 'r') as config:
		for line in config:																											
			line = line = line.strip().lower()
			command = line + "\n"
			ssh.send(command)
	time.sleep(1)
	command = "end\n"
	ssh.send(command)
	command = "copy run start\n"
	ssh.send(command)
	time.sleep(2)
	command = "\n"
	ssh.send(command)
	time.sleep(1)
	command = "\n"
	ssh.send(command)
	ssh.close()
	return
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
		print("Updating Switch - " + line + "\n")
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
					f.write("switchport trunk allowed vlan add 120 \n")
					f.write("!\n")
				cnt = cnt + 1
		f.close()
		#
		#
		setConfig(line)
		#
		# Update Device Configuration
		setConfigSSH(line, ttiuser, ttipass)
		# 

		#
#  ------------
#  End Main
#  ------------
