echo This is the installer
echo Always run with the sudo cmd
echo you are $USER
echo you should be root but what is your username??
read username
echo your username is $username
echo installing python and camera dependencies...
sleep 5
apt install python-dev python-rpi.gpio ffmpeg python-pip -y
pip install pip-update
pip install setuptools
cd /home/$username
echo installing paramiko and dependencies...
sleep 5
su -  $username -c "git clone https://github.com/paramiko/paramiko"
apt install build-essential libssl-dev libffi-dev -y
cd /home/$username/paramiko && python setup.py install
echo configuring file system...
sleep 5
cp /home/$username/DoorSecurity/confs/doorsensor.service /etc/systemd/system/doorsensor.service
chmod +x /etc/systemd/system/doorsensor.service
cat <<EOF >/root/start_door_sensor.bash
#!/bin/bash
cd /home/$username/DoorSecurity
sudo python door_sensor.py
EOF
su - $username -c "mkdir /home/$username/DoorSecurity/logs"
su - $username -c "mkdir /home/$username/DoorSecurity/logs/archives"
su - $username -c "mkdir /home/$username/DoorSecurity/logs/vids"
cd /home/$username/DoorSecurity
su - $username -c "chmod +x recordcamera.sh"
echo restarting services...
sleep 5
systemctl daemon-reload
systemctl enable doorsensor.service
systemctl start doorsensor.service
echo PRESS Q to escape from status view
systemctl status doorsensor.service
echo going to config file now, install script will be removed after config edit.
read y
su - $username -c "nano /home/$username/DoorSecurity/doormodules/config.py"
rm install.sh
