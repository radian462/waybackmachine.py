class TooManyRequestsError(Exception):
    pass

class NotFoundError(Exception):
    pass

class RetryLimitExceededError(Exception):
    pass