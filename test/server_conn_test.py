#!/usr/bin/python

#This works. dont break it, use it to check remote host is up
import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from doormodules.config  import *
import socket
import time

ip = remote_host
port = remote_port
retry = connection_retry
delay = connection_delay
timeout = connection_timeout

def isOpen(ip, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(timeout)
	try:
		s.connect((ip, int(port)))
		s.shutdown(socket.SHUT_RDWR)
		return True
	except:
		return False
	finally:
		s.close()

def checkHost(ip, port):
	ipup = False
	for i in range(retry):
		if isOpen(ip, port):
			ipup = True
			break
		else:
			time.sleep(delay)
        return ipup

if checkHost(ip, port):
	print ip + " is UP"
