#FOR TESTING - NOT NEEDED FOR BUILD

from tkinter import *
from tkinter import ttk
import subprocess
import yaml
import shlex
import os
import time
import paramiko
import sshCommands
import settings

publickey_path = r"C:\Users\TaylorSeger\.ssh\authorized_keys"
dropbear_path = "/etc/dropbear/authorized_keys"
host = "192.168.1.200"
user = "root"
print(publickey_path)

#Generate Private Key

pkey = paramiko.RSAKey.generate(4096)
pkey.write_private_key_file(publickey_path)

mykey = paramiko.RSAKey.from_private_key_file(publickey_path)

###################### SSH Connect #########################
try:
    print('[*] Connecting to S-Cone via SSH')
    #ssh = paramiko.SSHClient()
    settings.init()
    settings.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    settings.ssh.connect(host, username=user, pkey = mykey, password = "Strategic3!@#$")
    #exit_code = stdout.read().decode('ascii').strip("\n")
    #output = ssh.read()
    #output = stdout.read().decode()
    #print (output)
    print('[*] Connected successfully')
    time.sleep(1)

except:
    print('[*] Could NOT connect via SSH. Check your connectivity to the S-Cone.')
    sys.exit()

sshCommands.pingNat('8.8.8.8')