import sys
import os
import subprocess
import paramiko
import time
import base64
from getpass import getpass
from pprint import pprint
from sys import exit
from lxml import etree
import logging
#  ---------------------
#  Clear Buffer Function
#  ---------------------
def clear_buffer(ssh):
	if ssh.recv_ready():
		return ssh.recv(max_buffer)
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Network Device Password Function
#  --------------------------------
def setPass():
	passdict = []
	
	with open('files/ttipasscore.txt', 'r') as epass:
		for line3 in epass:
			line3 = line3.strip()
			passdict.append(line3)
	
	ttiuser = passdict[0]
	ttipass = passdict[1]
	return(ttiuser, ttipass)	
#  ------------
#  End Function
#  ------------
#	
#  --------------------------------
#  Network Device CDP Function
#  --------------------------------
def setCDP(line, ttiuser, ttipass):
	commands = 'show cdp neighbor'																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																													
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
	stdin, stdout, stderr = ssh.exec_command(commands)
	#cdp_out = stdout.read().decode()
	time.sleep(4)
	cdp_out = stdout.read().decode()
	ssh.close()

	with open('files/cdp_nei.txt', 'w') as cdp_nei:
		cdp_nei.write(cdp_out)
	cdp_nei.close()

	with open('files/cdp_temp.txt', 'w') as cdp_temp:
		with open('files/tti-network-devices', 'r') as net_devices:
			for line1 in net_devices:
				line1 = line1.strip()
				with open('files/cdp_nei.txt', 'r') as cdp_nei2:
					for line2 in cdp_nei2:
						line2 = line2.strip()
						if line1 in line2:
							cdp_temp.write(line2 + "\n")
		net_devices.close()
	cdp_temp.close()
	#
	cdp_temp2 = os.system("cat files/cdp_temp.txt \
					| awk '{print $1 " " ,$2 " " ,$3}' \
					| sed 's/Gig /Gi/g'  \
					| sed 's/Te/Te/g' > files/cdp_temp2.txt")
#
#
	with open('files/cdp_final.txt', 'w') as fcdp:
		with open('files/cdp_temp2.txt', 'r') as tcdp:
			for line3 in tcdp:
				line3 = line3 = line3.strip()
				tcdp_list = line3.split()
				tcdp_len = len(tcdp_list)
				for i in range(0, tcdp_len):
					if 'Gi' in tcdp_list[i]:
						fcdp.write(tcdp_list[i] + "\n")

	return()
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Network Device Etherchannel Function
#  --------------------------------
def setEther(line, ttiuser, ttipass):
	commands = 'show etherchannel sum'																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																													
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
	stdin, stdout, stderr = ssh.exec_command(commands)
	ether_out = stdout.read().decode()
	ssh.close()

	with open('files/ether_temp.txt', 'w') as ether_temp:
		ether_temp.write(ether_out)
		ether_temp.close()

	ether_final = os.system("cat files/ether_temp.txt \
                                             | sed -n 's/(P)//gp' | sed 's/(D)//g' \
                                             | sed 's/(SU)//g' | sed 's/(RD)//g' \
                                             | awk '{print $2, " " $4, " " $5}' > files/ether_final.txt")


	return()
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Network Device Trunk Filter Function
#  --------------------------------
def setIntf():
	#cdp_list = []
	trunk_list = []
	with open('files/cdp_final.txt', 'r') as cdp_final:
		cnt = 0
		#cnt1 = 0
		for line in cdp_final:
			line = line.strip()
			trunk_list.append(line)
			with open('files/ether_final.txt', 'r') as ether_final:
				for line1 in ether_final:
					line1 = line1.strip()
					ether_list = line1.split()
					if line in line1:
						cnt = cnt + 1
						trunk_list.append(ether_list[0])
			cnt = cnt + 1

	return trunk_list
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Network Device Trunk Function
#  --------------------------------
def setTrunk(line, ttiuser, ttipass):
	commands = 'show interface trunk'																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																													
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
	stdin, stdout, stderr = ssh.exec_command(commands)
	trunk_out = stdout.read().decode()
	ssh.close()
	#trunk_out.strip('Port')
	return(trunk_out)
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Network Device MAC Function
#  --------------------------------
def setMAC(line, ttiuser, ttipass, macadd):
	commands = 'show mac address address ' + macadd[0]
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())																																
	ssh.connect(line, username=ttiuser, password=ttipass, look_for_keys=False, allow_agent=False)
	stdin, stdout, stderr = ssh.exec_command(commands)
	mac_add = stdout.read().decode()
	ssh.close()
	#trunk_out.strip('Po
	return(mac_add)
#  ------------
#  End Function
#  ------------
#
#  -----------------------------------
#  Network Device Description Function
#  -----------------------------------
def setDesc(line, ttiuser, ttipass):
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
	return()
#  ------------
#  End Function
#  ------------
#
#  -----------------------------------
#  Main
#  -----------------------------------
logging.raiseExceptions=False		
max_buffer = 90000
trunk_list = []
#
# Call Password Function and retrieve Username and Password for file.
plist = setPass()
ttiuser = plist[0]
ttipass = plist[1]
#
# Open file that contains network devices that will be updated.
with open('files/ios-iplist.txt', 'r') as ccthost:
	for line in ccthost:																											
		line = line = line.strip().lower()
		#
		# Retrieve network device Trunk information. Then create a List that 
		# contains the Trunk Interfaces, and write to the proper file.
		with open('files/trunk_intf.txt', 'w') as f:
			trunk_out = setTrunk(line, ttiuser, ttipass)
			trunk_port = trunk_out.split()
			cnt = 0
			pos = '802.1q'
			while cnt <= (len(trunk_port) - 1):
				if pos == trunk_port[cnt]:
					acnt = cnt - 2
					f.write(trunk_port[acnt] + "\n")
				cnt = cnt + 1
		f.close()
		#
		# Call setCDP to get the CDP Neighbor Information.
		setCDP(line, ttiuser, ttipass)
		#
		# Call setEther to get the Etherchannel Summary Information.
		setEther(line, ttiuser, ttipass)
		#
		# Call setIntf to get the Trunk interfaces to filter
		trunk_list = setIntf()
		# 
		# Call setEther to get the Etherchannel Summary Information.
		with open('files/' + line + '-trunk.txt', 'w') as trunk_final:
			with open('files/trunk_intf.txt', 'r') as trunk_temp1:
				for line5 in trunk_temp1:
					trunk_len = len(trunk_list)
					for i in range(0, trunk_len):
						if trunk_list[i] in line5:
							trunk_final.write(line5)	
			trunk_temp1.close()		
		#
		with open('files/tti-mac-table.txt', 'r') as tmac:
			for line1 in tmac:
				#line1 = line1 = line1.strip().lower()
				line1 = line1 = line1.strip()
				macadd = line1.split()
				mac_add = setMAC(line, ttiuser, ttipass, macadd)
				port = mac_add.split()
		
				scnt = 0
				maccnt = 0
				cnt = 0
				while cnt <= (len(port) - 1):
					if macadd[0] == port[cnt]:
						acnt = cnt + 2
						switchport = port[acnt]
						scnt = 0
						with open('files/' + line + '-trunk.txt', 'r') as mac_tab:
							for line2 in mac_tab:
								line2 = line2.strip()	
								if switchport == line2:
									scnt =  1

						if scnt == 0:
							setDesc(line, ttiuser, ttipass)
						mac_tab.close()
					cnt = cnt + 1
		tmac.close()
#  ------------
#  End Main
#  ------------
