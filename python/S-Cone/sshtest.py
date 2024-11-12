## sshmodule.py

ip = '192.169.6.205'
pw = 'Strategic3!@#$'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ip, port=1337, username='root', password=pw)