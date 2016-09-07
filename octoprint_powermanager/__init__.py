# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class PowerManagerPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin):
    def on_after_startup(self):
        self._logger.info("Hello World! more %s)" % self._settings.get(["url"]))

    def get_settings_defaults(selt):
        return dict(url="https://en.wikipedia.org/wiki/Hello_world")

    def get_template_vars(self):
        return dict(url=self._settings.get(["url"]))

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

__plugin_name__ = "PowerManager"
__plugin_implementation__ = PowerManagerPlugin()
