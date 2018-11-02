import smtplib
import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from doormodules.config  import *
 
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(from_email, from_passwd)
 
msg = "This is a test message"
server.sendmail(from_email, notify_email, msg)
server.quit()