import datetime
import json
import subprocess
import time

from api.discord_presence import DiscordPresence
from api.kodi import Kodi
from updater import Updater
from util.config import Configurations
from util.system_tray import SysTray
from util.web_interface import WebInterface

running = True


class App:
    play_icon = '\u25B6'
    pause_icon = '\u275A\u275A'
    running = True
    update_rate = 1
    last_state = '{}'

    def __init__(self, configuration):
        self._config = configuration

    def stop(self):
        """
        Stop the application from running.
        """
        self.running = False

    def get_kodi_connection(self):
        """
        Returns a new Kodi connection with recent configurations.

        :return: new Kodi instance
        :rtype: Kodi
        """
        return Kodi(self._config.kodi_ip, self._config.kodi_port, self._config.kodi_username,
                    self._config.kodi_password)

    def update_discord(self, discord: DiscordPresence, play_info: dict,
                       remaining_time: 'datetime.timedelta' = None):
        """
        Updates the Discord Rich Presence display.

        :param remaining_time: The remaining time timedelta if paused.
        :type remaining_time: datetime.timedelta
        :param discord: Discord connection.
        :type discord: DiscordPresence
        :param play_info: Information about the movie/show.
        :type play_info: dict
        """
        if play_info.get('title') is not None and remaining_time is not None:
            discord.connect()
            if play_info['playing']:
                icon = self.play_icon
                state = None
                end = play_info['end_time']
            else:
                icon = self.pause_icon
                if remaining_time.seconds > 3600:
                    time_remaining = time.strftime('%H:%M:%S', time.gmtime(remaining_time.seconds))
                else:
                    time_remaining = time.strftime('%M:%S', time.gmtime(remaining_time.seconds))
                state = '{time_remaining} left'.format(icon=icon, time_remaining=time_remaining)
                end = None
            discord.update_status(details='{icon} {title}'.format(icon=icon, **play_info),
                                  large_image=play_info['type'],
                                  state=state, end=end)
        else:
            discord.disconnect()

    def run(self):
        """
        Main running thread.
        """
        discord = DiscordPresence(self._config.client_id)
        kodi = self.get_kodi_connection()
        while self.running:
            time.sleep(self.update_rate)
            if config.new_settings:
                kodi = self.get_kodi_connection()
                config.new_settings = False
            elif self.update_rate > 1:
                kodi = self.get_kodi_connection()  # refresh settings, since it was put on timeout
            kodi_info = kodi.get_currently_playing_item()
            if not kodi_info['failed_connection']:
                remaining_time = kodi_info.pop('remaining_time')
                kodi_info_json = json.dumps(kodi_info)
                if self.last_state != kodi_info_json:
                    last_state = json.loads(self.last_state)
                    if last_state.get('playing') != kodi_info.get('playing') or not kodi_info.get('title') \
                            or last_state.get('end_time') != kodi_info.get('end_time'):
                        self.update_discord(discord, kodi_info, remaining_time)
                        self.last_state = kodi_info_json


if __name__ == '__main__':
    updater = Updater()
    if updater.is_there_an_update():
        try:
            subprocess.Popen(['KoDiscord-updater.exe'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        except FileNotFoundError:
            pass
    else:
        config = Configurations()
        kodiscord = App(config)
        sys_tray = SysTray(kodiscord, config)
        sys_tray.start()
        web = WebInterface(config)
        web.start()
        kodiscord.run()
