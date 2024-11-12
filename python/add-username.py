#!/usr/bin/env python
# Strategic Service Solutions, Inc.
import sys
import os
import csv
import subprocess
import paramiko
import time
import telnetlib
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
	
	with open('files/labpasscore.txt', 'r') as epass:
		for line in epass:
			line = line.strip()
			passdict.append(line)
	
	ttiuser = passdict[0]
	ttipass = passdict[1]
	return(ttiuser, ttipass)	
#  ------------
#  End Function
#  ------------

def setUsernameSSH(line, ttiuser, ttipass):
	"""use paramiko to ssh into the switch"""
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
	ssh = ssh.invoke_shell()																										
	command = "config t\n"
	ssh.send(command)
	command = "username ttiadmin password TTI.cisc0\n"
	ssh.send(command)
	time.sleep(2)
	command = '\n'
	ssh.send(command)
	command = "username ttiadmin privilege 15\n"
	ssh.send(command)
	time.sleep(1)
	command = 'exit\n'
	ssh.send(command)
	time.sleep(1)
	command = 'copy running startup'
	ssh.send(command)
	time.sleep(2)
	command = '\n'
	ssh.send(command)
	time.sleep(1)
	command = '\n'
	ssh.send(command)
	ssh.close()
	return
#  ------------
#  End Function
#  ------------

def setUsernameTelnet(line, username, password):
	#
	"""use telnetlib to telnet into the switch"""
	tn = telnetlib.Telnet(line)
	tn.open(line)
	#username, password = getCredentials()
	#username
	tn.read_until(b"Username: ")
	tn.write(username.encode("ascii") + b"\n")
	#password
	tn.read_until(b"Password: ")
	tn.write(password.encode("ascii") + b"\n")
	#
	command="config t\n"
	tn.write(command)
	command="username ttiadmin password TTI.cisc0\n"
	tn.write(command + "\n")
	time.sleep(2)
	command="\n"
	tn.write(command)
	command="username ttiadmin privilege 15\n"
	tn.write(command + "\n")
	time.sleep(1)
	command="exit\n"
	tn.write(command)
	command="copy running startup\n"
	tn.write(command)
	time.sleep(1)
	command="\n"
	tn.write(command)
	time.sleep(1)	
	tn.close()
	return
#  ------------
#  End Function
#  ------------
#  Main
#  -----------------------------------
logging.raiseExceptions=False		
max_buffer = 90000
#
# Call Password Function and retrieve Username and Password for file.
plist = setPass()
ttiuser = plist[0]
ttipass = plist[1]
#
# Open file that contains ssh network devices that will be updated.
with open('files/lab-ios-iplist.txt', 'r') as ttidevice:
	for line in ttidevice:
		line = line = line.strip().lower()
		print ("Add Username ttiadmin to " + line + "***\n")
		setUsernameSSH(line, ttiuser, ttipass)
	ttidevice.close()
#
# Open file that contains telnet network devices that will be updated.
with open('files/lab-telnet-ios-iplist.txt', 'r') as ttidevice1:
	for line in ttidevice1:
		line = line = line.strip().lower()
		print ("Add Username ttiadmin to " + line + "***\n")
		setUsernameTelnet(line, ttiuser, ttipass)
	ttidevice.close()
#
#