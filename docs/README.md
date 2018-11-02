-----------------------------------------------------------------------------------------------------------------------------------
Door Security Project																								by Tim Jackson
-----------------------------------------------------------------------------------------------------------------------------------
The intentions of this project were for a learning point of view. My aim was to understand how GPIO pins work as well as creating
triggers that will alert the owner of a change in state. This led on to introducing a webcam into the mix that would switch on for 
a period of time and record what happens after the door sensor was triggered. also the use of logging information in basic format 
for mostly debugging and security purposes. And lastly I wanted to backup most of the information gathered from the door sensor to
a remote host, using scp(paramiko). 

example of usage:
catching your annoying family members invade your personal space while your away/working!
business service exit

Todo:
-allow owner to turn off remote back up

Next features:
-use webcams mic to record voice
-web controller
-introduce threading for multiple sensors


-----------------------------------------------------------------------------------------------------------------------------------
What you will need:
-----------------------------------------------------------------------------------------------------------------------------------
-raspbian installed on a sd card (raspbian-stretch-lite 2016 or newer)

-Raspberry pi 3 (with working GPIO pins, powersupply, internet connection) No monitor or keyboard will be required
Guide will include how to setup your raspberry pi 3 without monitor or keyboard

-some form of copper wiring (I used 20metres of 16AWG wiring)
-magnet door sensor or 2 paperclips ;)

-host to remote into the pi with (Windows Machine on the same network)
	-win32diskimager
	-putty
	-winscp

-linux based remote-server to backup recordings into (I used a ubuntu server running plex to view my content)


-----------------------------------------------------------------------------------------------------------------------------------
What you will learn
-----------------------------------------------------------------------------------------------------------------------------------
-pi setup without a keyboard or monitor, using local network and SSH

-GPIO setup (very basic!)


-----------------------------------------------------------------------------------------------------------------------------------
GUIDE step-by-step
-----------------------------------------------------------------------------------------------------------------------------------
SD CARD SETUP
---------------------------------------------

download win32diskimager on windows machine ( we will need this to format the sd card from the pi)

insert the pi's sd card in to your machine 

windows search for disk management

open disk management

	locate the 2 partitions currently on the sd card (boot, partition)

	delete both volumes

	add new simple drive to the sd card, doesnt matter what the win32diskimager will take care of the rest

open win32diskimager

	select in the drop box your sd cards device character

	in the image file locate the raspbian image you wish to install on  the sd card

	once confirming the right drive and file

	click write

	wait for imager to finish! (whilst this is installing, download putty and nmap; if youre on a windows machine)

once installation is finished close win32diskimager down

open boot("#") in a folder

	in here you need to insert a file called ssh.txt

	open notepad (windows) or touch /pathtobootvolume/ssh(linux)

		save empty file to boot ("#") and name it ssh.txt

		this will enable ssh from boot

if you dont have an ethernet cable for the pi, you can use wifi from boot too

	open notepad (windows) or nano /pathtobootvolume/wpa_supplicant.conf

	write :

	ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
	update_config=1
	country=<TWO_LETTER_ISO_COUNTRY_CODE>

	network={
    	ssid="<WIFI_NETWORK_NAME>"
   		psk="<WIFI_PASSWORD>"
    	key_mgmt=WPA-PSK

    save as "wpa_supplicant.conf"(windows) or ctrl+x and save as "wpa_supplicant.conf"(linux)

you can now safely remove the sd card and insert it into the pi

then plug in your ethernet cable(if exists) and then plug in your power supply

find your pi on the network

	using zenmap on windows you can scan your local network to find your pi's ip address (network/subnetmask:192.168.1.0/24)
	once you found your network
	open zenmap type in your network (in my case its 192.168.10.0/24) then on the profile select ping scan and click SCAN:

	look through the list of ips on your network and look for the one with the vendor id as Raspberry Pi Foundation

	note the Pi's ip down

	open putty:


Setting up the pi:
---------------------------------------------

using putty type in the ip address of the Rpi in the hostname box, leave port as 22 and click open:

	click YES on the pop up box

	ssh putty terminal will now start

	login as "pi"

	password is "raspberry"

	first thing on a new raspbian instal, is this command

		sudo passwd pi

		enter the new password for your pi and confirm it has changed

	then do this (monkey see monkey doo)

		sudo raspi-config

		go to Advanced > expand filesystem > ENTER

		go to interfaceing options > I2C enable > yes 

		optional : network options > hostname > ok > [enternewhostname] > ok

		please dont change the the username from pi
		my package relies on the pi name remaining the same, new versiosn this will change

		tab to finish > reboot YES.

setting up hardware
---------------------------------------------
	
	camera needs to be plugged into usb 
	check here to see if your webcam is compatible: https://elinux.org/RPi_USB_Webcams

	door sensor, is a circuit from GPIO 18 (pcm_clock) looped round to the ground pin on 6

	the script works like this, 

		if the circuit is complete from pin to ground then this means the door is closed

		if the circuit in uncomplete from the pin to ground then this means the door is open

		for this to work is create a circuit where it is complete when a door is closed,
		when the door opens itll break the circuit.

		paperclip seems to work fine
		probably best to use a magnetic door sensor


Installation:
---------------------------------------------




