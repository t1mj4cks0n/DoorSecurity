#!/usr/bin/python
import paramiko
import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from doormodules.config  import * # import all variables from config file

# default variables for testing
filepath = 	"/home/pi/DoorSecurity/test/test.txt"
destpath = 	"/home/{}/test.txt".remote_user

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(remote_host, username=remote_user, password=remote_passwd)

print "connected successfully!"

sftp = ssh.open_sftp() 
sftp.put(filepath, destpath) 
sftp.close() 
print "copied successfully!"