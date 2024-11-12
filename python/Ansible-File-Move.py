from shutil import copyfile
from sys import exit
import os
import shutil

src_file = raw_input('Enter File to Move: ')
des_dir = raw_input('Enter Directory: ')

#Move Ansible Files
dir_src =  "/home/sssuser/ETS/python/" + src_file
#
with open('files/ets-host.txt', 'r') as hostfile:
	for line in hostfile:
		line = line.strip().lower()
		dir_dst = "/home/sssuser/ETS/roles/" + line + "/" + des_dir + "/" + src_file
		try:
			copyfile(dir_src, dir_dst)
		except IOError as e:
			print("Unable to copy file. %s" %e)
			exit(1)

print("\nFile copy done!\n")


