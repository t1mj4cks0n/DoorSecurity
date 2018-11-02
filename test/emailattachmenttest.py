
import os, sys, time
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from doormodules.config  import *
from doormodules import support
printdebug = support.printdebug


def getEmailFile():
	import glob
	import os

	print "sleeping to allow recording to finish and email file to owner"
	time.sleep(1)
	print "sleep finished"

	testpath = "/home/pi/DoorSecurity/test/"
	list_of_files = glob.glob(testpath + "*.txt") 
	latest_file = max(list_of_files, key=os.path.getctime)
	basefile = os.path.basename(latest_file)

	print "{} FILE sendEmail".format(basefile)
	path = srcDir + latest_file
	print "{} FILEPATH be put into sendEmail".format(testpath)
	try:
		printdebug("Writing Email")
		sendEmail(basefile,testpath)
		printdebug("{} was emailed to {}".format(testpath,notify_email))
	except:
		printdebug("{} could not be sent to {}".format(testpath,notify_email))

def sendEmail(file,filepath):
	import smtplib
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEText import MIMEText
	from email.MIMEBase import MIMEBase
	from email import encoders

	msg = MIMEMultipart()
	
	msg['From'] = from_email
	print msg['From']
	msg['To'] = notify_email
	print msg['To']
	msg['Subject'] = "Security Alert"
	print msg['Subject']
	
	body = "at {}, {} was sent as a emailattachment test!".format(timenow,file)
	print body

	msg.attach(MIMEText(body, 'plain'))
	
	filename = file # this is the file name and file ext
	print "Email file is {}".format(filename)
	attachment = open(filepath, "rb") # filepath = full filepath
	
	part = MIMEBase('application', 'octet-stream')
	print " MIMEBase"
	part.set_payload((attachment).read())
	print " setting payload to read"
	encoders.encode_base64(part)
	print "setting encode_base64"
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	print "add_header {}".format(filename)

	msg.attach(part)
	print "attaching file"
	server = smtplib.SMTP(smtp_server, smtp_port)
	server.starttls()
	print "attempting to login"
	server.login(from_email, from_passwd)
	print "logged in as {}".format(from_email)
	text = msg.as_string()
	print "making msg variable a string"
	server.sendmail(from_email, notify_email, text)
	print server.sendmail(from_email, notify_email, text)
	server.quit()
	print "closing email"


getEmailFile()