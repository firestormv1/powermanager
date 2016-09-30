Octoprint Power Manager - README.md - BETA

WARNING!  I don't profess to know what I'm doing. I'm not a developer by trade and this is my first "serious" project.  
That being said, as long as you follow the directions (especially the wiring instructions), you shouldn't have any problems.
There is no warranty express or implied, so don't blame me if the printer explodes, your car breaks down, significant other
goes missing or the mortgage goes up on your house.  Please read the instructions and ask questions.

FOREWORD:
This plugin was intended for the Monoprice Select Mini 3D printer which is a great little printer despite some significant
cost-savings done by the manufacturer, namely the power supply is of questionable quality.  That being said, there is nothing 
to say that this plugin won't work for other printers as well.  It uses a standard relay module for the Raspberry Pi (running
OctoPi/OctoPrint) and if properly wired, can be used to perform basic power control actions on the printer via the web UI.
My printer has been heavily modified to run off of a computer power supply which is worlds better than the chinesium power
supply it shipped with.

This plugin was designed with two objectives in mind 1) I wanted to be able to control the PC Power Supply, Printer power, and
the LED lightstrip all via the web-UI, and 2) I wanted to be able to have an emergency shutdown feature that would power down
the printer and PSU in the event of a catastrophic failure.

INSTALLATION
In order to install this plugin into your existing octopi setup, perform the following commands (via SSH as pi)
1) Install RPi.GPIO - sudo apt-get install python-dev python-rpi.gpio
2) Install this plugin - ~/oprint/bin/pip install https://github.com/firestormv1/powermanager/archive/master.zip
3) Set permissions on the GPIO device to allow non-root users to access it.
    (TODO: I need to find what I used to get it to work.)
4) Shutdown OctoPi and install hardware.
5) Install hardware, make note of GPIO pins. See HARDWARE below.
6) Boot RasPi
5) Review logs for errors.  (PowerManager will complain that GPIOs are disabled, this is normal in a first-start condition)
6) login to the web-UI and configure via Settings/Plugins/Power Manager
7) Save your changes in the settings dialog.
8) Restart Octoprint via Power menu (to ensure settings are applied). On restart, printer should power on and start up.







#### Versions
0.0.0B - 09/21/16 - Initial Release
