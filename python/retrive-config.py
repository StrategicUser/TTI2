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
#  Network Config Function
#  --------------------------------
d_out = os.system("cat files/etsla-core-mac-address.txt \
                                            | sed -n 's/dynamic//gp' | sed -n 's/ip,ipx,assigned,other//gp' \
                                            | awk '{print $2, " " $3}' > files/etsla-core-table.txt")
data_list = []
intf = 'interface'
#
with open('files/final-data.txt', 'w') as final_data:
	with open('files/etsla-core-table.txt', 'r') as core_table:
	 	t_flag = 0
		for line in core_table:
			data_list = line.split()
			with open('files/etsla-core-config.txt', 'r') as config:
				for line1 in config:
					line1 = line1.strip()
					if t_flag == 0:
						if data_list[1] in line1:
							print data_list[0]
							t_flag = 1
					else:
						if not intf in line1:
							print line1
						else:
							t_flag = 0
							print '\n'
#
#  ------------
#  End Function
#  ------------
#