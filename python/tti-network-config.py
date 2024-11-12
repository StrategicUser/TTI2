from netmiko import ConnectHandler
import getpass
import sys
import time
#
#
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
# ----------------------
# Main Program
# ----------------------
#
# Call Password Function and retrieve Username and Password for file.
plist = setPass()
username = plist[0]
password = plist[1]

device = {
    'device_type': 'cisco_nxos',
    'ip': 'sss-sw1',
    'username': 'admin',
    'password': 'TTI.cisc0',
    'secret': 'TTI.cisc0'
    }

print ("!!!Script for SSH to device!!!")

# Open Network Device List
ipfile=open("/home/strategic/TTI/python/files/iosxe-iplist.txt")

for line in ipfile:
	device['ip']=line.strip("\n")
	configfile=open("/home/strategic/TTI/python/files/" + device['ip'] + "/" + device['ip'] + ".cfg")
	configset=configfile.read()
	configfile.close()
	if device['ip'] in line:
 		print("\n\nConnecting Device ",line)
 		net_connect = ConnectHandler(**device)
 		net_connect.enable()
 		time.sleep(2)
 		print ("Passing configuration set ")
 		net_connect.send_config_set(configset)
 		print ("Device Conigured ")
 

ipfile.close()

