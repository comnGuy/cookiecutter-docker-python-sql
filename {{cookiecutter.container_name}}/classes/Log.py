
import os
import logging
from logging.handlers import TimedRotatingFileHandler

LOGS_PATH = 'logs/'


class Log():

    """ Initiates a new logger

    This class initiates a new logger dependent upon the given settings
    set via the environment variables.
    The important outcome to use the new logger is self.logger.

    Example code:

        # Add logger
        logging = Log(__name__).logger
        logging.error('Error message.')

    Args:
        logger: Contains the logger class | logging
    """
    # Here we define our formatter
    FORMATTER = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def __init__(self, current_script=None):
        # Sets the current file name
        if current_script == None:
            self.current_script = os.environ.get('LOGGING_NAME', 'default')
        else:
            self.current_script = current_script
        # Level of logger: DEBUG, INFO, WARNING, ERROR
        self.level = os.environ.get('LOGGING_LEVEL', 'DEBUG')

        # Examples: Controller, Text Recognition ...
        self.module = os.environ.get('LOGGING_MODULE', 'default')

        # When starts the new log file
        self.when = os.environ.get('LOGGING_WHEN', 'midnight')

        # How often starts the new log file
        self.interval = int(os.environ.get('LOGGING_INTERVAL', 1))

        # How much logging is stored till it will removed
        self.backups = int(os.environ.get('LOGGING_BACKUPS', 31))

        # Name of the log
        self.filename = os.environ.get('LOGGING_FILENAME', 'logs.log')

        # Path of the logs
        self.path = os.environ.get('LOGGING_PATH', 'logs/')

        self.check()
        self.set_handler()

        # Sets the logger
        self.logger = logging.getLogger(self.current_script)
        self.logger.setLevel(self.get_level())
        self.logger.addHandler(self.logHandler)

    def check(self):
        """ This function check if the path valid or nod """
        # Log path
        if not os.path.isdir(LOGS_PATH):
            os.mkdir(LOGS_PATH)
        self.path = '{}{}/'.format(LOGS_PATH, self.module)
        # Log Module path
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

    def set_handler(self):
        """ Sets the log handler with the given settings """
        self.logHandler = TimedRotatingFileHandler(
            '{}{}'.format(self.path, self.filename),
            when=self.when,
            interval=self.interval,
            backupCount=self.backups
        )
        self.logHandler.setFormatter(self.FORMATTER)

    def get_level(self):
        """ Returns the log level dependent upon the given setting """
        if self.level == 'DEBUG':
            return logging.DEBUG
        elif self.level == 'INFO':
            return logging.INFO
        elif self.level == 'WARNING':
            return logging.WARNING
        elif self.level == 'ERROR':
            return logging.ERROR
