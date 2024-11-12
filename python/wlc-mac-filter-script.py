import paramiko
import time
import base64
import sys
import cmd
import json
import yaml
import os

cchost = sys.argv[1]
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
# Create Python-MAC Filtering#
##############################
dev.send('config macfilter add 98:2c:bc:c6:ca:0a 1 ems-yard' + '\n')
print ('\n\n\n*** WLC MAC Address Added ***\n\n')
time.sleep(600)
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
dev.send('config macfilter delete 98:2c:bc:c6:ca:0a' + '\n')
#
resp = dev.recv(99999)
print ('\n\n\n*** WLC MAC Address Removed ***\n\n')
#print resp

