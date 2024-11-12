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
mac_add = raw_input("Enter the WiFi Client MAC Address: ")
#print ('\n\n*** Accessing ' + cchost + ' credentials from encrypted database *** \n\n')
with open('/home/sssuser/TTI/python/files/' + cchost + '-cred.txt', 'r') as login:
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
time.sleep(5)
dev.send('show client detail ' + mac_add + '\n')
time.sleep(20)
dev.send('debug client ' + mac_add + '\n')
time.sleep(60)
dev.send('show msglog' + '\n')
time.sleep(35)
dev.send('debug disable-all' + '\n')
resp = dev.recv(99999)
print ('\n\n\n*** Show Client Detail and Debug Information ***\n\n')
print resp

