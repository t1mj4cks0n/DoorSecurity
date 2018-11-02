#!/bin/bash
nohup ffmpeg -t 60 -f v4l2 -framerate 25 -video_size 1280x720 -i /dev/video0 -t 300 /home/pi/DoorSecurity/logs/vids/door60sec$(date +%Y%m%d%H$M%S).mkv &>/dev/null &


