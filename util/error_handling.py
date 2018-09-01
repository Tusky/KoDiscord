import logging
from logging.handlers import TimedRotatingFileHandler


def create_timed_rotating_log(log_int: int = 0):
    logger = logging.getLogger("KoDiscord")
    formatter = logging.Formatter(
        '%(asctime)s::%(threadName)-10s::%(levelname)-5s::%(funcName)15s::%(name)-15s:: %(message)s'
    )
    logger.setLevel(logging.INFO)
    try:
        handler = TimedRotatingFileHandler("KoDiscord{log_int}.log".format(log_int=log_int if log_int else ''),
                                           when="midnight",
                                           interval=1,
                                           backupCount=5)
    except PermissionError:
        pass
    else:
        handler.setFormatter(formatter)
        logger.addHandler(handler)


class ErrorHandler:
    def __init__(self, message):
        logger = logging.getLogger("KoDiscord")
        self.message = message
        logger.info(message)
        print(message)
