import os
import threading
import webbrowser
from pathlib import Path
from typing import TYPE_CHECKING

import pystray
from PIL import Image

try:
    # noinspection PyUnresolvedReferences
    from win32com.client import Dispatch
except ImportError:
    pass

# Load only for type checking to bypass circular reference error.
if TYPE_CHECKING:
    from app import App
    from util.config import Configurations

state = None


class SysTray(threading.Thread):
    _app = None
    _tray = None
    _config = None

    def __init__(self, app: 'App', config: 'Configurations'):
        global state
        super().__init__()
        self._app = app
        self._config = config
        self.daemon = True
        state = self._config.auto_start

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

    @staticmethod
    def get_shortcut_file():
        return os.path.join("C:\\Users\\{username}\\AppData\\Roaming\\Microsoft"
                            "\\Windows\\Start Menu\\Programs\\Startup".format(username=os.getlogin()),
                            'KoDiscord.lnk')

    def remove_shortcut(self):
        shortcut_file = self.get_shortcut_file()
        os.remove(shortcut_file)

    def create_shortcut(self):
        shortcut_file = self.get_shortcut_file()
        path = Path(__file__).parents[2]
        shortcut = Dispatch('WScript.Shell').CreateShortCut(shortcut_file)
        shortcut.Targetpath = '{path}\KoDiscord.exe'.format(path=path)
        shortcut.IconLocation = os.path.join(path, 'kodi-icon.ico')
        shortcut.save()

    # noinspection PyUnusedLocal
    def auto_start_on_boot(self, *args, **kwargs):
        global state
        state = not state
        if state:
            self.create_shortcut()
        else:
            self.remove_shortcut()
        self._config.change_setting('auto_start', state)
        self._config.save_settings()

    # noinspection PyUnusedLocal
    def open_settings(self, *args, **kwargs):
        webbrowser.open('http://localhost:{port}'.format(port=self._config.kodiscord_port))

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
                "Settings", self.open_settings,
            ),
            pystray.MenuItem(
                "Autoboot", self.auto_start_on_boot, checked=lambda item: state
            ),
            pystray.MenuItem(
                "Reload Settings", self.reload_settings,
            ),
            pystray.MenuItem(
                "Exit", self.exit_app
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
