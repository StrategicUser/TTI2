import sys
import paramiko
import time
import base64
from getpass import getpass
from pprint import pprint
from sys import exit
from lxml import etree
import logging

logging.raiseExceptions=False		
max_buffer = 90000
def clear_buffer(ssh):
	if ssh.recv_ready():
		return ssh.recv(max_buffer)

passdict = []

with open('files/ttipasscore.txt', 'r') as epass:
	for line3 in epass:
		line3 = line3.strip()
		passdict.append(line3)

ttiuser = passdict[0]
ttipass = passdict[1]
	

with open('files/ios-iplist.txt', 'r') as ccthost:
	for line in ccthost:																											
		line = line = line.strip().lower()
		with open('files/' + line + '/' + line + '-trunk.txt', 'w') as f:
			commands = 'show interface trunk'																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																													
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
		 	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
			stdin, stdout, stderr = ssh.exec_command(commands)
		 	time.sleep(4)
			trunk_out = stdout.channel.recv(8000)
			ssh.close()
			#trunk_out.strip('Port')
			trunk_port = trunk_out.split()
			cnt = 0
			pos = '802.1q'
			while cnt <= (len(trunk_port) - 1):
				if pos == trunk_port[cnt]:
					acnt = cnt - 2
					f.write(trunk_port[acnt] + "\n")
				cnt = cnt + 1
			f.close()
			with open('files/tti-mac-table.txt', 'r') as tmac:
				for line1 in tmac:
					#line1 = line1 = line1.strip().lower()
					line1 = line1 = line1.strip()
					macadd = line1.split()
					commands = 'show mac address address ' + macadd[0]
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
				 	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
				 	time.sleep(1)
					stdin, stdout, stderr = ssh.exec_command(commands)
				 	time.sleep(4)
					mac_add = stdout.channel.recv(8000)
					#trunk_out.strip('Port')
					port = mac_add.split()
					ssh.close()		
					scnt = 0
					maccnt = 0
					cnt = 0
					while cnt <= (len(port) - 1):
						if macadd[0] == port[cnt]:
							acnt = cnt + 2
							switchport = port[acnt]
							scnt = 0
							with open('files/' + line + '/' + line + '-trunk.txt', 'r') as mac_tab:
								for line2 in mac_tab:
									line2 = line2.strip()	
									if switchport == line2:
										scnt =  1

							if scnt == 0:
								print switchport
								print line2
								port_des = macadd[1].replace("+", " ")	 
								print '**** Updating port description to ' + port_des + ' for ' + line + ' Interface ' + switchport + ' ****'
								#print switchport
								commands = ['config t\n', 'int ' + switchport + '\n', 'Description ' + port_des + '\n', 'end\n', '\n']
								ssh = paramiko.SSHClient()
								ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
 								ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
								ssh = ssh.invoke_shell()
								for command in commands:
									time.sleep(3)
									ssh.send(command)
								ssh.close()
								print '**** Completed Configuration for ' + line + ' ****\n\n'
							mac_tab.close()
						cnt = cnt + 1
			tmac.close()
		
						#ssh.close()
