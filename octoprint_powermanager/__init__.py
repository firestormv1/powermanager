# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.settings
import RPi.GPIO as GPIO
from subprocess import call




class PowerManagerPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin):

    def initialize(self):
	#Load config vars
        self.powergpiopin = self._settings.get(["powergpiopin"])
        self.printergpiopin = self._settings.get(["printergpiopin"])
	self.lightgpiopin self._settings.get(["lightgpiopin"])
	self.invertgpiopins = self._settings.get(["invertgpiopins"])

	#Print logging output
        self._logger.info("OctoPrint PowerManager is starting up.")
        self._logger.info("Power GPIO Pin:   [%s]"%self.powergpiopin)
        self._logger.info("Printer GPIO Pin: [%s]"%self.printergpiopin)
        self._logger.info("Light GPIO Pin:  [%s]"%self.lightgpiopin)
	self._logger.info("Invert GPIO pins: [%s]"%self.invertgpiopins)

	#Disable GPIO warnings and set pin labeling mode.
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

        #Sets ON values
        #If inverted, "ON" = FALSE for active-on-low boards.

        if self.invertgpiopins:
            ON = False
            OFF = True
            self._logger.info("Using Inverted tables for GPIO")
        else:
            ON = True
            OFF = False
            self._logger.info("Using Normal tables for GPIO")



        #Set mode OUTPUT for GPIO pins
        GPIO.setup(int(self.powergpiopin), GPIO.OUT)
        GPIO.setup(int(self.lightgpiopin), GPIO.OUT)
        GPIO.setup(int(self.printergpiopin), GPIO.OUT)


        #Sets status flags and initial start
	GPIO.output(int(self.powergpiopin), On) #Turn on power supply.
	GPIO.output(int(self.printergpiopin), On) #Turn on printer.
        GPIO.output(int(self.lightgpiopin), On #Turn on lights.


    def on_after_startup(self):
        self._logger.info("Hello World! more %s)" % self._settings.get(["url"]))


    #Tidy up after shutting down Octoprint.
    def on_shutdown(self):
        GPIO.output(self.printergpiopin, OFF) #Turn off printer
        GPIO.output(self.lightgpiopin, OFF)   #Lights off
	GPIO.output(self.powergpiopin, OFF)   #Turn off power supply.
	GPIO.cleanup()


    def get_settings_defaults(self):
        return dict(
              powergpiopin="-1",
              lightgpiopin="-1",
              printergpiopin="-1",
              invertgpiopins="-1"
        )

    def get_template_vars(self):
        return dict(
              powergpiopin=self._settings.get(["powergpiopin"]),
              lightgpiopin=self._settings.get(["lightgpiopin"]),
              printergpiopin=self._settings.get(["printergpiopin"])
        )

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

__plugin_name__ = "PowerManager"
__plugin_implementation__ = PowerManagerPlugin()
