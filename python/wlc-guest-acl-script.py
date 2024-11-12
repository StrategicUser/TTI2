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
# Create TTI-Guest ACL#
#######################
dev.send('config acl delete TTI-Guest' + '\n')
dev.send('config acl create TTI-Guest' + '\n')
#
# ACL rule to allow access to DNS
dev.send('config acl rule add TTI-Guest 1' + '\n')
dev.send('config acl rule direction TTI-Guest 1 in' + '\n')
dev.send('config acl rule protocol TTI-Guest 1 17' + '\n')
dev.send('config acl rule source port range TTI-Guest 1 0 65535' + '\n')
dev.send('config acl rule destination port range TTI-Guest 1 53 53' + '\n')
dev.send('config acl rule action TTI-Guest 1 permit' + '\n')
time.sleep(1)
#
# ACL rule to allow Web redirection to ISE
dev.send('config acl rule add TTI-Guest 2' + '\n')
dev.send('config acl rule direction TTI-Guest 2 in' + '\n')
dev.send('config acl rule protocol TTI-Guest 2 6' + '\n')
dev.send('config acl rule source address TTI-Guest 2 172.16.145.90 255.255.255.255' + '\n')
dev.send('config acl rule source port range TTI-Guest 2 0 65535' + '\n')
dev.send('config acl rule destination port range TTI-Guest 2 8443 8443' + '\n')
dev.send('config acl rule action TTI-Guest 2 permit' + '\n')
time.sleep(1)
#
# ACL RFC1918 
dev.send('config acl rule add TTI-Guest 3' + '\n')
dev.send('config acl rule direction TTI-Guest 3 in' + '\n')
dev.send('config acl rule source port range TTI-Guest 3 0 65535' + '\n')
dev.send('config acl rule destination address TTI-Guest 3 10.0.0.0 255.0.0.0' + '\n')
dev.send('config acl rule destination port range TTI-Guest 3 0 65535' + '\n')
dev.send('config acl rule action TTI-Guest 3 deny' + '\n')
time.sleep(1)
dev.send('config acl rule add TTI-Guest 4' + '\n')
dev.send('config acl rule direction TTI-Guest 4 in' + '\n')
dev.send('config acl rule source port range TTI-Guest 4 0 65535' + '\n')
dev.send('config acl rule destination address TTI-Guest 4 172.16.0.0 255.255.240.0' + '\n')
dev.send('config acl rule destination port range TTI-Guest 4 0 65535' + '\n')
dev.send('config acl rule action TTI-Guest 4 deny' + '\n')
time.sleep(1)
dev.send('config acl rule add TTI-Guest 5' + '\n')
dev.send('config acl rule direction TTI-Guest 5 in' + '\n')
dev.send('config acl rule source port range TTI-Guest 5 0 65535' + '\n')
dev.send('config acl rule destination address TTI-Guest 5 192.168.0.0 255.255.0.0' + '\n')
dev.send('config acl rule destination port range TTI-Guest 5 0 65535' + '\n')
dev.send('config acl rule action TTI-Guest 5 deny' + '\n')
time.sleep(1)
#
# ACL rule to allow Internet access
dev.send('config acl rule add TTI-Guest 6' + '\n')
dev.send('config acl rule direction TTI-Guest 6 in' + '\n')
dev.send('config acl rule source port range TTI-Guest 6 0 65535' + '\n')
dev.send('config acl rule destination port range TTI-Guest 6 0 65535' + '\n')
dev.send('config acl rule action TTI-Guest 6 permit' + '\n')
time.sleep(1)
#
# ACL rule to allow access to DNS
dev.send('config acl rule add TTI-Guest 2' + '\n')
dev.send('config acl rule direction TTI-Guest 2 in' + '\n')
dev.send('config acl rule protocol TTI-Guest 2 17' + '\n')
dev.send('config acl rule destination port range TTI-Guest 2 0 65535' + '\n')
dev.send('config acl rule source port range TTI-Guest 2 53 53' + '\n')
dev.send('config acl rule action TTI-Guest 2 permit' + '\n')
time.sleep(1)
#
#######################
# Create Webauth-ACL ACL#
#######################
dev.send('config acl delete Webauth-ACL' + '\n')
dev.send('config acl create Webauth-ACL' + '\n')
#
# ACL rule to allow access to DNS
dev.send('config acl rule add Webauth-ACL 1' + '\n')
dev.send('config acl rule direction Webauth-ACL 1 in' + '\n')
dev.send('config acl rule protocol Webauth-ACL 1 17' + '\n')
dev.send('config acl rule source port range Webauth-ACL 1 0 65535' + '\n')
dev.send('config acl rule destination port range Webauth-ACL 1 53 53' + '\n')
dev.send('config acl rule action Webauth-ACL 1 permit' + '\n')
time.sleep(1)
dev.send('config acl rule add Webauth-ACL 2' + '\n')
dev.send('config acl rule direction Webauth-ACL 2 out' + '\n')
dev.send('config acl rule protocol Webauth-ACL 2 17' + '\n')
dev.send('config acl rule destination port range Webauth-ACL 2 0 65535' + '\n')
dev.send('config acl rule source port range Webauth-ACL 2 53 53' + '\n')
dev.send('config acl rule action Webauth-ACL 2 permit' + '\n')
time.sleep(1)
#
# ACL rule to allow access to DHCP
dev.send('config acl rule add Webauth-ACL 3' + '\n')
dev.send('config acl rule direction Webauth-ACL 3 out' + '\n')
dev.send('config acl rule protocol Webauth-ACL 3 17' + '\n')
dev.send('config acl rule source port range Webauth-ACL 3 67 67' + '\n')
dev.send('config acl rule destination port range Webauth-ACL 3 68 68' + '\n')
dev.send('config acl rule action Webauth-ACL 3 permit' + '\n')
time.sleep(1)
dev.send('config acl rule add Webauth-ACL 4' + '\n')
dev.send('config acl rule direction Webauth-ACL 4 in' + '\n')
dev.send('config acl rule protocol Webauth-ACL 4 17' + '\n')
dev.send('config acl rule destination port range Webauth-ACL 4 67 67' + '\n')
dev.send('config acl rule source port range Webauth-ACL 4 68 68' + '\n')
dev.send('config acl rule action Webauth-ACL 4 permit' + '\n')
time.sleep(1)
#
# ACL rule to allow Web redirection to ISE
dev.send('config acl rule add Webauth-ACL 5' + '\n')
dev.send('config acl rule direction Webauth-ACL 5 in' + '\n')
dev.send('config acl rule protocol Webauth-ACL 5 6' + '\n')
dev.send('config acl rule destination address Webauth-ACL 5 172.16.145.90 255.255.255.255' + '\n')
dev.send('config acl rule source port range Webauth-ACL 5 0 65535' + '\n')
dev.send('config acl rule destination port range Webauth-ACL 5 8905 8905' + '\n')
dev.send('config acl rule action Webauth-ACL 5 permit' + '\n')
time.sleep(1)
dev.send('config acl rule add Webauth-ACL 6' + '\n')
dev.send('config acl rule direction Webauth-ACL 6 out' + '\n')
dev.send('config acl rule protocol Webauth-ACL 6 6' + '\n')
dev.send('config acl rule source address Webauth-ACL 6 172.16.145.90 255.255.255.255' + '\n')
dev.send('config acl rule source port range Webauth-ACL 6 8905 8905' + '\n')
dev.send('config acl rule destination port range Webauth-ACL 6 0 65535' + '\n')
dev.send('config acl rule action Webauth-ACL 6 permit' + '\n')
time.sleep(1)
dev.send('config acl rule add Webauth-ACL 7' + '\n')
dev.send('config acl rule direction Webauth-ACL 7 in' + '\n')
dev.send('config acl rule protocol Webauth-ACL 7 6' + '\n')
dev.send('config acl rule destination address Webauth-ACL 7 172.16.145.90 255.255.255.255' + '\n')
dev.send('config acl rule source port range Webauth-ACL 7 0 65535' + '\n')
dev.send('config acl rule destination port range Webauth-ACL 7 8443 8443' + '\n')
dev.send('config acl rule action Webauth-ACL 7 permit' + '\n')
time.sleep(1)
dev.send('config acl rule add Webauth-ACL 8' + '\n')
dev.send('config acl rule direction Webauth-ACL 8 out' + '\n')
dev.send('config acl rule protocol Webauth-ACL 8 6' + '\n')
dev.send('config acl rule source address Webauth-ACL 8 172.16.145.90 255.255.255.255' + '\n')
dev.send('config acl rule source port range Webauth-ACL 8 8443 8443' + '\n')
dev.send('config acl rule destination port range Webauth-ACL 8 0 65535' + '\n')
dev.send('config acl rule action Webauth-ACL 8 permit' + '\n')
time.sleep(1)
dev.send('config acl rule add Webauth-ACL 9' + '\n')
dev.send('config acl rule source port range Webauth-ACL 9 0 65535' + '\n')
dev.send('config acl rule destination port range Webauth-ACL 9 0 65535' + '\n')
dev.send('config acl rule action Webauth-ACL 9 deny' + '\n')
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

