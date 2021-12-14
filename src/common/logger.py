from enum import Enum


class LogType(Enum):
    """
    A class used for enumerations to represent different log levels

    Attributes
    ----------
    INFO : str
        Log level that informs the user
    WARN : str
        Log level that warns the user but does not stop the program
    ERROR : str
        Log level that shows an error and stops the program
    """

    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class Logger:
    """
    A class used to print logs and notify the user

    Methods
    -------
    log(type, message)
        Prints the log message in the specified format
    """

    def __init__(self, class_name: str) -> None:
        """
        Parameters
        ----------
        _class_name : str
            The name of the class the logger is initialized in

        Returns
        -------
        None
        """
        self._class_name: str = class_name

    def log(self, type: LogType, message: str) -> None:
        """
        Prints the log message in the specified format

        Parameters
        ----------
        type : LogType
            The type that represents the log message
        message: str
            The message to be logged to inform the user

        Returns
        -------
        None
        """
        print(f"[{self._class_name}][{type.value}] {message}")
