# UPDATES AND INSTALLATIONS
sudo apt-get update
sudo apt-get upgrade -y
# install python dependencies
sudo apt-get install python-dev python-rpi.gpio git git-core -y
# install camera dependencies
sudo apt-get install ffmpeg -y
sudo apt-get install python-pip -y
# update pip and get packages
sudo pip install pip-update
sudo pip install setuptools wheel
# git clone paramiko for scp
cd /home/pi/
sudo git clone https://github.com/paramiko/paramiko
# install paramiko dependencies
sudo apt-get install build-essential libssl-dev libffi-dev python-dev -y
cd /home/pi/paramiko && sudo python setup.py install
# copy door sensor sevice to system location
sudo cp /home/pi/DoorSecurity/confs/doorsensor.service /etc/systemd/system/doorsensor.service
sudo chmod +x /etc/systemd/system/doorsensor.service
# copy root file to start door sensor service
sudo cp /home/pi/DoorSecurity/confs/start_door_sensor.bash /root/start_door_sensor.bash
sudo chmod +x /root/start_door_sensor.bash
# create first time log files
cd /home/pi/DoorSecurity/logs/
touch debug_logs door_logs scp_logs
cd /home/pi/DoorSecurity/
chmod +x recordcamera.sh
# update crontab

# reload daemon's
sudo system daemon-reload
sudo systemctl enable doorsensor.service
sudo systemctl start doorsensor.service
sudo systemctl status doorsensor.service
sleep 10
sudo reboot

# web setup
sudo pip install flask-sqlalchemy mysql-python