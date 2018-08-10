import logging

logging.basicConfig(filename='KoDiscord.log', level=logging.INFO)


class ErrorHandler:
    def __init__(self, message):
        self.message = message
        logging.info(message)
        print(message)
