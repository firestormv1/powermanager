# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.settings
import RPi.GPIO as GPIO





class PowerManagerPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin):

    def initialize(self):
	#Load config vars
        self.powergpiopin = self._settings.get(["powergpiopin"])
        self.fangpiopin = self._settings.get(["fangpiopin"])
        self.printergpiopin = self._settings.get(["printergpiopin"])
	self.invertgpiopins = self._settings.get(["invertgpiopins"])

	#Print logging output
        self._logger.info("OctoPrint PowerManager is starting up.")
        self._logger.info("Power GPIO Pin:   [%s]"%self.powergpiopin)
	self._logger.info("Fan GPIO Pin:     [%s]"%self.fangpiopin)
        self._logger.info("Printer GPIO Pin: [%s]"%self.printergpiopin)
	self._logger.info("Invert GPIO pins: [%s]"%self.invertgpiopins)

	#Disable GPIO warnings and set pin labeling mode.
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

        #Set I/O modes if GPIOs are defined.

    def on_after_startup(self):
        self._logger.info("Hello World! more %s)" % self._settings.get(["url"]))

    def get_settings_defaults(self):
        return dict(
              powergpiopin="-1",
              fangpiopin="-1",
              printergpiopin="-1",
              invertgpiopins="-1"
        )

    def get_template_vars(self):
        return dict(
              powergpiopin=self._settings.get(["powergpiopin"]),
              fangpiopin=self._settings.get(["fangpiopin"]),
              printergpiopin=self._settings.get(["printergpiopin"])
        )

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

__plugin_name__ = "PowerManager"
__plugin_implementation__ = PowerManagerPlugin()
