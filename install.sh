#!/bin/sh
sudo apt update
sudo apt upgrade -y
sudo apt install python-dev python-rpi.gpio git git-core -y
sudo apt install ffmpeg python-pip -y
sudo pip install pip-update
sudo pip install setuptools wheels

# setting up paramiko
cd /home/pi/
sudo git clone https://github.com/paramiko/paramiko
sudo apt install build-essential libssl-dev libffi-dev -y
cd /home/pi/paramiko && sudo python setup.py install

# copy config files | set permissions
sudo cp /home/pi/DoorSecurity/confs/doorsensor.service /etc/systemd/system/doorsensor.service
sudo chmod +x /etc/systemd/system/doorsensor.service
sudo cp /home/pi/DoorSecurity/confs/start_door_sensor.bash /root/start_door_sensor.bash
sudo chmod +x /root/start_door_sensor.bash

# create first time logs
mkdir /home/pi/DoorSecurity/logs/
cd /home/pi/DoorSecurity/logs/
touch debugs_logs door_logs scp_logs
mkdir vids archives

# script permissions
cd /home/pi/DoorSecurity/shscripts/
chmod +x *.sh

#start services
sudo system daemon-reload
sudo systemctl enable doorsensor.service
sudo systemctl start doorsensor.service
sudo systemctl status doorsensor.service
echo "sleeping for 10 then system reboot.\nService should start automatically"
sleep 10



