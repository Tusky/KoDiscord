import json
from collections import namedtuple
from pathlib import Path

# Default settings to be used.
DEFAULTS = {
    "kodi_ip": "localhost",
    "kodi_port": 8080,
    "kodi_username": "",
    "kodi_password": "",
    "auto_start": False,
    "kodiscord_port": 80
}


class Configurations:
    config_file_name = 'config.json'
    settings = None
    client_id = 476526847530631168
    new_settings = False

    def __init__(self):
        self.config_file = Path(self.config_file_name)
        if not self.config_file.exists():
            self.save_default_settings()
        self.load_settings()

    def load_settings(self):
        """
        Loads the settings file, and converts it into a named tuple for easier usage.
        """
        self.settings = json.loads(self.config_file.read_text(),
                                   object_hook=lambda c: namedtuple('settings', c.keys())(*c.values()))

    def save_settings(self, settings=None):
        """
        Saves the current settings into the configuration file.

        :param settings: Settings to save.
        :type settings: dict or None
        """
        if not settings:
            # noinspection PyProtectedMember,PyUnresolvedReferences
            settings = self.settings._asdict()
        self.config_file.write_text(json.dumps(settings, indent=2, sort_keys=True))

    def save_default_settings(self):
        """
        Saves the default settings in case config.json file is missing.
        """
        self.save_settings(DEFAULTS)

    def refresh_settings(self):
        """
        Reloads the settings file.
        """
        self.load_settings()

    def __getattr__(self, item):
        """
        Makes getting configurations easier instead using dictionary.

        :param item: Item to be returned.
        :type item: Any
        :return: Returned configuration
        :rtype: Any
        """
        return getattr(self.settings, item)

    def change_setting(self, key, value):
        # noinspection PyProtectedMember,PyUnresolvedReferences
        setting_dict = self.settings._asdict()
        setting_dict[key] = value
        self.new_settings = True
        self.settings = namedtuple('settings', setting_dict.keys())(**setting_dict)
