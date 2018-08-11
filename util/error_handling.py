import logging

logging.basicConfig(filename='KoDiscord.log', level=logging.INFO,
                    format='%(asctime)s::%(threadName)-10s::%(levelname)-5s::%(funcName)15s::%(name)-15s:: %(message)s')


class ErrorHandler:
    def __init__(self, message):
        self.message = message
        logging.info(message)
        print(message)
