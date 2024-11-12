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
time.sleep(2)
#
#######################
# Create TTI-Manager-ACL ACL#
#######################
dev.send('config acl delete TTI-Manager-ACL' + '\n')
dev.send('config acl create TTI-Manager-ACL' + '\n')
#
# ACL rule to restrict access to network devices 
dev.send('config acl rule add TTI-Manager-ACL 1' + '\n')
dev.send('config acl rule direction TTI-Manager-ACL 1 in' + '\n')
dev.send('config acl rule source port range TTI-Manager-ACL 1 0 65535' + '\n')
dev.send('config acl rule destination address TTI-Manager-ACL 1 10.200.250.0 255.255.255.0' + '\n')
dev.send('config acl rule destination port range TTI-Manager-ACL 1 0 65535' + '\n')
dev.send('config acl rule action TTI-Manager-ACL 1 deny' + '\n')
time.sleep(1)
#
# ACL rule to allow everywhere else
dev.send('config acl rule add TTI-Manager-ACL 2' + '\n')
dev.send('config acl rule direction TTI-Manager-ACL 2 in' + '\n')
dev.send('config acl rule source port range TTI-Manager-ACL 2 0 65535' + '\n')
dev.send('config acl rule destination port range TTI-Manager-ACL 2 0 65535' + '\n')
dev.send('config acl rule action TTI-Manager-ACL 2 permit' + '\n')
time.sleep(1)
#
#
#
dev.send('save config' + '\n')
time.sleep(1)
dev.send('y' + '\n')
time.sleep(8)
dev.send('show acl detailed TTI-Manager-ACL' + '\n')
time.sleep(3)
#
#
resp = dev.recv(99999)
print ('\n\n\n*** WLC ACL Added ***\n\n')
print resp

