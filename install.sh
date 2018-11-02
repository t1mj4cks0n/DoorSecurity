#!/bin/sh

# This needs to be ran immediately after repo download
echo "installing python dependencies"
sleep 2
# install python and camera dependencies
sudo apt install python-dev python-rpi.gpio -y
sudo apt install ffmpeg python-pip -y
sudo pip install pip-update
sudo pip install setuptools wheels

echo "installing paramiko for scp connections"
sleep 2
# install paramiko and dependencies
cd /home/$USER/
sudo git clone https://github.com/paramiko/paramiko
echo "installing paramiko dependencies and setting it up now"
sudo apt install build-essential libssl-dev libffi-dev -y
cd /home/$USER/paramiko && sudo python setup.py install

# copy config files | set permissions
echo "Copying files to system location for autorunning"
sleep 2
sudo cp /home/$USER/DoorSecurity/confs/doorsensor.service /etc/systemd/system/doorsensor.service
sudo chmod +x /etc/systemd/system/doorsensor.service
sudo cp /home/$USER/DoorSecurity/confs/start_door_sensor.bash /root/start_door_sensor.bash
sudo chmod +x /root/start_door_sensor.bash

echo "setting permission of scripts"
# script permission
cd /home/$USER/DoorSecurity/
sudo chmod +x recordcamera.sh

#start services
echo "reloading system services"
sudo system daemon-reload
sudo systemctl enable doorsensor.service
sudo systemctl start doorsensor.service
echo "doorsensor.service STATUS below, Q to carry on..."
sudo systemctl status doorsensor.service
echo "opening nano on this file ' /home/$USER/DoorSecurity/doormodules/config.py'\n fill this out to configure the program\n PRESS ENTER TO CONTINUE"
read yes
sudo nano /home/$USER/DoorSecurity/doormodules/config.py

sudo rm install.sh



