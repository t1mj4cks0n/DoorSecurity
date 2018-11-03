import RPi.GPIO as GPIO
import time, datetime
import sys, os
from doormodules import support

# setting import module names
logentry = support.writeFile 
printdebug = support.printdebug

# creating logs if they dont already exist
support.createLogsDir()
support.createDoorLogs()
support.createScpLogs()
support.createDebugLogs()

# setting up GPIO pins and trigger states
GPIO.setmode(GPIO.BCM)  # setting GPIO mode to use BCM
DOOR_SENSOR_PIN = 18    # setting GPIO pin to 18 which circuits round to a ground pin
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

print "GPIO pins setup\nDoor Sensor now ready"
printdebug("door_sensor.py started ")

def main():
    Open = None
    Closed = None
    State = None
    while True: 
        Open = Closed
        Closed = GPIO.input(DOOR_SENSOR_PIN)

        if (Closed and (Closed != Open)):
            State = " OPEN "
            print State
            timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            support.recordCamera(timenow)
            support.notifyOwner(timenow)
            logentry(State,timenow)

        elif (Open != Closed):
            State = "CLOSED"
            print State
            timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logentry(State,timenow)
        
        time.sleep(0.1)

if __name__ == "__main__":
    main()
