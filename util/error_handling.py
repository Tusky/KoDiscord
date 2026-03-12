import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

path = Path(f"{os.getenv('LOCALAPPDATA')}/KoDiscord/")
path.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("KoDiscord")
formatter = logging.Formatter(
    '%(asctime)s::%(threadName)-10s::%(levelname)-5s::%(funcName)15s::%(name)-15s:: %(message)s'
)
logger.setLevel(logging.INFO)
file = "KoDiscord.log"
handler = TimedRotatingFileHandler(f'{path}/{file}',
                                   when="midnight",
                                   interval=1,
                                   backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)


class ErrorHandler:
    def __init__(self, message):
        self.message = message
        logger.info(message)
        print(message)
