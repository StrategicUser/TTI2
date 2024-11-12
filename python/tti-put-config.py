#!/usr/bin/env python
# Strategic Service Solutions, Inc.
import sys
import os
import csv
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
#
#  -------------------------------------------
#  Function that Writes Configuration to NVRAM
#  -------------------------------------------
def setConnect(line, ttiuser, ttipass):
	"""use paramiko to ssh into the switch"""
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
	ssh = ssh.invoke_shell()
	command = 'copy running startup'
	ssh.send(command)
	time.sleep(1)
	command = '\n'
	ssh.send(command)
	time.sleep(1)
	command = '\n'
	ssh.send(command)
	time.sleep(1)
	ssh.close()
	return
#  ------------
#  End Function
#  ------------
#


def getIntf(line, ttiuser, ttipass, macadd):
	#global ssh
	global intf
	with open('files/' + line + '-mactab.txt', 'w') as mactab:
		commands = 'show mac address address ' + macadd
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
		ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
		stdin, stdout, stderr = ssh.exec_command(commands)
		mac_list = stdout.read().decode()
		mactab.write(mac_list)
		mactab.close()
		ssh.close()
	#
	#
	iflag = 0
	with open('files/' + line + '-mactab.txt', 'r') as intf_tab:
		for line1 in intf_tab:
			line1 = line1.strip()
			intf_list = line1.split()
			if macadd in line1:
				if 'Po' in line1:
					print '*** Port-Channel Interface ***'
				else:
					intf = intf_list[3]
					iflag = 1
	#
	if iflag == 0:
		intf = 'NoInt'
	return
#  ------------
#  End Function
#  ------------
#
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
#gige = 'Gi'
#faste = 'Fe'
#portc = 'Po'
cflag = 0
#
# Open file that contains network devices that will be updated.
with open('files/tti-retrive-device.txt', 'r') as ttidevice:
	for line3 in ttidevice:
		line3 = line3 = line3.strip().lower()
		with open('files/iosxe-iplist.txt', 'r') as ccthost:
			for line in ccthost:																											
				line = line = line.strip().lower()
				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
				ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
				ssh = ssh.invoke_shell()
				#
				with open('files/' + line3 + '/' + line3 + '-config.txt', 'r') as final_data:
					for line1 in final_data:
						line1 = line1.strip()
						if '.' in line1:
							#cflag = 1
							getIntf(line, ttiuser, ttipass, line1)
							if intf == 'NoInt':
								cflag = 1
								print '*** No MAC Address Match for ' + line1
							else:
								command = "config t\n"
								ssh.send(command)
								command = "interface " + intf
								ssh.send(command)
								command = "\n"
								ssh.send(command)
								time.sleep(1)
								cflag = 0
								#print intf
						else:
							if cflag == 0:
								command = line1	+ "\n"
								ssh.send(command)
								time.sleep(1)
		
				setConnect(line, ttiuser, ttipass)
			print "***Completed Interface Configuration***"
			#cflag = cflag + 1
			ssh.close()
	ttidevice.close()

