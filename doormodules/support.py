
#!/usr/bin/python
import time
import subprocess
from config import *

def getTime():
	# use this to get the current time
	import datetime
	timerightnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	return timerightnow

def printdebug(message): 
	# used to print messages to the screen and update debug log
	dbprint = "DEBUG: {}".format(message)
	writeDebugLog(message)
	if debug_switch == True:
		print dbprint

def isOpen(remote_host,remote_port): 
	# this is used to connect to the remote server
	printdebug("checking connection to {} on port{} and waiting for results".format(remote_host,remote_port))
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(connection_timeout)
	try:
		s.connect((remote_host, int(remote_port)))
		s.shutdown(socket.SHUT_RDWR)
		return True
	except:
		return False
	finally:
		s.close()

def checkHost(remote_host, remote_port):
	# this is used to attempt conenctions to remote host
	printdebug("checking connection profile: {}@{}".format(remote_user,remote_host))
	ipup = False
	for i in range(connection_retry):
		if isOpen(remote_host, remote_port):
			ipup = True
			break
		else:
			time.sleep(connection_delay)
        return ipup

def remoteConn(): 
	# this is used to check the connection state on the remote server
	if remote_setup == True:
		printdebug("creating connection profile: {}@{}".format(remote_user,remote_host))
		if checkHost(remote_host,remote_port) == True:
			printdebug("connection success to {} on {}".format(remote_host,remote_port))
			return True
		else:
			printdebug("connection failure to {} on {}".format(remote_host,remote_port))
			return False
	else:
		printdebug("remote connection disabled")

def recordTimeCheck(): 
	# this is used to check the times set in the config file to current time for recording
	printdebug("Checking Recording operating hours")
	import time
	import datetime
	currenttime =  datetime.datetime.now()
	start_time = datetime.datetime.combine(datetime.date.today(),datetime.time(hour=record_starthour,minute=record_startminute))
	end_time = start_time + datetime.timedelta(hours=record_runtime)
	if (currenttime >= (start_time - datetime.timedelta(hours=24))) and (currenttime < (end_time - datetime.timedelta(hours=24))):
		time.sleep(1)
		printdebug("is within recording hours")
		return True
	else:
		if (currenttime >= start_time) and (currenttime < end_time):
			printdebug("within recording hours")
			return True
		else:
			printdebug("NOT in recording hours")
			return False

def notifyTimeCheck(): 
	# this is used to check the times set in the config file to current time for notifications
	printdebug("Checking Notification hours")
	import time
	import datetime
	currenttime =  datetime.datetime.now()
	start_time = datetime.datetime.combine(datetime.date.today(),datetime.time(hour=notify_starthour,minute=notify_startminute))
	end_time = start_time + datetime.timedelta(hours=notify_runtime)
	if (currenttime >= (start_time - datetime.timedelta(hours=24))) and (currenttime < (end_time - datetime.timedelta(hours=24))):
		time.sleep(1)
		printdebug("within notification hours")
		return True
	else:
		if (currenttime >= start_time) and (currenttime < end_time):
			printdebug("within notification hours")
			return True
		else:
			printdebug("NOT in notification hours")
			return False

def sendEmail(timenow,file,filepath):
	#this is used to setup the format of an email before sending it
	import smtplib
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEText import MIMEText
	from email.MIMEBase import MIMEBase
	from email import encoders

	msg = MIMEMultipart()
	
	msg['From'] = from_email
	msg['To'] = notify_email
	msg['Subject'] = "Door Security Alert"
	
	body = "at {}, your door was opened!".format(timenow)

	msg.attach(MIMEText(body, 'plain'))
	
	filename = file # this is the file name and file ext
	attachment = open(filepath, "rb") # filepath = full filepath
	
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

	msg.attach(part)
	server = smtplib.SMTP(smtp_server, smtp_port)
	server.starttls()
	server.login(from_email, from_passwd)
	printdebug("logged in as {}, prepared to send email to {}".format(from_email,notify_email))
	text = msg.as_string()
	server.sendmail(from_email, notify_email, text)
	server.quit()
	printdebug("Sending Email has finished Successfully")

def scpCopy(filepath,remote_user,remote_host,destpath): 
	# used to send one file to a remote host, requires password
	import paramiko
	if remoteConn() == True:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(remote_host, username=remote_user, password=remote_passwd)
		writeScpLog(filepath,remote_user,remote_host,destpath)
		printdebug("connected to {}@{} successfully!".format(remote_user,remote_host))
		try:
			sftp = ssh.open_sftp() 
			sftp.put(filepath, destpath) 
			sftp.close() 
			print "copied successfully!"
			return True
		except:
			print "copy failure"
			printdebug("failed scp to {}@{}, file {} was not sent!".format(remote_user,remote_host,filepath))
	else:
		printdebug("remote backup disabled")
		
def moveFile(srcpath,destpath):
	# used to move one file to another directory
	import subprocess
	cmd = "mv"
	line = "{} {} {}".format(cmd, srcpath, destpath)
	try:
		subprocess.Popen(line, shell=True)
		printdebug(line)
	except:
		printdebug("failed to execute line: {}".format(line)) # works

def writeScpLog(srcfile,remote_user,remote_host,destpath): 
	#used to write the line format for the scp log
	print "writing to scp_log..."
	line = "at {}, {} was copied to {}@{}:{}".format(getTime(),srcfile,remote_user,remote_host,destpath)
	file = open(scplogspath, "a")
	file.write("\n" + str(line))
	file.close() # works

def writeDebugLog(message): 
	# used to write the line format for the debug log
	file = open(debuglogs, "a")
	line = {"time": getTime(), "DEBUG":message}
	file.write("\n" + str(line))
	file.close

def writeFile(state,timenow): 
	# used to write the file format for the door log
	file = open(doorlogspath, "a")
	line = {"time ": timenow, "State ": state}
	file.write("\n" + str(line))
	file.close

def recordCamera(timenow): 
	# used to record on camera if within recording times
	if recordTimeCheck() == True:
		printdebug("Attepting to use camera...")
		RecordSuccess = "Camera recording has started!"
		RecordError = "Camera failed to Record"
		RecordBash = "bash recordcamera.sh"
		printdebug("Camera settings: runtime {}, fps {}, res {}, path {}".format(RecordBash, cam_runtime, cam_fps, cam_res, cam_path))
		try:
			subprocess.Popen(['./recordcamera.sh %s %s %s %s' %(cam_runtime,cam_fps,cam_res,cam_path)], shell=True)
			printdebug(RecordSuccess)
		except:
			printdebug(RecordError) 
	else:
		printdebug("Not within camera recording hours")

def createDoorLogs(): 
	# use to create log file
	import os
	if not os.path.exists(doorlogspath):
		file = open(doorlogspath, "w")
		file.close()
		printdebug("Directory " + doorlogspath + " created!")
	else:
		printdebug("Directory " + doorlogspath + " already exists!") 

def createScpLogs(): 
	# use to create log file
	import os
	if not os.path.exists(scplogspath):
		file = open(scplogspath, "w")
		file.close()
		printdebug("Directory " + scplogspath + " created!")
	else:
		printdebug("Directory " + scplogspath + " already exists!") 

def createDebugLogs():
	# use to create log file
	import os
	if not os.path.exists(debuglogs):
		file = open(debuglogs, "w")
		file.close()
		printdebug("Directory " + debuglogs + " created!")
	else:
		printdebug("Directory " + debuglogs + " already exists!") 

def sleepWait():
	# used to set the sleep time between start recording and sending email
	import os
	printdebug("Sleeping for {}, to allow the camera to finish recording".format(cam_runtime))
	time.sleep(int(cam_runtime))

def NotifyOwner(timenow):
	# used to find the latest file saved after recording
	import glob
	import os

	
	sleepWait()
	# get the latest file saved
	if os.path.exists(srcDir):
		list_of_files = glob.glob(srcDir + "*.mkv") 
		srcfullpath = max(list_of_files, key=os.path.getctime)
		basefile = os.path.basename(srcfullpath)
		remotepath = destVideoDir + basefile
		archivepath = archives + basefile
		printdebug("{} is the srcfullpath".format(srcfullpath))
	else:
		printdebug("{} does not exist".fomrat(srcDir))

	# NOTIFY OWNER VIA EMAIL
	if notifyTimeCheck() == True:
		if email_setup == True:
			printdebug("{} will be put into sendEmail".format(srcfullpath))
			try:
				printdebug("Writing Email")
				sendEmail(timenow,basefile,srcfullpath)
				printdebug("{} was emailed to {}".format(srcfullpath,notify_email))
			except:
				printdebug("{} could not be sent to {}".format(srcfullpath,notify_email))
		else:
			printdebug("Email notifications disabled")

	# SCP FILE TO OWNER
	if remoteConn() == True: # remote connection also checks remote setup
		if scpCopy(srcfullpath,remote_user,remote_host,remotepath) == True:
			try:
				moveFile(srcfullpath,archivepath)
			except:
				printdebug("could not archive {}".format(basefile))
		else:
			printdebug("could not send {} to {}@{}".format(basefile,remote_user,remote_host))

def sendLogs():
	pass