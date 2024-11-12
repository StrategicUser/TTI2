#!/usr/bin/env python
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
# ----------------------
# Main Program
# ----------------------
#
# Call Password Function and retrieve Username and Password for file.
plist = setPass()
username = plist[0]
password = plist[1]
host = 'ttilgb_admin_6513_a'
#
#
ipfile=open("/home/strategic/TTI/python/files/tti-telnet-iplist.txt")
#
for line in ipfile:
	host=line.strip("\n")
	#
	"""use telnetlib to telnet into the switch"""
	tn = telnetlib.Telnet(host)
	tn.open(host)
	#username, password = getCredentials()
	#username
	tn.read_until(b"Username: ")
	tn.write(username.encode("ascii") + b"\n")
	#password
	tn.read_until(b"Password: ")
	tn.write(password.encode("ascii") + b"\n")
	#	
	with open('/home/strategic/TTI/python/files/' + host + '/' + host + '.cfg', 'r') as conf:
		for line2 in conf:
			line2 = line2.strip()
			tn.write(line2 + "\n")
			time.sleep(1)
	#tn.write("exit\n")
	conf.close()
	#
	tn.close()
ipfile.close()
