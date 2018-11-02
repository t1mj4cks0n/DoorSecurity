#!/bin/bash

nohup ffmpeg -t $1 -f v4l2 -framerate $2 -video_size $3 -i $4 -t 300 /home/pi/DoorSecurity/logs/vids/doorrecord$(date +%Y%m%d%H%M%S).mkv &>/dev/null &


