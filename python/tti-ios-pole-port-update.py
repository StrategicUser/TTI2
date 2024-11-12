import sys
import paramiko
from netmiko.cisco import CiscoS300SSH
from netmiko import ConnectHandler
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


with open('files/ios-iplist.txt', 'r') as ccthost:
	for line in ccthost:																											
		line = line = line.strip().lower()
		with open('files/' + line + '/' + line + '-trunk.txt', 'w') as f:
			port9 = 'gi9'
			port10 = 'gi10'
			f.write(port9 + "\n")
			f.write(port10 + "\n")
		print '**** Reset the port descriptions on ' + line + '\n'
		ets_dev = {
		'device_type':'cisco_ios',
		'ip':line,
		'username':'cisco',
		'password':'cisco',
		}
		d_cnt = 0
		port_dclr = ['f0/1','f0/2','f0/3','f0/4','f0/5','f0/6','f0/7','f0/8']
		config_commands = ['interface ' + port_dclr[0] + '\n', 'no description\n','interface ' + port_dclr[1] + '\n','no description\n','interface ' + port_dclr[2] + '\n','no description\n','interface ' + port_dclr[3] + '\n','no description\n','interface ' + port_dclr[4] + '\n','no description\n','interface ' + port_dclr[5] + '\n','no description\n','interface ' + port_dclr[6] + '\n','no description\n','interface ' + port_dclr[7] + '\n','no description\n']
		net_connect=ConnectHandler(**ets_dev)
		output1=net_connect.send_config_set(config_commands)
		#net_connect.disconnect()
		print '**** Reset descriptions completed****\n\n'
		#d_cnt = d_cnt + 1																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																										
		with open('files/mac-ios-table.txt', 'r') as tmac:
			for line1 in tmac:
				line1 = line1 = line1.strip().lower()
				macadd = line1.split()
				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
			 	ssh.connect(line, username='cisco', password='cisco', look_for_keys=False, allow_agent=False)
			 	dev = ssh.invoke_shell()
			 	time.sleep(1)
			 	dev.send('terminal length 0\n')
				dev.send('show mac address address ' + macadd[0] + '\n')
				time.sleep(3)
				mac_add = dev.recv(99999)
				#print mac_add
				port = mac_add.split()
				ssh.close()
				net_connect.disconnect()
				scnt = 0
				maccnt = 0
				cnt = 14
				while cnt <= (len(port) - 1):
					if macadd[0] == port[cnt]:
						acnt = cnt + 2
						switchport = port[acnt]
						with open('files/' + line + '/' + line + '-trunk.txt', 'r') as mac_tab:
							for line2 in mac_tab:
								line2 = line2 = line2.strip()
								if switchport == line2:
									scnt =  1
								else:
									scnt = 0
						if scnt == 0:
							print '**** Updating Configuration for ' + line + '****'
							port_des = macadd[1].replace("-", " ")
							port_vlan = macadd[2]
							print '**** Update interface ' + switchport + ' - changing switchport to ' + port_vlan + '\n'
							ets_dev = {
							'device_type':'cisco_ios',
							'ip':line,
							'username':'cisco',
							'password':'cisco',
							}
							config_commands = ['interface ' + switchport + '\n','description ' + port_des + '\n','switchport mode access\n','switchport access vlan ' + port_vlan + '\n','end\n','copy running startup\n']
							net_connect=ConnectHandler(**ets_dev)
							output1=net_connect.send_config_set(config_commands)
							time.sleep(4)
							net_connect.disconnect()
							print '**** Completed Configuration for ' + line + '****\n\n'
					cnt = cnt + 1
		
		