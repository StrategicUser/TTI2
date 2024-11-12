from shutil import copyfile
from sys import exit
import os
import shutil

src_dir = raw_input('Enter sss-sw1 Directory to Move: ')
src_file = raw_input('Enter File To Move: ')

#Move Ansible Files
dir_src =  "/home/strategic/TTI/ansible/roles/sss-sw1/" + src_dir + "/" + src_file
#
with open('files/tti-host.txt', 'r') as hostfile:
	for line in hostfile:
		line = line.strip().lower()
		dir_dst = "/home/strategic/TTI/ansible/roles/" + line + "/" + src_dir + "/" + src_file
		try:
			copyfile(dir_src, dir_dst)
		except IOError as e:
			print("Unable to copy file. %s" %e)
			exit(1)

print("\nFile copy done!\n")


