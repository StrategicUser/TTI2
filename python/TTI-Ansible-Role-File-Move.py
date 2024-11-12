#!/usr/bin/env python
# Ansible Role File 
#
import sys
import os
import subprocess
import time
import base64
from getpass import getpass
from pprint import pprint
from sys import exit
from lxml import etree
import logging
from shutil import copyfile
from sys import exit
#
# Change and move Ansible files to their proper "Role" location
#
#
#  ------------------------------------------------------------------------
#  Move Template YAML file to Device YAML and update to reflect Device name
#  ------------------------------------------------------------------------
def movMainYAML(line):
	print line
	mac_final = os.system("cat /home/strategic/TTI/ansible/template/template.yaml \
                                           | sed 's/template/" + line + "/g' > /home/strategic/TTI/ansible/template/template-temp.yaml")

	dir_src =  "/home/strategic/TTI/ansible/template/template-temp.yaml"
	#
	dir_dst = "/home/strategic/TTI/ansible/" + line + ".yaml"
	try:
		copyfile(dir_src, dir_dst)
	except IOError as e:
		print("Unable to copy file. %s" %e)
		exit(1)
	
	print("\nMain YAML file copied!\n")
	return()
#
#
#  --------------------------------------------------------------------
#  Move Template Rfile to Device YAML and update to reflect Device name
#  --------------------------------------------------------------------
def movConfigFile(line):

	dir_src =  "/home/strategic/TTI/ansible/template/template-config.cfg"
	#
	dir_dst = "/home/strategic/TTI/ansible/roles/" + line + "/files/" + line + "-config.cfg"
	try:
		copyfile(dir_src, dir_dst)
	except IOError as e:
		print("Unable to copy file. %s" %e)
		exit(1)
	
	print("\nDevice Configuration file copied!\n")
	return()
#
#
#  ---------------------------------------------------
#  Move Template Password file to Device Password File
#  ---------------------------------------------------
def movPasswdFile(line):
	dir_src =  "/home/strategic/TTI/ansible/template/template-pass.yaml"
	#
	dir_dst = "/home/strategic/TTI/ansible/roles/" + line + "/vars/pass.yaml"
	try:
		copyfile(dir_src, dir_dst)
	except IOError as e:
		print("Unable to copy file. %s" %e)
		exit(1)
	
	print("\nPassword file copied!\n")
	return()
#
#
#  -----------------------------------------------------
#  Move Template Main YML file to Device Main YML File
#  -----------------------------------------------------
def movMainFile(line):
	mac_final = os.system("cat /home/strategic/TTI/ansible/template/template-main.yml \
                                           | sed 's/template/" + line + "/g' > /home/strategic/TTI/ansible/template/template-main-temp.yml")

	dir_src =  "/home/strategic/TTI/ansible/template/template-main-temp.yml"
	#
	dir_dst = "/home/strategic/TTI/ansible/roles/" + line + "/tasks/main.yml"
	try:
		copyfile(dir_src, dir_dst)
	except IOError as e:
		print("Unable to copy file. %s" %e)
		exit(1)
	
	print("\nDevice Configuration file copied!\n")
	return()
#
#
#  ----------------------------------
#  Move Template Device YAML file to Device YAML file
#  ----------------------------------
def movDeviceYAMLFile(line):
	mac_final = os.system("cat /home/strategic/TTI/ansible/template/template-config.yaml \
                                           | sed 's/template/" + line + "/g' > /home/strategic/TTI/ansible/template/template-config-temp.yaml")

	dir_src =  "/home/strategic/TTI/ansible/template/template-config-temp.yaml"
	#
	dir_dst = "/home/strategic/TTI/ansible/roles/" + line + "/tasks/" + line + "-config.yaml"
	try:
		copyfile(dir_src, dir_dst)
	except IOError as e:
		print("Unable to copy file. %s" %e)
		exit(1)
	
	print("\nDevice Configuration file copied!\n")
	return()
#  -----------------------------------
#  Main
#  -----------------------------------
#
# Open file that contains network devices that will be updated.
with open('files/ios-iplist.txt', 'r') as ccthost:
	for line in ccthost:																											
		line = line = line.strip().lower()
		#
		# Create Device Roles
		AnsibleRoles = os.system("ansible-galaxy init /home/strategic/TTI/ansible/roles/" + line + " --force")
		#
		movMainYAML(line)
		#
		movConfigFile(line)
		# 
		movPasswdFile(line)
		#
		# 
		movMainFile(line)
		#
		#
		movDeviceYAMLFile(line)
		# 
	ccthost.close()
