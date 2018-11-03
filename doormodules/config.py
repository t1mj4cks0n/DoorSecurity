#!/usr/bin/python

''' config file - use this file to edit the variables used in the main script'''
#;; required modules
import datetime

#-----------------------------------------------------------------------------------#
#                                LOCAL HOST SETTINGS
#-----------------------------------------------------------------------------------#
#;; change this to the host username # default pi
#host_user = "pi"
host_user = "pi" 

#;; change this if you want to use your own time format for logging
#timenow = time.asctime(time.localtime(time.time())) # function call to get localtime
timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#-----------------------------------------------------------------------------------#
#                           		 OPERATING HOURS
#-----------------------------------------------------------------------------------#
### Warning, 08 and 09 are octal convert into int e.g. int("08")
#;; change this to the time of day you wish for the device to record from
record_starthour = int("08") # hour day 08 and 09 wont work
record_startminute = int("00") # mins of the hour 

#;; change this to the number of hours you wish for the device to record for per day
record_runtime = int("23") # number of hours for runtime from start time

#;; change this to the time of day you would like to be notified if the door is open
notify_starthour = int("08")
notify_startminute = int("00")

#;; change this to the number of hours you wish for the notification alert to run for
notify_runtime = int("23")


#-----------------------------------------------------------------------------------#
#                           		 EMAIL SETUP
#-----------------------------------------------------------------------------------#
#;; enable to allow email notifications
email_setup = False

#;; change this to the email address you want notifications going to
notify_email = "emailtonotify@emaildomain"

#;;change this to the smtp address of your email domain and their port# default google
smtp_server = "smtp.gmail.com" # this is your email domains server
smtp_port = 587 # this is the port your email domain server uses

#;; change this to the email address you want notifications being sent from
from_email = "emailname@emaildomain"
from_passwd = "enter email password here"


#-----------------------------------------------------------------------------------#
#                            REMOTE SERVER CONECTION SETTINGS
#-----------------------------------------------------------------------------------#
#;; enable the connection to remote host to get backups
remote_setup = False

#;; change this for the ip or hostname of the remote server you want to copy
#;; files too
remote_user = "<username>"

#;; change this for the remote host ip used on the remote server
remote_host = "<ip or host>"

#;; change this for the remote host's passwd' used on the remote server
remote_passwd = "<password>"

#;; change this for ssh port used on the remote server # default port 22
remote_port = 22

#;; change this to edit the number of retrys connecting to the remote host 
#;; # default 5 seconds
connection_retry = 5 

#;; change this to edit the time between each retry connecting to remote host 
#;; # default 10 seconds
connection_delay = 10 

#;; change this to edit the connection to time out after attempting to connect
#;; to remote host # default 3 seconds
connection_timeout = 3

#-----------------------------------------------------------------------------------#
#                LOCAL HOST DIRECTORY SETTINGS /DoorSecurity
#-----------------------------------------------------------------------------------#
#;; change this to the full directory path for the logs
alllogspath = "/home/{}/DoorSecurity/logs/".format(host_user)

#;; change this to the full path of the door state log
doorlogspath = "/home/{}/DoorSecurity/logs/door_log".format(host_user)

#;; change this to the full path of the scp connection log
scplogspath = "/home/{}/DoorSecurity/logs/scp_log".format(host_user)

#;; change this to the full path of the debug log
debuglogs = "/home/{}/DoorSecurity/logs/debug_logs".format(host_user)

#;; change this to the full path of the Movie directory
srcDir = "/home/{}/DoorSecurity/logs/vids/".format(host_user)

#;; chnage this to the full path of the Archives directory
archives = "/home/{}/DoorSecurity/logs/archives/".format(host_user)

#-----------------------------------------------------------------------------------#
#                    REMOTE SERVER DIRECTORY SETTINGS
#-----------------------------------------------------------------------------------#
#;; change this to the full path of remote server films directory
destVideoDir = "/home/{}/".format(remote_user)

#;; change this to the full path of the remote server logs Directory
destLogsDir = "/home/{}/".format(remote_user)


#-----------------------------------------------------------------------------------#
#                    			CAMERA SETTINGS
#-----------------------------------------------------------------------------------#
#;; change this to the number of seconds you want you camera to record for after
#;; being trigger # default 60
cam_runtime = str(60)

#;; change this to the number of frames you want the camera recording at #default 25
cam_fps = str(25)

#;; change this to the resolution to record in # default 1280x720
cam_res = str("1280x720")

#;; change this to the camera location if different to default /dev/video0
cam_path = str("/dev/video0")

#-----------------------------------------------------------------------------------#
#                    			DEBUGGING
#-----------------------------------------------------------------------------------#
#;; change this to true if you wish for debugging statements to be printed to
#;; to the CLI
debug_switch = True
