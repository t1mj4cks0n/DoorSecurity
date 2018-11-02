# create first time logs

# re install of repo run this

mkdir /home/pi/DoorSecurity/logs/
cd /home/pi/DoorSecurity/logs/
touch debugs_logs door_logs scp_logs
mkdir vids archives
cd /home/pi/DoorSecurity/doormodules/
touch __init__.py
cd /home/pi/DoorSecurity/test/
touch __init__.py

# script permission
cd /home/pi/DoorSecurity/
sudo chmod +x recordcamera.sh