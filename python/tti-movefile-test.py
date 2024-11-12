# Ansible Role File 
#
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
from shutil import copyfile
from sys import exit
import os
import shutil
#
# Change and move Ansible files to their proper "Role" location
#
#
#  ------------------------------------------------------------------------
#  Move Template YAML file to Device YAML and update to reflect Device name
#  ------------------------------------------------------------------------
var = 'don-did-it'
mac_final = os.system("cat /home/strategic/TTI/ansible/template.yaml \
                                          | sed 's/template/" + var + "/g' > /home/strategic/TTI/ansible/template-temp.yaml")
#
print("\nSed is done!\n")
print var
#
# Use sed to update the Device YAML file