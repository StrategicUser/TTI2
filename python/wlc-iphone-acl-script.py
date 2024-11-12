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
# Create TTI-IPhone ACL#
#######################
dev.send('config acl delete TTI-IPhone' + '\n')
dev.send('config acl create TTI-IPhone' + '\n')
#
# ACL rule to allow access to DNS
dev.send('config acl rule add TTI-IPhone 1' + '\n')
dev.send('config acl rule direction TTI-IPhone 1 in' + '\n')
dev.send('config acl rule protocol TTI-IPhone 1 17' + '\n')
dev.send('config acl rule source port range TTI-IPhone 1 0 65535' + '\n')
dev.send('config acl rule destination port range TTI-IPhone 1 53 53' + '\n')
dev.send('config acl rule action TTI-IPhone 1 permit' + '\n')
time.sleep(1)
#
# ACL rule to allow Web redirection to ISE
dev.send('config acl rule add TTI-IPhone 2' + '\n')
dev.send('config acl rule direction TTI-IPhone 2 in' + '\n')
dev.send('config acl rule protocol TTI-IPhone 2 6' + '\n')
dev.send('config acl rule source address TTI-IPhone 2 172.16.145.90 255.255.255.255' + '\n')
dev.send('config acl rule source port range TTI-IPhone 2 0 65535' + '\n')
dev.send('config acl rule destination port range TTI-IPhone 2 8443 8443' + '\n')
dev.send('config acl rule action TTI-IPhone 2 permit' + '\n')
time.sleep(1)
#
# ACL RFC1918 
dev.send('config acl rule add TTI-IPhone 3' + '\n')
dev.send('config acl rule direction TTI-IPhone 3 in' + '\n')
dev.send('config acl rule source port range TTI-IPhone 3 0 65535' + '\n')
dev.send('config acl rule destination address TTI-IPhone 3 10.0.0.0 255.0.0.0' + '\n')
dev.send('config acl rule destination port range TTI-IPhone 3 0 65535' + '\n')
dev.send('config acl rule action TTI-IPhone 3 deny' + '\n')
time.sleep(1)
dev.send('config acl rule add TTI-IPhone 4' + '\n')
dev.send('config acl rule direction TTI-IPhone 4 in' + '\n')
dev.send('config acl rule source port range TTI-IPhone 4 0 65535' + '\n')
dev.send('config acl rule destination address TTI-IPhone 4 172.16.0.0 255.255.240.0' + '\n')
dev.send('config acl rule destination port range TTI-IPhone 4 0 65535' + '\n')
dev.send('config acl rule action TTI-IPhone 4 deny' + '\n')
time.sleep(1)
dev.send('config acl rule add TTI-IPhone 5' + '\n')
dev.send('config acl rule direction TTI-IPhone 5 in' + '\n')
dev.send('config acl rule source port range TTI-IPhone 5 0 65535' + '\n')
dev.send('config acl rule destination address TTI-IPhone 5 192.168.0.0 255.255.0.0' + '\n')
dev.send('config acl rule destination port range TTI-IPhone 5 0 65535' + '\n')
dev.send('config acl rule action TTI-IPhone 5 deny' + '\n')
time.sleep(1)
#
# ACL rule to allow Internet access
dev.send('config acl rule add TTI-IPhone 6' + '\n')
dev.send('config acl rule direction TTI-IPhone 6 in' + '\n')
dev.send('config acl rule source port range TTI-IPhone 6 0 65535' + '\n')
dev.send('config acl rule destination port range TTI-IPhone 6 0 65535' + '\n')
dev.send('config acl rule action TTI-IPhone 6 permit' + '\n')
time.sleep(1)
#
# ACL rule to allow access to DNS
dev.send('config acl rule add TTI-IPhone 2' + '\n')
dev.send('config acl rule direction TTI-IPhone 2 in' + '\n')
dev.send('config acl rule protocol TTI-IPhone 2 17' + '\n')
dev.send('config acl rule destination port range TTI-IPhone 2 0 65535' + '\n')
dev.send('config acl rule source port range TTI-IPhone 2 53 53' + '\n')
dev.send('config acl rule action TTI-IPhone 2 permit' + '\n')
time.sleep(1)
#
#
dev.send('config save config' + '\n')
time.sleep(1)
dev.send('y' + '\n')
time.sleep(8)
dev.send('show acl detailed Webauth-ACL' + '\n')
time.sleep(3)
#
#
resp = dev.recv(99999)
print ('\n\n\n*** WLC ACL Added ***\n\n')
print resp

