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
####################
# Create Python-ACL#
####################
dev.send('config acl delete Python-ACL' + '\n')
time.sleep(1)
dev.send('config acl create Python-ACL' + '\n')
time.sleep(1)
#
# ACL Rule 1
dev.send('config acl rule add Python-ACL 1' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 1 both' + '\n')
time.sleep(1)
dev.send('config acl rule protocol Python-ACL 1 17' + '\n')
time.sleep(1)
dev.send('config acl rule destination port range Python-ACL 1 53 53' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 1 permit' + '\n')
time.sleep(1)
#
# ACL Rule 2
dev.send('config acl rule add Python-ACL 2' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 2 both' + '\n')
time.sleep(1)
dev.send('config acl rule protocol Python-ACL 2 17' + '\n')
time.sleep(1)
dev.send('config acl rule source port range Python-ACL 2 53 53' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 2 permit' + '\n')
time.sleep(1)
#
# ACL Rule 3
dev.send('config acl rule add Python-ACL 3' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 3 both' + '\n')
time.sleep(1)
dev.send('config acl rule destination address Python-ACL 3 172.16.145.0 255.255.255.0' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 3 deny' + '\n')
time.sleep(1)
#
# ACL Rule 4
dev.send('config acl rule add Python-ACL 4' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 4 both' + '\n')
time.sleep(1)
dev.send('config acl rule source address Python-ACL 4 172.16.145.0 255.255.255.0' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 4 deny' + '\n')
time.sleep(1)
#
# ACL Rule 5
dev.send('config acl rule add Python-ACL 5' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 5 both' + '\n')
time.sleep(1)
dev.send('config acl rule destination address Python-ACL 5 172.16.145.0 255.255.255.0' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 5 deny' + '\n')
time.sleep(1)
#
# ACL Rule 6
dev.send('config acl rule add Python-ACL 6' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 6 both' + '\n')
time.sleep(1)
dev.send('config acl rule source address Python-ACL 6 172.16.145.0 255.255.255.0' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 6 deny' + '\n')
time.sleep(1)
#
# ACL Rule 7
dev.send('config acl rule add Python-ACL 7' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 7 both' + '\n')
time.sleep(1)
dev.send('config acl rule destination address Python-ACL 7 192.168.17.0 255.255.255.0' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 7 deny' + '\n')
time.sleep(1)
#
# ACL Rule 8
dev.send('config acl rule add Python-ACL 8' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 8 both' + '\n')
time.sleep(1)
dev.send('config acl rule source address Python-ACL 8 192.168.17.0 255.255.255.0' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 8 deny' + '\n')
time.sleep(1)
#
# ACL Rule 9
dev.send('config acl rule add Python-ACL 9' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 9 both' + '\n')
time.sleep(1)
dev.send('config acl rule destination address Python-ACL 9 192.168.18.0 255.255.255.0' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 9 deny' + '\n')
time.sleep(1)
#
# ACL Rule 8
dev.send('config acl rule add Python-ACL 8' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 8 both' + '\n')
time.sleep(1)
dev.send('config acl rule source address Python-ACL 8 192.168.18.0 255.255.255.0' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 8 deny' + '\n')
time.sleep(1)
#
# ACL Rule 15
dev.send('config acl rule add Python-ACL 15' + '\n')
time.sleep(1)
dev.send('config acl rule direction Python-ACL 15 both' + '\n')
time.sleep(1)
dev.send('config acl rule action Python-ACL 15 permit' + '\n')
#
#######################
# Create TTI-Guest ACL#
#######################
dev.send('config acl delete TTI-Guest' + '\n')
time.sleep(1)
dev.send('config acl create TTI-Guest' + '\n')
time.sleep(1)
#
# ACL Rule 1
dev.send('config acl rule add TTI-Guest 1' + '\n')
time.sleep(1)
dev.send('config acl rule direction TTI-Guest 1 in' + '\n')
time.sleep(1)
dev.send('config acl rule protocol TTI-Guest 1 6' + '\n')
time.sleep(1)
dev.send('config acl rule source port range TTI-Guest 1 0 65535' + '\n')
time.sleep(1)
dev.send('config acl rule destination port range TTI-Guest 1 53 53' + '\n')
time.sleep(1)
dev.send('config acl rule action TTI-Guest 1 permit' + '\n')
time.sleep(1)
#
# ACL Rule 2
dev.send('config acl rule add TTI-Guest 2' + '\n')
time.sleep(1)
dev.send('config acl rule direction TTI-Guest 2 in' + '\n')
time.sleep(1)
dev.send('config acl rule protocol TTI-Guest 2 6' + '\n')
time.sleep(1)
dev.send('config acl rule source address TTI-Guest 2 172.16.145.90 255.255.255.255' + '\n')
time.sleep(1)
dev.send('config acl rule source port range TTI-Guest 2 0 65535' + '\n')
time.sleep(1)
dev.send('config acl rule source port range TTI-Guest 2 8443 8443' + '\n')
time.sleep(1)
dev.send('config acl rule action TTI-Guest 2 permit' + '\n')
time.sleep(1)
#
#
#
resp = dev.recv(99999)
print ('\n\n\n*** WLC ACL Added ***\n\n')
#print resp

