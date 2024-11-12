#!/usr/bin/env python
# S-Cone.py
# Strategic Service Solutions, Inc.
import sys
import os
import subprocess
import paramiko
import telnetlib
import time
import base64
from getpass import getpass
from pprint import pprint
from sys import exit
from lxml import etree
import logging
#
#
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
#  Network Device Trunk Function
#  --------------------------------
def setTrunk(tn):
	tn.write("show int trunk\n")
	time.sleep(7)
	output = tn.read_very_eager()
	print output
	return
#  ------------
#  End Function
#  ------------
#
# ----------------------
# Main Program
# ----------------------
#
# Call Password Function and retrieve Username and Password for file.
plist = setPass()
username = plist[0]
password = plist[1]
host = '172.16.145.250'
#username = 'cisco'
#password = 'cisco'
#
"""use telnetlib to telnet into the switch"""
tn = telnetlib.Telnet(host)
tn.open(host)
#username, password = getCredentials()
#username
tn.read_until(b"Username: ")
tn.write(username.encode("ascii") + b"\n")
#password
if password:
	tn.read_until(b"Password: ")
	tn.write(password.encode("ascii") + b"\n")
#
#
tn.write("terminal length 0\n")
tn.write("show mac address\n")
time.sleep(7)
#tn.write("exit\n")
#
#tn.write("vt100\n")
output = tn.read_very_eager().decode('ascii')
print output
setTrunk(tn)
tn.close()