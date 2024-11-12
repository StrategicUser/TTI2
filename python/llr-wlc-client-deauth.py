import paramiko
import time
import base64
import sys
import cmd
import json
import yaml
import os



cchost = 'sss-wlc'
#
cred = []
#
#print ('\n\n*** Accessing ' + cchost + ' credentials from encrypted database *** \n\n')
with open('/home/strategic/TTI/python/files/' + cchost + '-cred.txt', 'r') as login:
	for line in login:
		line = line.replace("\n", "")
		cred.append(line)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(cchost, username=cred[0], password=cred[1], look_for_keys=False, allow_agent=False)
dev = ssh.invoke_shell()
time.sleep(0.1)
dev.send(cred[0] + '\n')
time.sleep(0.1)
dev.send(cred[1] + '\n')
time.sleep(0.1)
dev.send('config paging disable' + '\n')
dev.send('debug disable-all' + '\n')
dev.send('clear msglog' + '\n')
dev.send('y' + '\n')
time.sleep(3)
#
##############################
# Deauthenticate Client#
##############################
dev.send('config client deauthenticate 98:2c:bc:c6:ca:0a' + '\n')
#print ('\n\n\n*** WLC MAC Address Added ***\n\n')
#
#
resp = dev.recv(99999)
print ('\n\n\n*** WLC Client 98:2c:bc:c6:ca:0a Deauthenticated ***\n\n')
#print resp

