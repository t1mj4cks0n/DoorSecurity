#!/bin/sh
echo "##########################################################"
echo " 	installer for DoorSecurity"
echo " 	this should be run as root with the sudo cmd"
echo "##########################################################"
echo \nYou are :$USER
echo This should say root, what is your username? i.e pi
read homeuser
username=$homeuser
echo You are $username@$hostname
echo "##########################################################"
echo 			install python and camera dependencies
echo "##########################################################"
apt install python-dev python-rpi.gpio -y
apt install ffmpeg python-pip -y
pip install pip-update
pip install setuptools
cd /home/$username/
sleep 5
echo "##########################################################"
echo 			install paramiko and dependencies
echo "##########################################################"
su - $username -c "git clone https://github.com/paramiko/paramiko"
echo Installing paramiko dependencies and setting it up now
apt install build-essential libssl-dev libffi-dev -y
cd /home/$username/paramiko && sudo python setup.py install
sleep 5
echo "##########################################################"
echo 				Configuring File system
echo "##########################################################"
cp /home/$username/DoorSecurity/confs/doorsensor.service /etc/systemd/system/doorsensor.service
chmod +x /etc/systemd/system/doorsensor.service
cat <<EOF >/root/start_door_sensor.bash
#!/bin/bash
cd /home/$username/DoorSecurity
sudo python door_sensor.py
EOF
su - $username -c "mkdir /home/$username/DoorSecurity/logs"
cd /home/$username/DoorSecurity/logs
su - $username -c "mkdir archives/ vids/"
cd /home/$username/DoorSecurity/
su - $username -c "chmod +x recordcamera.sh"
sleep 5
echo "##########################################################"
echo 				Restarting the Services
echo "##########################################################"
systemctl daemon-reload
systemctl enable doorsensor.service
systemctl start doorsensor.service
echo doorsensor.service STATUS below, Q to carry on...
systemctl status doorsensor.service
echo opening nano on this file  /home/$username/DoorSecurity/doormodules/config.py\n fill this out to configure the program\n PRESS ENTER TO CONTINUE
sleep 5
su - $username -c "nano /home/$username/DoorSecurity/doormodules/config.py"
rm install.sh



