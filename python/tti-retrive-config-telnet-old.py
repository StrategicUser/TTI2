#!/usr/bin/env python
# S-Cone.py
# Strategic Service Solutions, Inc.
import sys
import os
import subprocess
import telnetlib
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
#  Network Device MAC Function
#  --------------------------------
def setMACTable(line, ttiuser, ttipass):
	#
	"""use telnetlib to telnet into the switch"""
	tn = telnetlib.Telnet(line)
	tn.open(line)
	#username, password = getCredentials()
	#username
	tn.read_until(b"Username: ")
	tn.write(ttiuser.encode("ascii") + b"\n")
	#password
	if ttipass:
		tn.read_until(b"Password: ")
		tn.write(ttipass.encode("ascii") + b"\n")
	#
	#
	tn.write("terminal length 0\n")
	tn.write("show mac address\n")
	time.sleep(3)
	mac_tab = tn.read_very_eager().decode('ascii')
	tn.close()
	#
	#
	with open('files/mac_temp.txt', 'w') as mac_temp:
		mac_temp.write(mac_tab)
		mac_temp.close()
	#
	#
	mac_final = os.system("cat files/mac_temp.txt \
                                            | sed -n 's/dynamic/dynamic/gp'  \
                                            | awk '{print $3, " " $7}' \
                                            | awk '!/dynamic/' > files/tti-mac-table.txt")
	return
#  ------------
#  End Function
#  ------------
#	
#  --------------------------------
#  Network Device CDP Function
#  --------------------------------
def setCDP(line, ttiuser, ttipass):
	#
	"""use telnetlib to telnet into the switch"""
	tn = telnetlib.Telnet(line)
	tn.open(line)
	#username, password = getCredentials()
	#username
	tn.read_until(b"Username: ")
	tn.write(ttiuser.encode("ascii") + b"\n")
	#password
	if ttipass:
		tn.read_until(b"Password: ")
		tn.write(ttipass.encode("ascii") + b"\n")
	#
	#
	tn.write("terminal length 0\n")
	tn.write("show cdp neighbor\n")
	time.sleep(3)
	cdp_out = tn.read_very_eager().decode('ascii')
	tn.close()
	#
	#
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
					| sed 's/Ten /Te/g' > files/cdp_temp2.txt")
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
					if 'Te' in tcdp_list[i]:
						fcdp.write(tcdp_list[i] + "\n")
	fcdp.close()
	tcdp.close()
	return()
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Network Device Etherchannel Function
#  --------------------------------
def setEther(line, ttiuser, ttipass):
	#
	"""use telnetlib to telnet into the switch"""
	tn = telnetlib.Telnet(line)
	tn.open(line)
	#username, password = getCredentials()
	#username
	tn.read_until(b"Username: ")
	tn.write(ttiuser.encode("ascii") + b"\n")
	#password
	if ttipass:
		tn.read_until(b"Password: ")
		tn.write(ttipass.encode("ascii") + b"\n")
	#
	#
	tn.write("terminal length 0\n")
	tn.write("show etherchannel sum\n")
	time.sleep(3)
	ether_out = tn.read_very_eager().decode('ascii')
	tn.close()

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
	cdp_final.close()
	ether_final.close()
	#
	return trunk_list
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Network Device Trunk Function
#  --------------------------------
def setTrunk(line, ttiuser, ttipass):
	#
	"""use telnetlib to telnet into the switch"""
	tn = telnetlib.Telnet(line)
	tn.open(line)
	#username, password = getCredentials()
	#username
	tn.read_until(b"Username: ")
	tn.write(ttiuser.encode("ascii") + b"\n")
	#password
	if ttipass:
		tn.read_until(b"Password: ")
		tn.write(ttipass.encode("ascii") + b"\n")
	#
	#
	tn.write("terminal length 0\n")
	tn.write("show interface trunk\n")
	time.sleep(3)
	trunk_out = tn.read_very_eager().decode('ascii')
	tn.close()
	return(trunk_out)
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Network Device MAC Function
#  --------------------------------
def setMAC(line, ttiuser, ttipass, macadd):
	#
	"""use telnetlib to telnet into the switch"""
	tn = telnetlib.Telnet(line)
	tn.open(line)
	#username, password = getCredentials()
	#username
	tn.read_until(b"Username: ")
	tn.write(ttiuser.encode("ascii") + b"\n")
	#password
	if ttipass:
		tn.read_until(b"Password: ")
		tn.write(ttipass.encode("ascii") + b"\n")
	#
	#
	tn.write("terminal length 0\n")
	tn.write("show mac address address " + macadd[0] + "\n")
	time.sleep(3)
	mac_add = tn.read_very_eager().decode('ascii')
	tn.close()
	#
	return(mac_add)
#  ------------
#  End Function
#  ------------
#
def setFinalMAC():
	with open('files/tti-mac-table-final.txt', 'w') as tmacfinal:
		with open('files/tti-mac-table.txt', 'r') as tmac:
			for line1 in tmac:
				#line1 = line1 = line1.strip().lower()
				line1 = line1 = line1.strip()
				macadd = line1.split()
				scnt = 0
				with open('files/' + line + '-trunk.txt', 'r') as mac_tab:
					for line2 in mac_tab:
						line2 = line2.strip()
						if line2 == macadd[1]:
							scnt =  1
					if scnt == 0:
						tmacfinal.write(line1 + '\n') 	
				mac_tab.close()
		tmac.close()
	tmacfinal.close()
	return()

#  ----------------------------------
#  Network Data Config Build Function
#  ----------------------------------
def setData(line5):
	d_out = os.system("cat files/intf_final.txt \
	                                | sed -n 's/Gi/GigabitEthernet/gp' > files/intf_final2.txt")
	data_list = []
	dup_intf = []
	intf = 'interface'
	#
	with open('files/' + line5 + '/' + line5 + '-config.txt', 'w') as final_data:
		with open('files/intf_final2.txt', 'r') as core_table:
		 	t_flag = 0
			for line in core_table:
				data_list = line.split()
				with open('files/tti-final-config.txt', 'r') as confg:
					for line1 in confg:
						line1 = line1.strip()
						if t_flag == 0:
							if data_list[1] in line1:
								if data_list[1] in dup_intf:
									print '*** Duplicate Interface ***\n'
								else:
									dup_intf.append(data_list[1])
									final_data.write(data_list[0] + '\n')
									t_flag = 1
						else:
							if not intf in line1:
								final_data.write(line1 + '\n')
							else:
								t_flag = 0
		core_table.close()
	final_data.close()
#
#  ------------
#  End Function
#  ------------
#
#  --------------------------------
#  Pull Network Config Function
#  --------------------------------
def setConf(line, ttiuser, ttipass):
	with open('files/tti-config.txt', 'w') as config:
		#
		"""use telnetlib to telnet into the switch"""
		tn = telnetlib.Telnet(line)
		tn.open(line)
		tn.read_until(b"Username: ")
		tn.write(ttiuser.encode("ascii") + b"\n")
		#password
		if ttipass:
			tn.read_until(b"Password: ")
			tn.write(ttipass.encode("ascii") + b"\n")
		#
		#
		tn.write("terminal length 0\n")
		tn.write("show run\n")
		time.sleep(12)
		trunk_out = tn.read_very_eager().decode('ascii')
		tn.close()
		#trunk_out.strip('Port')
		#trunk_port = trunk_out.split()
		config.write(trunk_out)
		config.close()
		d_out = os.system("cat files/tti-config.txt \
										| sed '/wrr-queue/d' \
										| sed '/mls/d' \
	                                	| sed '/service-policy/d' > files/tti-final-config.txt")	
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
		setMACTable(line, ttiuser, ttipass)
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
		setFinalMAC()
		#
		with open('files/intf_final.txt', 'w') as intf_final:
			with open('files/tti-mac-table-final.txt', 'r') as tmac:
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
							acnt = cnt + 4
							switchport = port[acnt]
							#
							#
							scnt = 0
							with open('files/' + line + '-trunk.txt', 'r') as mac_tab:
								for line2 in mac_tab:
									line2 = line2.strip()	
									if switchport == line2:
										scnt =  1
	
							if scnt == 0:
								intf_final.write(macadd[0] + ' ' + switchport + '\n') 
								
							mac_tab.close()
						cnt = cnt + 1
			tmac.close()
		intf_final.close()
		#
		setConf(line, ttiuser, ttipass)
		#
		setData(line)
		#
#  ------------
#  End Main
#  ------------
