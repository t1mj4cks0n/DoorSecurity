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

Next features:
-use webcams mic to record voice
-web controller
-introduce threading for multiple sensors

##########################################################################################
##                  PLEASE DONT BE AFRAID TO REPORT ANY ISSUE's                         ##
##########################################################################################
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

-linux based remote-server to backup recordings into (I used a ubuntu server running plex to view my content)
	-you can disable a backup host in the config files



-----------------------------------------------------------------------------------------------------------------------------------
GUIDE step-by-step
-----------------------------------------------------------------------------------------------------------------------------------
SD CARD SETUP
---------------------------------------------

download win32diskimager on windows machine ( we will need this to format the sd card from the pi)

insert the pi's sd card in to your machine 

windows search for disk management

open disk management

	>locate the 2 partitions currently on the sd card (boot, partition)

	>delete both volumes

	>add new simple volume to the sd card, doesnt matter whats its called, win32diskimager will take care of the rest

open win32diskimager

	>select in the drop box your sd cards device character

	>in the image file locate the raspbian image you wish to install on  the sd card

	once confirming the right drive and file:

	>click write

	wait for imager to finish! (whilst this is installing, download putty and nmap; if youre on a windows machine)

	after its finish windows will throw up some pop up asking to format the drive, DO NOT CLICK YES, jsut close it down

once installation is finished close win32diskimager down

open boot("#") in a file explorer

	in here you need to insert a file called ssh.txt, to do that:

	open notepad (windows) or touch /pathtobootvolume/ssh(linux):

		>save empty file to boot ("#") and name it ssh.txt

		>check the boot folder for the file and confirm its file extension.

		this will enable ssh from boot!

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

    safely eject the sd card 

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

insert the sd card into the pi

then plug in your ethernet cable(if exists) and then plug in your power supply

wait for pi to load up

find your pi on the network

	using zenmap on windows you can scan your local network to find your pi's ip address (network/subnetmask:192.168.1.0/24)

	if you dont know your network info do this:

	windows button or search bar > "cmd" > open command prompt > type in "ipconfig"

		find your network adapter and note down this:

			IPv4 address: X.X.X.X i.e. 192.168.1.43
			subnetmask  : 255.X.X.X i.e most common is 255.255.255.0

			go to http://www.subnet-calculator.com/

			enter your IPv4 address into IP address box
			enter your subnetmask into the subnet mask box
			then click on the webpage and the screens should refresh with your details changing it

			notedown this info from the site

			SubnetID and Mask Bits
			i.e. 192.166.1.0 and 24
			add them together and you get 192.168.1.0/24 
			once you know what youve worked your out as remember it and input this into zenmap



	once you know your network
	open zenmap type in your network (in my case its 192.168.10.0/24) then on the profile select ping scan and click SCAN:

	look through the list of ips on your network and look for the one with the vendor id as Raspberry Pi Foundation

	note the Pi's ip down

	open putty:


Setting up the pi:
---------------------------------------------

using putty type in the ip address of the Rpi in the hostname box, leave port as 22 and click open:

	>click YES on the pop up box

ssh putty terminal will now start:

	>login as "pi"

	>password is "raspberry"

	first thing on a new raspbian install, is this command:

		>sudo passwd pi

		>enter the new password for your pi and confirm it is successful

	then do this (monkey see monkey doo):

		>sudo raspi-config

		>go to Advanced Options > expand filesystem > ENTER

		>go to interfacing options > I2C enable > yes (you will need this for any future GPIO projects)

		>optional : network options > hostname > ok > [enternewhostname] > ok

		>tab to finish > reboot YES.

	your connection on putty will drop, close it down and re attempt after about 10 seconds


Installation:
---------------------------------------------

log in with your new password

check internet connectivity with ping 8.8.8.8 then ctrl + c

commands

	>sudo apt update && sudo apt upgrade -y

	>sudo apt install git -y (if that dont work try git-core)

	>cd /home/pi/

	>git clone https://github.com/t1mj4cks0n/DoorSecurity

	>cd DoorSecurity/

	>sudo bash install.sh

		enter your username at the start of this script. if your name is pi then enter pi

		setting up paramiko repo will take a while (paramiko credit to = paramiko, this is not owned byme)

		after it has finished intalling you will end up in the config file where you can edit it to your requirements


		key feautures are set to disabled and debugging will be switched on

		if you have a google account you are sending files from do this:

			>keep the smtp port and domain the same

			>go to google accounts and sign in with your from email address

			>turn on allow access to less secure apps

			if that dont work do this:

				>enable 2 step verification for that email you are sending from

				>go to app passwords

				>create a new password for that device

				note down the 16 digit password and enter that into the password section in the config file

		if you use anything other than google, they may use other security features that you will have to research yourself which will allow emails to be sent from less secure devices.

	once the config file is filled out with how you want to use this program the script should run fine. SHOULD!


How I use this program

the trigger is setup on my home study door, with the pi running in a cupboard and a camera resting on the
cupboard facing the door.
the script is always running in the back ground as a service so no need for me to remember to turn it on or had forget to turn it on when it was needed.
ive set the recording hours between midnight running for 17 hours, so anyone entering my study between 0000 hours and 1700 hours will get recorded. i dont want recordings out of them hours as they are the hours i use my study.
ive set my notification hours from 8 in the morning for 9 hours, so anyone entering my study between 0800hours and 1700hours I will get emailed a notification with the file as an attachment immediately. ive set up email notifications from the pi as a VIP contact meaning i will be notiied even with do no disturb set on my phone. i dont want notifying during the night as i dont want to be woken.














