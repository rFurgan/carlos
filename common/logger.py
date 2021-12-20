class EType(enumerate):
    """
    A class to hold different types of log messages

        `info:`  Message to inform about certain events
        `debug:` Message to locate bugs
        `warn:`  Message to warn about something going wrong without exiting
        `error:` Message to warn about something going wrong and exiting
    """

    info = "INFO"
    debug = "DEBUG"
    warn = "WARN"
    error = "ERROR"


class Logger:
    """
    A class to print formatted messages for better reading
    """

    def __init__(self, name):
        """
        Args:
            `name (str):` Name of the class/method the logger is used in

        Returns:
            `None`
        """
        self._name = name

    def info(self, message):
        """
        Prints an info type log message

        Args:
            `message (str):` Message to be shown

        Returns:
            `None`
        """
        self._log(EType.info, message)

    def debug(self, message):
        """
        Prints a debug type log message

        Args:
            `message (str):` Message to be shown

        Returns:
            `None`
        """
        self._log(EType.debug, message)

    def warn(self, message):
        """
        Prints a warn type log message

        Args:
            `message (str):` Message to be shown

        Returns:
            `None`
        """
        self._log(EType.warn, message)

    def error(self, message):
        """
        Prints an error type log message

        Args:
            `message (str):` Message to be shown

        Returns:
            `None`
        """
        self._log(EType.error, message)

    def _log(self, type, message):
        """
        Prints a log message with the defined name, type and message.
        Serves as the base for the actual log methods

        Args:

            `type (EType):`     Message type
            `message (str):`    Message to be shown

        Returns:
            `None`
        """
        print(f"[{self._name}][{type}] {message}")
