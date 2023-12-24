from util.logging import log


class BotError(Exception):
    """Base class for all bot errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

        log(self.message, level='ERR')

    def __str__(self) -> str:
        return self.message
