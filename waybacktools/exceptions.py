class TooManyRequestsError(Exception):
    def __init__(self, message=None):
        if message is None:
            message = (
                "Your IP has been blocked."
                "Save Page Now has a limit of 15 requests per minute."
                "Please try again in 5 minutes."
            )

        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "Archive Not Found"
        super().__init__(message)


class RetryLimitExceededError(Exception):
    def __init__(self, error: str, message=None):
        if message is None:
            message = f"The retry limit has been reached.\n{error}"
        super().__init__(message)
