import logging

class Logger:
    def __init__(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler() 
            ]
        )

        self.logger = logging.getLogger(__name__)

    def debug(self, message: str):
        self.logger.debug(message, stacklevel=2)

    def info(self, message: str):
        self.logger.info(message, stacklevel=2)

    def warning(self, message: str):
        self.logger.warning(message, stacklevel=2)

    def error(self, message: str):
        self.logger.error(message, stacklevel=2)
    
    def critical(self, message: str):
        self.logger.critical(message, stacklevel=2)

