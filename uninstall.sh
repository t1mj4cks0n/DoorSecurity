echo this will remove everything that the installation script isntalled
echo "if you are ok with this confirm your username now, else ctrl + C"
read homeuser
username=$homeuser
apt remove python-dev python-rpi.gpio ffmpeg python-pip -y
pip uninstall setup-tools
rm -rf /home/$username/paramiko
apt remove libssl-dev libffi-dev -u
rm /etc/systemd/system/doorsensor.service
rm /root/start_door_sensor.bash
rm -rf /home/$username/DoorSecurity
systemctl daemon-reload

