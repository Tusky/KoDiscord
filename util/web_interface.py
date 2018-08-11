import asyncio
import threading
from pathlib import Path
from typing import TYPE_CHECKING

import tornado.ioloop
import tornado.web
from tornado import template

loader = template.Loader('web/template/')

if TYPE_CHECKING:
    from util.config import Configurations


class WebInterface(threading.Thread):
    daemon = True

    def __init__(self, config: 'Configurations'):
        self._config = config
        super().__init__()

    def web_interface(self):
        config = self._config

        class ConfigurationHandler(tornado.web.RequestHandler):
            def data_received(self, chunk):
                pass

            def get(self, saved=False):
                config.refresh_settings()
                template_kwargs = {
                    'ip': config.kodi_ip,
                    'port': config.kodi_port,
                    'username': config.kodi_username,
                    'password': config.kodi_password,
                    'saved': saved
                }
                self.write(loader.load("config.html").generate(**template_kwargs))

            def post(self):
                config.change_setting('kodi_ip', self.get_argument('ip'))
                config.change_setting('kodi_port', self.get_argument('port'))
                config.change_setting('kodi_username', self.get_argument('username'))
                config.change_setting('kodi_password', self.get_argument('password'))
                config.save_settings()
                self.get(saved=True)

        class LogHandler(tornado.web.RequestHandler):
            def data_received(self, chunk):
                pass

            def get(self, saved=False):
                try:
                    logs = Path('KoDiscord.log').read_text().split('\n')
                except FileNotFoundError:
                    logs = ['', 'No logs have been found.', '']
                else:
                    logs.reverse()
                    logs = [x.strip() for x in logs if "MainThread" in x]
                    logs.insert(0, '')
                    logs.append('')
                template_kwargs = {
                    'logs': logs,
                }
                self.write(loader.load("logs.html").generate(**template_kwargs))

        return tornado.web.Application([
            (r"/", ConfigurationHandler),
            (r"/logs/", LogHandler),
        ])

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        app = self.web_interface()
        app.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
