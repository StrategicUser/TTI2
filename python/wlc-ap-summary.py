import paramiko
import time
import base64
import sys
import cmd
import json
import yaml
import os

cchost = sys.argv[1]
#device['ip']=cchost

cred = []
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
dev.send('show ap summary\n')
time.sleep(7)
resp = dev.recv(99999)
print ('\n\n\n\n          *** ' + cchost + ' AP summary Information ***\n\n')
print resp

