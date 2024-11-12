############################################################
######################## Modules ###########################
############################################################
import paramiko
import subprocess
import time
import sys
import os
#
output = os.system("cat files/etsla-core-mac-address.txt \
                                             | sed -n 's/dynamic//gp' | sed -n 's/ip,ipx,assigned,other//gp' \
                                             | awk '{print $2, " " $3}'")
                                             #| sed 's/(SU)//g' | sed 's/(RD)//g' \
                                             #| awk '{print $2, " " $4, " " $5}'")
#ether_trunk = stdout.read().decode().rstrip()
print output
