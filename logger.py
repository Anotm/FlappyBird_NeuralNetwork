from ordered_enum import OrderedEnum
import os

class LogLevels(OrderedEnum):
    """Inherits from OrderedEnum to order the Loglevels 
    from lowest to highest precedence

    Order is:
    - debug
    - info
    - warning
    - error
    """
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


class Logger:
    """Logger class to print messages based off the log level set
    Will print if Log is active

    Calling Log at a log level will also log messages from log levels exceeding the set one. 

    For example: logging debug would log debug, info, warning and error. While, logging warning would only log warning and error. 

    """
    log_level = LogLevels.INFO
    print_in_console = True
    log_file_path = 'log.txt'
    
    @classmethod
    def _write_to_file(cls, msg: str) -> None:
        """Write message to log file, creating file if it doesn't exist.

        Args:
            msg (str): The message to log
        """

        if not os.path.exists(cls.log_file_path):
            open(cls.log_file_path, 'w').close()

        with open(cls.log_file_path, 'a') as f:
            f.write(msg + '\n')

    @classmethod
    def print_console(cls, msg: str) -> None:
        """print message in the console if log is active

        Args:
            msg (str): the message to print
        """
        if cls.print_in_console:
            print(msg)
        
        cls._write_to_file(msg)

    @classmethod
    def debug(cls, *msgs) -> None:
        """print debug messages is the log level is equal or lower to itself 

        Args:
            msg (str): the message to print
        """
        if cls.log_level <= LogLevels.DEBUG:
            msg = ' '.join(str(message) for message in msgs)
            cls.print_console(f'[DEBUG] {msg}')

    @classmethod
    def info(cls, *msgs) -> None:
        """print info messages is the log level is equal or lower to itself 

        Args:
            msg (str): the message to print
        """
        if cls.log_level <= LogLevels.INFO:
            msg = ' '.join(str(message) for message in msgs)
            cls.print_console(f'[INFO] {msg}')

    @classmethod
    def warning(cls, *msgs) -> None:
        """print warning messages is the log level is equal or lower to itself 

        Args:
            msg (str): the message to print
        """
        if cls.log_level <= LogLevels.WARNING:
            msg = ' '.join(str(message) for message in msgs)
            cls.print_console(f'[WARNING] {msg}')

    @classmethod
    def error(cls, msgs) -> None:
        """print debug messages is the log level is equal or lower to itself 

        Args:
            msg (str): the message to print
        """
        if cls.log_level <= LogLevels.ERROR:
            msg = ' '.join(str(message) for message in msgs)
            cls.print_console(f'[ERROR] {msg}')
    
    @classmethod
    def add_newline(cls) -> None:
        cls.print_console("")
    
    @classmethod
    def clear_log_file(cls) -> None:
        open(cls.log_file_path, 'w').close()