#!/bin/bash

# Door Sensor Bash file called by systemd doorsensor.service
cd /home/pi/DoorSecurity
sudo python door_sensor.py
