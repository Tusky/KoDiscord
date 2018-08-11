import asyncio
import threading
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

        return tornado.web.Application([
            (r"/", ConfigurationHandler),
        ])

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        app = self.web_interface()
        app.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
