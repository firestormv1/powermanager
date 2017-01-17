Octoprint Power Manager - README.md - BETA

WARNING!  I don't profess to know what I'm doing. I'm not a developer by trade and this is my first "serious" project.  That being said, as long as you follow the directions (especially the wiring instructions), you shouldn't have any problems.  There is no warranty express or implied, so don't blame me if your prints don't adhere, the printer explodes, your car breaks down, significant other goes missing or the mortgage goes up on your house.  Please read the instructions and ask questions.    
By downloading and using this plugin, you accept the warning above and agree not to hold me responsible for the 3D Printer Apocalypse.  

FOREWORD:
This plugin was intended for the Monoprice Select Mini 3D printer which is a great little printer despite some significant
cost-savings done by the manufacturer, namely the power supply of questionable quality.  That being said, there is nothing 
to say that this plugin won't work for other printers as well.  It uses a standard relay module for the Raspberry Pi (running
OctoPi/OctoPrint) and if properly wired, can be used to perform basic power control actions on the printer via the web UI.
My printer has been heavily modified to run off of a computer power supply which is worlds better than the chinesium power
supply it shipped with.

This plugin was designed with two objectives in mind 
1. I wanted to be able to control the PC Power Supply, Printer power, and the LED lightstrip all via the web-UI, and  
2. I wanted to be able to have an emergency shutdown feature that would power down the printer in the event of a catastrophic failure.

## INSTALLATION
In order to install this plugin into your existing octopi setup, perform the following commands (via SSH as pi)

~~1. Install RPi.GPIO - sudo apt-get install python-dev python-rpi.gpio~~
~~2. Install this plugin - ~/oprint/bin/pip install https://github.com/firestormv1/powermanager/archive/master.zip~~
~~3. Set permissions on the GPIO device to allow non-root users to access it.~~  
    ~~(TODO: I need to find what I used to get it to work.)~~  
1. Go to the Plugins section of Octoprint, and provide this github repo's URL to the installer.  Steps above are handled automatically. :)    
4. Shutdown OctoPi and install hardware.  
5. Install hardware, make note of GPIO pins. See GPIO under HARDWARE below.  PowerManager uses BCM designations for GPIO pins.
6. Boot RasPi  
7. Review logs for errors.  (PowerManager will complain that GPIOs are disabled, this is normal in a first-start condition)  
8. login to the web-UI and configure via Settings/Plugins/Power Manager  
9. Save your changes in the settings dialog.  
10. Restart Octoprint via Power menu (to ensure settings are applied). On restart, printer should power on and start up.  
  
## USAGE AND CONFIGURATION
#### Configuration
Configuring PowerManager is done through the Settings Menu, under Plugins.  Simply tell PowerManager what GPIO pins are assigned to the three functions (Printer, PSU, and Lights) and save your settings.  If your board requires inverted signalling, select this option, then click Save to save your changes.  Hit F5 to ensure that your browser reflects the updated settings, then test by clicking the various options under the PowerManager tab.  You don't have to use all three functions if  you have a smaller relay board.  Just leave the un-needed GPIO declarations at "-1" to disable those functions.  The buttons will be present, but they will only log a message when pressed instead of performing an action.

#### Usage
Usage of this plugin is pretty straight forward, it sits idle until you need it.  Invoking PowerManager actions is done by one of two methods, either by clicking on one of the three buttons in the navbar at the top, or by accessing the PowerManager panel page.  (Click on the triple line icon to the right of the Temperature/Control/Timelapse tabs to access the PowerManager tab menu)  
  
The EMERGENCY STOP button currently does one thing, it shuts off the printer in whatever state it's in, whatever it's doing at the time.  It's the web-based equivalent to pulling the power cable mid-print.  

**If you use the EMERGENCY STOP button, you will not be able to resume your current print.  You will have to clear whatever is on the buildplate and start your print over again. **
In order to recover from an EMERGENCY STOP, access the PowerManager tab menu and turn on the Printer using the Printer button.  After the printer powers up, click "Connect" on the left hand sidebar to reestablish communication with the printer.

It's been seen that sometimes Octoprint can be finicky about reconnecting after the printer's been shut off. If you are initially unable to connect, shut the printer off first, count to 10, turn the printer back on, count to 10 and refresh Octoprint (F5 in most browsers), then try connecting via Octoprint's UI again.
  
## HARDWARE
This plugin was written using this interface board:  http://amzn.to/2dj6aIF  This board was selected as it is compatible with the RasPi's 3.3v GPIO pins, is electronically isolated from the switching side via optical isolators (not transistors) and is physically protected from high voltage at the relay contacts via PCB separation.  You could in theory switch 120V mains voltage with this relay board without fear of blowing your Pi.

The only other mod that needs to be performed is to have the printhead cooling fan directly connected to +12V.  This ensures that in an emergency shutdown condition, the fan stays running to rapidly cool the printhead.  I tried to get it wired through the relay board, however my printer switched ground, not +12V and appeared to do some weird  stuff with +12v (possibly PWM) which adversely impacted me from wiring it to a relay.  Rather than risk damage to the printer's controller board, I just bypassed it entirely for the head fan.

## Wiring
In order to connect a PC power supply to the interface board, you will need to build or splice the following wires.  Use http://pinouts.ru/Power/atx_v2_pinout.shtml as a guide to the standard ATX power supply.  Wire up the control board as described below.
- For power supply control, you will need the **PS_ON** wire and a ground wire on one relay.  The PS_ON wire should go to the Normally Open side of the relay, and the ground should go to the center contact of the relay. This means the relay must be energized for the PC PSU to turn on.
- For Light control, you will need a yellow **+12V** wire and a ground wire.  The +12V wire should go to a Normally Open side of the relay, and the wire coming from your lights should go to the center contact of the relay. This means the relay must be energized for the lights to turn on.
- For Printer control, you will need **Two +12V** wires and a ground wire. The two +12V wires should be soldered together and go to a Normally Open side of the relay.  The printer's +12V IN line should go to the center contact of the relay.  This means that the relay must be energized for the printer to power up. **Unlike the Lights, the printer is a high current device so we are doubling up on the wire feeding the printer to ensure there is adequate power. Using too thin of a wire will present a fire hazard as the inadequate wire will heat up during operation and could melt and start a fire if amperage draw is too high.**

## GPIO
Be aware that the interface board linked above requires INVERTED signalling (available via the config menu) which means that to turn a relay on requires writing a "0" to the GPIO pin, and turning a relay off requires writing a "1" to the GPIO pin.  If you use other boards, they may require NORMAL signalling (1 to turn on, 0 to turn off) so you'll need to test it to find out what works for your board.  Board installation is simple, +5V to one of the +5v pins on the GPIO header, then the four relays to any four unused GPIO pins. **PowerManager uses the standardized BCM designations for GPIO pins.  Please ensure that you document which relays are connected to what GPIOs for proper configuration.**  Hint:  http://pinout.xyz/ contains lots of useful info for GPIO pinout details for your Pi.  

## Troubleshooting
**GPIO doesn't appear to work.**
- Try manually executing the below commands as the 'pi' user:
> gpio -g mode (some GPIO pin to test) output  
> gpio -g write (GPIO pin) 1   #relay should switch state.  
> gpio -g write (GPIO pin) 0   #relay should switch state  

- Ensure that Pi is part of the gpio group
> groups   #gpio should be listed.  

- Check permissions on /dev/gpiomem
>stat /dev/gpiomem  #Should have permissions 0660 owned by root with group gpio.  

**Buttons don't work.**
>tail -f ~/.octoprint/logs/octoprint.log  
Run that and start clicking buttons.  Look for "octoprint.plugins.powermanager" messages.  You should at least get some startup info when Octoprint starts and should get a message when a button is pressed.  This will tell you if it's an issue of  Octoprint not getting button click events, or if there's another issue like GPIOs not working.





#### Versions
0.0.0B - 09/21/16 - Initial Release, core components work (buttons in navbar, buttons on tabbed panel, configs)  
1.0.0R - 09/30/16 - Initial public release - May god have mercy on my soul...
