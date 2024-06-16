#!/usr/bin/python3

class Log:
    """Class with message code colors for logging
        Use it: Log.error("Error message")
    """

    RESET = "\033[0m"
    BLACK = "\033[30m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    WHITE = "\033[37m"
    YELLOW = "\033[33m"

    @staticmethod
    def error(message, finish=True):
        """Prints [ERROR] followed by a message.
        Parameters
        ----------
        message : string
            Message to show at terminal
        finish : bool, optional
            If it is true, the exection stops (default is true)
        """
        print(f"{Log.RED}[ERROR] {Log.RESET}{message}")
        if finish:
            exit(1)

    @staticmethod
    def warning(message):
        """Prints [WARNING] followed by a message.
        Parameters
        ----------
        message : string
            Message to show at terminal
        """
        print(f"{Log.YELLOW}[WARNING] {Log.RESET}{message}")

    @staticmethod
    def info(message):
        """Prints [INFO] followed by a message.
        Parameters
        ----------
        message : string
            Message to show at terminal
        """
        print(f"{Log.BLUE}[INFO] {Log.RESET}{message}")

    @staticmethod
    def debug(message):
        """Prints [DEBUG] followed by a message.
        Parameters
        ----------
        message : string
            Message to show at terminal
        """
        print(f"{Log.CYAN}[DEBUG] {Log.RESET}{message}")