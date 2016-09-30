# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.settings
import flask
import RPi.GPIO as GPIO




class PowerManagerPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.BlueprintPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.EventHandlerPlugin,
                       octoprint.plugin.SettingsPlugin):

    #
    # INITIALIZATION - By default, we'll start up and turn the psu, printer, and LEDs on.
    #
    def initialize(self):
	#Load config vars
        self.powergpiopin = self._settings.get(["powergpiopin"])
        self.printergpiopin = self._settings.get(["printergpiopin"])
        self.lightgpiopin = self._settings.get(["lightgpiopin"])
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
        #If inverted, "ON" = FALSE for active-on-low relay boards (Sainsmart, etc..).

        if self.invertgpiopins:
            self.ON = 0 
            self.OFF = 1
            self._logger.info("Using Inverted values for GPIO")
        else:
            self.ON = 1
            self.OFF = 0
            self._logger.info("Using Normal values for GPIO")

        #Set mode OUTPUT for GPIO pins if defined
	#Turn on power and printer pins.
        if self.powergpiopin == "-1" :
                self._logger.info("Power GPIO pin is undefined.")
        else:
                GPIO.setup(int(self.powergpiopin), GPIO.OUT, initial=self.OFF)
                GPIO.output(int(self.powergpiopin), self.ON)
        if self.lightgpiopin == "-1" :
                self._logger.info("Light GPIO pin is undefined.")
        else:
                GPIO.setup(int(self.lightgpiopin), GPIO.OUT, initial=self.OFF)
                GPIO.output(int(self.lightgpiopin), self.ON)
        if self.printergpiopin == "-1":
                self._logger.info("Printer GPIO pin is undefined.")
        else:
                GPIO.setup(int(self.printergpiopin), GPIO.OUT, initial=self.OFF)
                GPIO.output(int(self.lightgpiopin), self.ON)

    def on_after_startup(self):
        self._logger.info("Octoprint Power Manager running.")

    #
    # BLUEPRINT PLUGIN - We will define our api endpoints and perform actions here.
    # 
    # Each button/action is mapped to its own endpoint to actually do something.

    #Lights On
    @octoprint.plugin.BlueprintPlugin.route("/lightson", methods=["GET"])
    def lightson(self):
        if self.lightgpiopin != "-1":
            GPIO.output(int(self.lightgpiopin),self.ON)
            self._logger.info("Lights turned on.")
        else:
            self._logger.info("Lights disabled, GPIO pin undefined.")
        return flask.make_response("Lights On.")

    #LightsOff
    @octoprint.plugin.BlueprintPlugin.route("/lightsoff", methods=["GET"])
    def lightsoff(self):
        if self.lightgpiopin != "-1":
            GPIO.output(int(self.lightgpiopin),self.OFF)
            self._logger.info("Lights turned off.")
        else:
            self._logger.info("Lights disabled, GPIO pin undefined.")
        return flask.make_response("Lights Off.")

    #PSU On
    @octoprint.plugin.BlueprintPlugin.route("/psuon", methods=["GET"])
    def psuon(self):
        if self.powergpiopin != "-1":
            GPIO.output(int(self.powergpiopin),self.ON)
            self._logger.info("Power Supply turned on.")
        else:
            self._logger.info("PSU disabled, GPIO pin undefined.")
        return flask.make_response("Power Supply On.")

    #PSU Off
    @octoprint.plugin.BlueprintPlugin.route("/psuoff", methods=["GET"])
    def psuoff(self):
        if self.powergpiopin != "-1":
            GPIO.output(int(self.powergpiopin),self.OFF)
            self._logger.info("Power Supply turned off.")
        else:
            self._logger.info("PSU disabled, GPIO pin undefined.")
        return flask.make_response("Power Supply Off.")

    #Printer On
    @octoprint.plugin.BlueprintPlugin.route("/printeron", methods=["GET"])
    def printeron(self):
        if self.printergpiopin != "-1":
            GPIO.output(int(self.printergpiopin),self.ON)
            self._logger.info("Printer turned on.")
        else:
            self._logger.info("Printer disabled, GPIO pin undefined.")
        return flask.make_response("Printer On.")

    #Printer Off
    @octoprint.plugin.BlueprintPlugin.route("/printeroff", methods=["GET"])
    def printeroff(self):
        if self.printergpiopin != "-1":
            GPIO.output(int(self.printergpiopin),self.OFF)
            self._logger.info("Printer turned off.")
        else:
            self._logger.info("Printer disabled, GPIO pin undefined.")
        return flask.make_response("Printer Off.")

    #Emergency Stop
    @octoprint.plugin.BlueprintPlugin.route("/emergencystop", methods=["GET"])
    def emergencystop(self):
	if self.printergpiopin != "-1":
            GPIO.output(int(self.printergpiopin),self.OFF)
            self._logger.info("******** EMERGENCY STOP **********")
        else:
            self._logger.info("**** Emergency Stop called, but printer GPIO not configured! ****")
        return flask.make_response("Emergency Stop has shut down the printer.")







    # This is needed for some reason. TODO: Figure out what exactly this does.
    #I think it's to control authenticated user access to the API endpoints.
    def is_blueprint_protected(self):
        return False


    #
    # EVENTS -I'm putting this here for a new feature.
    #
    # Event handling disabled, for future development.
    def on_event(self, event, payload):
	#elf._logger.info("Received Event: [%s] with payload [%s]", event, payload)
	return

    #
    # SHUTDOWN TASKS - Turn off all devices, perform GPIO cleanup.
    # 
    #Unlike init, we don't really care about invalid values since the system's halting.
    def on_shutdown(self):
        GPIO.output(self.printergpiopin, OFF) #Turn off printer
        GPIO.output(self.lightgpiopin, OFF)   #Lights off
        GPIO.output(self.powergpiopin, OFF)   #Turn off power supply.
        GPIO.cleanup()

    #
    # DEFAULT SETTINGS - Plugin defaults when started for the first time.
    #
    def get_settings_defaults(self):
        return dict(
              powergpiopin="-1",
              lightgpiopin="-1",
              printergpiopin="-1",
              invertgpiopins=False
        )


    #
    # POPULATE VARS from stored settings
    #
    def get_template_vars(self):
        return dict(
              powergpiopin=self._settings.get(["powergpiopin"]),
              lightgpiopin=self._settings.get(["lightgpiopin"]),
              printergpiopin=self._settings.get(["printergpiopin"])
        )

    #
    # Needed by Octoprint, we're not using custom bindings here.
    #
    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False),
            dict(type="tab", custom_bindings=False)
        ]

__plugin_name__ = "PowerManager"
__plugin_implementation__ = PowerManagerPlugin()
