import threading
from typing import TYPE_CHECKING

import pystray
from PIL import Image

# Load only for type checking to bypass circular reference error.
if TYPE_CHECKING:
    from app import App
    from config import Configurations


class SysTray(threading.Thread):
    _app = None
    _tray = None
    _config = None

    def __init__(self, app: 'App', config: 'Configurations'):
        super().__init__()
        self._app = app
        self._config = config
        self.daemon = True

    # noinspection PyUnusedLocal
    def exit_app(self, *args):
        """
        Exits the application.

        :param args: forcible passed, but unused.
        :type args: tuple
        """
        self._tray.stop()
        self._app.stop()

    # noinspection PyUnusedLocal
    def reload_settings(self, *args):
        """
        Reloads the settings file.

        :param args: forcible passed, but unused.
        :type args: tuple
        """
        self._config.refresh_settings()

    def build_tray(self):
        """
        Creates the system tray icon.
        """
        try:
            image = Image.open('kodi-icon.ico')
        except FileNotFoundError:
            image = Image.new('RGB', (64, 64))
        menu = pystray.Menu(
            pystray.MenuItem(
                "Exit", self.exit_app
            ),
            pystray.MenuItem(
                "Reload Settings", self.reload_settings,
            ),
        )

        self._tray = pystray.Icon(
            "KoDiscord", image,
            "KoDiscord", menu
        )

        self._tray.run()

    def run(self):
        """
        Thread initializer.
        """
        self.build_tray()
